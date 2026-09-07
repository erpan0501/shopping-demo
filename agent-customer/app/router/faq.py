import httpx
from fastapi import APIRouter, HTTPException, Query, Request
from uuid import uuid4
from pydantic import BaseModel, Field,ConfigDict
import logging
import re
from time import perf_counter


from ..service.session_service import create_session_service
from ..service.intent_service import IntentService
from ..config import get_settings
from ..java_client import JavaApiError, JavaCircuitOpenError, JavaClient
from ..models import FaqPage
from ..service.faq_service import FaqService
from ..service.faq_vector_service import QdrantFaqRetriever
from ..agent.faq_agent import FaqAgent
from ..llm.deep_seek_client import DeepSeekClient
from ..service.order_service import OrderService
from ..service.handoff_service import HandoffService
from ..service.rate_limit_service import (
    RateLimitExceeded,
    RateLimitStoreUnavailable,
    create_rate_limiter,
)
from ..service.audit_service import AuditService
from ..llm.intent_classifier import IntentClassifier
logger = logging.getLogger(__name__)


def _mask_question(question: str) -> str:
    # 订单号等 19 位数字：只保留前 3、后 4 位
    masked = re.sub(
        r"(?<!\d)(\d{3})\d{12}(\d{4})(?!\d)",
        r"\1************\2",
        question,
    )

    # 手机号：138****0000
    return re.sub(
        r"(?<!\d)(1\d{2})\d{4}(\d{4})(?!\d)",
        r"\1****\2",
        masked,
    )
router = APIRouter(tags=["FAQ"])
settings = get_settings()

java_client = JavaClient(settings)
faq_vector_retriever = (
    QdrantFaqRetriever(settings)
    if settings.faq_retrieval_backend == "qdrant"
    else None
)
faq_service = FaqService(java_client, faq_vector_retriever)
order_service = OrderService(java_client)
handoff_service = HandoffService(settings.handoff_db_path)
audit_service = AuditService(settings.audit_db_path)

deepseek_client = DeepSeekClient(settings)
intent_classifier = IntentClassifier(deepseek_client)
intent_service = IntentService(intent_classifier)

session_service = create_session_service(settings)
chat_rate_limiter = create_rate_limiter(settings)

faq_agent = FaqAgent(
    faq_service=faq_service,
    deepseek_client=deepseek_client,
    session_service=session_service,
    order_service=order_service,
    handoff_service=handoff_service,
    intent_service=intent_service,
)
class ChatRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    question: str = Field(min_length=1)

    session_id: str | None = Field(
        default=None,
        alias="sessionId",
    )

    user_id: int | None = Field(
        default=None,
        alias="userId",
        gt=0,
    )


class ChatResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    matched: bool
    answer: str
    source: str
    session_id: str = Field(alias="sessionId")



@router.get("/faq/search", response_model=FaqPage)
async def search_faq(
    page: int = Query(default=1, ge=1),
    size: int = Query(default=20, ge=1, le=100),
    category_id: int | None = Query(
        default=None,
        ge=1,
        alias="categoryId",
    ),
) -> FaqPage:
    try:
        return await faq_service.search_faq(
            page=page,
            size=size,
            category_id=category_id,
        )
    except JavaCircuitOpenError as exc:
        raise HTTPException(
            status_code=503,
            detail="商城服务正在恢复，请稍后再试。",
            headers={"Retry-After": str(exc.retry_after_seconds)},
        ) from exc
    except (httpx.HTTPError, JavaApiError) as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Java FAQ 接口调用失败：{exc}",
        ) from exc


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, http_request: Request) -> ChatResponse:
    session_id = request.session_id or str(uuid4())
    started_at = perf_counter()
    try:
        user_id = await _resolve_user_id(request, http_request)
    except HTTPException as exc:
        _record_audit(
            session_id=session_id,
            user_id=None,
            source="auth",
            outcome="rejected",
            status_code=exc.status_code,
            elapsed_ms=(perf_counter() - started_at) * 1000,
            error_code=(
                "AUTH_INVALID"
                if exc.status_code == 401
                else "AUTH_SERVICE_UNAVAILABLE"
            ),
        )
        raise

    rate_limit_key = (
        f"user:{user_id}"
        if user_id is not None
        else f"ip:{http_request.client.host if http_request.client else 'unknown'}"
    )
    try:
        await chat_rate_limiter.check(rate_limit_key)
    except RateLimitExceeded as exc:
        _record_audit(
            session_id=session_id,
            user_id=user_id,
            source="rate_limit",
            outcome="rejected",
            status_code=429,
            elapsed_ms=(perf_counter() - started_at) * 1000,
            error_code="RATE_LIMITED",
        )
        raise HTTPException(
            status_code=429,
            detail="请求过于频繁，请稍后再试。",
            headers={"Retry-After": str(exc.retry_after_seconds)},
        ) from exc
    except RateLimitStoreUnavailable as exc:
        _record_audit(
            session_id=session_id,
            user_id=user_id,
            source="rate_limit",
            outcome="failed",
            status_code=503,
            elapsed_ms=(perf_counter() - started_at) * 1000,
            error_code="RATE_LIMIT_STORE_UNAVAILABLE",
        )
        raise HTTPException(
            status_code=503,
            detail="服务保护组件暂时不可用，请稍后再试。",
        ) from exc

    try:
        result = await faq_agent.chat(
            session_id=session_id,
            question=request.question,
            user_id=user_id,
        )

        elapsed_ms = (perf_counter() - started_at) * 1000

        logger.info(
            "chat_completed session_id=%s user_id=%s source=%s "
            "matched=%s elapsed_ms=%.1f question=%s",
            session_id,
            user_id,
            result.source,
            result.matched,
            elapsed_ms,
            _mask_question(request.question),
        )

        _record_audit(
            session_id=session_id,
            user_id=user_id,
            source=result.source,
            outcome="completed",
            status_code=200,
            elapsed_ms=elapsed_ms,
        )

        return ChatResponse(
            matched=result.matched,
            answer=result.answer,
            source=result.source,
            session_id=session_id,
        )

    except (httpx.HTTPError, JavaApiError) as exc:
        elapsed_ms = (perf_counter() - started_at) * 1000

        logger.warning(
            "chat_java_api_failed session_id=%s user_id=%s "
            "elapsed_ms=%.1f question=%s error=%s",
            session_id,
            user_id,
            elapsed_ms,
            _mask_question(request.question),
            exc,
        )

        _record_audit(
            session_id=session_id,
            user_id=user_id,
            source="java",
            outcome="failed",
            status_code=502,
            elapsed_ms=elapsed_ms,
            error_code=_java_error_code(exc),
        )

        raise HTTPException(
            status_code=502,
            detail="商城服务暂时不可用，请稍后再试。",
        ) from exc

    except Exception:
        elapsed_ms = (perf_counter() - started_at) * 1000

        logger.exception(
            "chat_unexpected_error session_id=%s user_id=%s "
            "elapsed_ms=%.1f question=%s",
            session_id,
            user_id,
            elapsed_ms,
            _mask_question(request.question),
        )

        _record_audit(
            session_id=session_id,
            user_id=user_id,
            source="agent",
            outcome="failed",
            status_code=500,
            elapsed_ms=elapsed_ms,
            error_code="UNEXPECTED_ERROR",
        )

        raise HTTPException(
            status_code=500,
            detail="客服服务暂时异常，请稍后再试。",
        )


def _record_audit(**kwargs: object) -> None:
    try:
        audit_service.record_chat(**kwargs)
    except Exception:
        # 审计写入异常不能阻断客服主链路。
        logger.exception("chat_audit_write_failed")


def _java_error_code(error: Exception) -> str:
    if isinstance(error, JavaCircuitOpenError):
        return "JAVA_CIRCUIT_OPEN"
    if isinstance(error, JavaApiError):
        if error.business_code is not None:
            return f"JAVA_BUSINESS_{error.business_code}"
        if error.status_code is not None:
            return f"JAVA_HTTP_{error.status_code}"
    return "JAVA_TRANSPORT_ERROR"


async def _resolve_user_id(request: ChatRequest, http_request: Request) -> int | None:
    authorization = http_request.headers.get("Authorization")
    if authorization:
        try:
            user_id = await java_client.get_current_user_id(authorization)
        except JavaApiError as exc:
            raise HTTPException(
                status_code=502,
                detail="商城身份服务暂时不可用，请稍后再试。",
            ) from exc
        if user_id is None:
            raise HTTPException(status_code=401, detail="登录状态无效或已过期。")
        return user_id

    if request.user_id is not None and not settings.allow_test_user_id:
        raise HTTPException(status_code=401, detail="请提供有效的商城登录令牌。")
    return request.user_id

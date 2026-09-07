"""内部 FAQ 向量索引管理接口。"""

import httpx
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict, Field

from ..java_client import JavaApiError, JavaCircuitOpenError
from ..service.faq_vector_service import FaqVectorError
from ..service.faq_vector_sync_service import FaqVectorSyncService
from .faq import faq_vector_retriever, java_client, settings
from .staff import require_staff_access


router = APIRouter(prefix="/internal/faq-vectors", tags=["内部 FAQ 向量索引"])


class FaqVectorSyncResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    collection: str
    source_count: int = Field(alias="sourceCount")
    indexed_count: int = Field(alias="indexedCount")
    removed_count: int = Field(alias="removedCount")


@router.post(
    "/sync",
    response_model=FaqVectorSyncResponse,
    dependencies=[Depends(require_staff_access)],
)
async def sync_faq_vectors() -> FaqVectorSyncResponse:
    if settings.faq_retrieval_backend != "qdrant" or faq_vector_retriever is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="FAQ 向量检索未启用，请先设置 FAQ_RETRIEVAL_BACKEND=qdrant。",
        )
    try:
        summary = await FaqVectorSyncService(
            java_client,
            faq_vector_retriever,
        ).sync()
    except JavaCircuitOpenError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="商城 FAQ 服务正在恢复，请稍后再试。",
            headers={"Retry-After": str(exc.retry_after_seconds)},
        ) from exc
    except (httpx.HTTPError, JavaApiError) as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="读取商城 FAQ 失败，未执行向量同步。",
        ) from exc
    except FaqVectorError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="FAQ 向量服务暂时不可用。",
        ) from exc

    return FaqVectorSyncResponse(
        collection=settings.faq_qdrant_collection,
        sourceCount=summary.source_count,
        indexedCount=summary.indexed_count,
        removedCount=summary.removed_count,
    )

import httpx
from fastapi import APIRouter, HTTPException

from ..config import get_settings
from ..java_client import JavaApiError, JavaClient
from .faq import session_service

router = APIRouter(tags=["系统"])
settings = get_settings()


@router.get("/health")
async def health() -> dict[str, str]:
    response = {
        "status": "ok",
        "service": settings.app_name,
    }
    response["session_backend"] = settings.session_backend
    return response


@router.get("/health/session")
async def session_health() -> dict[str, str]:
    try:
        # 一个不存在的会话只会读取 Redis，不会创建数据。
        await session_service.get_history("health-check")
        return {"status": "ok", "session_backend": settings.session_backend}
    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail="会话存储不可用，请检查 Redis 配置和网络。",
        ) from exc


@router.get("/health/java")
async def java_health() -> dict[str, object]:
    try:
        page = await JavaClient(settings).search_faq(page=1, size=1)
        return {
            "status": "ok",
            "java_base_url": settings.java_base_url,
            "faq_count": page.total,
        }
    except (httpx.HTTPError, JavaApiError) as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Java FAQ 接口不可用：{exc}",
        ) from exc

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .config import get_settings
from .router.faq import router as faq_router
from .router.system import router as system_router
from .router.staff import router as staff_router
from .router.audit import router as audit_router
from .router.vector import router as vector_router
from .router.staff_console import router as staff_console_router
from .router.faq import chat_rate_limiter, session_service

settings = get_settings()
_STATIC_DIR = Path(__file__).resolve().parent / "static"

@asynccontextmanager
async def lifespan(_: FastAPI):
    yield
    await chat_rate_limiter.aclose()
    await session_service.aclose()


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    lifespan=lifespan,
)
app.mount(
    "/internal/console/assets",
    StaticFiles(directory=_STATIC_DIR),
    name="staff-console-assets",
)

app.include_router(system_router)
app.include_router(faq_router)
app.include_router(staff_router)
app.include_router(audit_router)
app.include_router(vector_router)
app.include_router(staff_console_router)

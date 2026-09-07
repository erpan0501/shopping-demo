"""不保存密钥的内部客服工作台页面。"""

from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import FileResponse


router = APIRouter(prefix="/internal/console", include_in_schema=False)
_STATIC_DIR = Path(__file__).resolve().parents[1] / "static"


@router.get("")
def staff_console() -> FileResponse:
    return FileResponse(
        _STATIC_DIR / "staff-console.html",
        headers={
            "Cache-Control": "no-store",
            "X-Frame-Options": "DENY",
            "Content-Security-Policy": (
                "default-src 'self'; connect-src 'self'; "
                "script-src 'self'; style-src 'self'; base-uri 'none'; frame-ancestors 'none'"
            ),
        },
    )

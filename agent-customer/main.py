import uvicorn

from app.config import get_settings


def main() -> None:
    settings = get_settings()
    uvicorn.run("app.main:app", host="127.0.0.1", port=settings.agent_port, reload=False)


if __name__ == "__main__":
    main()

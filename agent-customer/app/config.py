from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "智能客服"
    java_base_url: str = "http://127.0.0.1:8080"
    java_timeout_seconds: float = 10.0
    java_retry_attempts: int = Field(default=3, ge=1, le=5)
    java_retry_delay_seconds: float = Field(default=0.15, ge=0.0, le=5.0)
    java_circuit_failure_threshold: int = Field(default=5, ge=1, le=100)
    java_circuit_recovery_seconds: int = Field(default=30, ge=1, le=3600)
    chat_rate_limit_max_requests: int = Field(default=30, ge=1, le=1000)
    chat_rate_limit_window_seconds: int = Field(default=60, ge=1, le=3600)
    rate_limit_backend: Literal["memory", "redis"] = "memory"
    rate_limit_redis_key_prefix: str = "mall-customer-service:rate-limit"
    allow_test_user_id: bool = True
    agent_port: int = 8000
    handoff_db_path: Path = Path("data/customer_service.db")
    audit_db_path: Path = Path("data/customer_service.db")
    staff_api_key: str | None = None
    # 保持现有本地启动可用；部署环境须在 .env 中显式设为 redis。
    session_backend: Literal["redis", "memory"] = "memory"
    redis_url: str = "redis://127.0.0.1:6379/0"
    redis_key_prefix: str = "mall-customer-service:session"
    session_ttl_seconds: int = Field(default=1800, ge=60)
    session_history_max_messages: int = Field(default=10, ge=2, le=100)
    # FAQ 向量检索默认关闭，保留 Java FAQ 的稳定主链路。
    faq_retrieval_backend: Literal["java", "qdrant"] = "java"
    faq_qdrant_url: str = "http://127.0.0.1:6333"
    faq_qdrant_collection: str = "mall_faq"
    # 以 text-embedding-v4 的语义分数和字面重排联合校准。
    faq_vector_score_threshold: float = Field(default=0.62, ge=0.0, le=1.0)
    embedding_base_url: str | None = None
    embedding_api_key: str | None = None
    embedding_model: str = "text-embedding-v4"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
    deepseek_api_key: str
    deepseek_model: str = "deepseek-v4-flash"

@lru_cache
def get_settings() -> Settings:
    return Settings()

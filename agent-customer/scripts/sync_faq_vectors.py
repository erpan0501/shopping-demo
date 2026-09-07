"""从 Java FAQ 接口读取已启用 FAQ，并同步至 Qdrant。"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

# 支持从项目根目录直接执行 `uv run python scripts/sync_faq_vectors.py`。
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.config import get_settings
from app.java_client import JavaClient
from app.service.faq_vector_service import QdrantFaqRetriever
from app.service.faq_vector_sync_service import FaqVectorSyncService


async def main() -> None:
    settings = get_settings()
    if settings.faq_retrieval_backend != "qdrant":
        raise RuntimeError("请先设置 FAQ_RETRIEVAL_BACKEND=qdrant")

    retriever = QdrantFaqRetriever(settings)
    summary = await FaqVectorSyncService(JavaClient(settings), retriever).sync()
    print(
        f"已从 Java 读取 {summary.source_count} 条启用 FAQ，"
        f"同步 {summary.indexed_count} 条到 {settings.faq_qdrant_collection}，"
        f"清理 {summary.removed_count} 条已下线向量。"
    )


if __name__ == "__main__":
    asyncio.run(main())

"""FAQ 向量索引的受控同步流程。"""

from __future__ import annotations

from dataclasses import dataclass

from ..java_client import JavaClient
from ..models import Faq
from .faq_vector_service import QdrantFaqRetriever, VectorFaqSyncResult


@dataclass(frozen=True)
class FaqVectorSyncSummary:
    source_count: int
    indexed_count: int
    removed_count: int


class FaqVectorSyncService:
    """从 Java 读取所有启用 FAQ，再同步至 Qdrant。"""

    def __init__(
        self,
        java_client: JavaClient,
        vector_retriever: QdrantFaqRetriever,
    ) -> None:
        self._java_client = java_client
        self._vector_retriever = vector_retriever

    async def sync(self) -> FaqVectorSyncSummary:
        faqs = await self._load_enabled_faqs()
        result: VectorFaqSyncResult = await self._vector_retriever.sync_with_result(faqs)
        return FaqVectorSyncSummary(
            source_count=len(faqs),
            indexed_count=result.indexed_count,
            removed_count=result.removed_count,
        )

    async def _load_enabled_faqs(self) -> list[Faq]:
        faqs: list[Faq] = []
        page = 1
        while True:
            result = await self._java_client.search_faq(page=page, size=100)
            faqs.extend(faq for faq in result.records if faq.status == 1)
            if page >= result.pages:
                return faqs
            page += 1

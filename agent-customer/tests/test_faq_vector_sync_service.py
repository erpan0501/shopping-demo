import unittest

from app.models import Faq, FaqPage
from app.service.faq_vector_service import VectorFaqSyncResult
from app.service.faq_vector_sync_service import FaqVectorSyncService


class _PagedJavaClient:
    def __init__(self) -> None:
        self.calls: list[int] = []

    async def search_faq(self, *, page: int, size: int) -> FaqPage:
        self.calls.append(page)
        if page == 1:
            return FaqPage(
                records=[
                    Faq(id="enabled-1", question="问题一", answer="答案一", status=1),
                    Faq(id="disabled", question="旧问题", answer="旧答案", status=0),
                ],
                pages=2,
            )
        return FaqPage(
            records=[Faq(id="enabled-2", question="问题二", answer="答案二", status=1)],
            pages=2,
        )


class _VectorRetriever:
    def __init__(self) -> None:
        self.faqs: list[Faq] = []

    async def sync_with_result(self, faqs: list[Faq]) -> VectorFaqSyncResult:
        self.faqs = faqs
        return VectorFaqSyncResult(indexed_count=len(faqs), removed_count=1)


class FaqVectorSyncServiceTests(unittest.IsolatedAsyncioTestCase):
    async def test_sync_reads_all_pages_and_only_enabled_faqs(self) -> None:
        java_client = _PagedJavaClient()
        vector_retriever = _VectorRetriever()

        summary = await FaqVectorSyncService(  # type: ignore[arg-type]
            java_client,
            vector_retriever,
        ).sync()

        self.assertEqual(java_client.calls, [1, 2])
        self.assertEqual([faq.id for faq in vector_retriever.faqs], ["enabled-1", "enabled-2"])
        self.assertEqual(summary.source_count, 2)
        self.assertEqual(summary.indexed_count, 2)
        self.assertEqual(summary.removed_count, 1)

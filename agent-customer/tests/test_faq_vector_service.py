import unittest

from app.config import Settings
from app.models import Faq
from app.service.faq_service import FaqService
from app.service.faq_vector_service import QdrantFaqRetriever, normalize_faq_text


class _JavaWithoutAnswer:
    async def get_faq_answer(self, question: str):
        return None


class _VectorWithAnswer:
    async def find_answer(self, question: str):
        return "向量检索答案"


def _vector_settings() -> Settings:
    """为网络完全隔离的向量检索测试提供虚拟配置。"""
    return Settings(
        deepseek_api_key="test",
        embedding_base_url="https://embedding.invalid/v1",
        embedding_api_key="test",
    )


class FaqVectorServiceTests(unittest.IsolatedAsyncioTestCase):
    def test_normalizer_unifies_common_customer_phrases(self) -> None:
        self.assertEqual(normalize_faq_text("商城支持哪些付款方式？"), "商城支持哪些支付方式")
        self.assertEqual(normalize_faq_text("在哪查订单啊"), "如何查询我的订单啊")

    async def test_java_miss_falls_back_to_vector_retriever(self) -> None:
        service = FaqService(_JavaWithoutAnswer(), _VectorWithAnswer())
        self.assertEqual(await service.get_answer("口语化问题"), "向量检索答案")

    def test_reranking_combines_semantic_and_lexical_scores(self) -> None:
        retriever = QdrantFaqRetriever(_vector_settings())
        match = retriever._rerank(
            "商城支持哪些支付方式",
            [
                {"score": 0.80, "payload": {"normalized_question": "商城支持哪些支付方式", "answer": "支付方式答案"}},
                {"score": 0.85, "payload": {"normalized_question": "忘记密码怎么办", "answer": "密码答案"}},
            ],
        )
        self.assertIsNotNone(match)
        self.assertEqual(match.answer, "支付方式答案")

    async def test_sync_batches_embeddings_in_groups_of_ten(self) -> None:
        retriever = QdrantFaqRetriever(_vector_settings())
        batches: list[int] = []
        requests: list[dict] = []

        async def embed(texts: list[str]) -> list[list[float]]:
            batches.append(len(texts))
            return [[0.1, 0.2] for _ in texts]

        async def ensure_collection(_: int) -> None:
            return None

        async def get_point_ids() -> set[str]:
            return {"0", "retired"}

        async def request(*_: object, json: dict | None = None, **__: object) -> dict:
            if json is not None:
                requests.append(json)
            return {}

        retriever._embedder.embed = embed  # type: ignore[method-assign]
        retriever._ensure_collection = ensure_collection  # type: ignore[method-assign]
        retriever._get_point_ids = get_point_ids  # type: ignore[method-assign]
        retriever._request = request  # type: ignore[method-assign]
        faqs = [
            Faq(id=str(index), question=f"问题 {index}", answer=f"答案 {index}")
            for index in range(11)
        ]

        self.assertEqual(await retriever.sync(faqs), 11)
        self.assertEqual(batches, [10, 1])
        self.assertEqual(len(requests[0]["points"]), 11)
        self.assertEqual(requests[1], {"points": ["retired"]})


if __name__ == "__main__":
    unittest.main()

from ..java_client import JavaClient
from ..models import FaqPage
from .faq_vector_service import QdrantFaqRetriever

class FaqService:
    def __init__(
        self,
        java_client: JavaClient,
        vector_retriever: QdrantFaqRetriever | None = None,
    ):
        self.java_client = java_client
        self.vector_retriever = vector_retriever

    async def search_faq(
        self,
        page: int = 1,
        size: int = 20,
        category_id: int | None = None,
    ) -> FaqPage:
        return await self.java_client.search_faq(
            page=page,
            size=size,
            category_id=category_id,
        )

    async def get_answer(self, question: str) -> str | None:
        answer = await self.java_client.get_faq_answer(question)
        if answer or self.vector_retriever is None:
            return answer
        return await self.vector_retriever.find_answer(question)

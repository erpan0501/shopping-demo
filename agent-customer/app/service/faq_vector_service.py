"""可选的 Qdrant FAQ 检索层。

向量由外部、OpenAI 兼容的 embeddings 服务生成；本模块不把 API 密钥或 FAQ 正文写入日志。
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from difflib import SequenceMatcher
from typing import Any

import httpx

from ..config import Settings
from ..models import Faq

logger = logging.getLogger(__name__)


class FaqVectorError(RuntimeError):
    """向量服务或 Qdrant 不可用。"""


@dataclass(frozen=True)
class VectorFaqMatch:
    answer: str
    score: float


@dataclass(frozen=True)
class VectorFaqSyncResult:
    indexed_count: int
    removed_count: int


def normalize_faq_text(text: str) -> str:
    """统一常见客服口语表达，用于入库、查询与轻量重排序。"""
    normalized = re.sub(r"[\s，。！？、；：‘’“”'\"()（）【】\-—_]", "", text.lower())
    aliases = (
        ("付款方式", "支付方式"),
        ("付款", "支付"),
        ("发货要多久", "订单多久可以发货"),
        ("几天发货", "订单多久可以发货"),
        ("怎么查订单", "如何查询我的订单"),
        ("在哪查订单", "如何查询我的订单"),
        ("人工客服", "联系人工客服"),
    )
    for source, target in aliases:
        normalized = normalized.replace(source, target)
    return normalized


class OpenAICompatibleEmbedder:
    def __init__(self, settings: Settings) -> None:
        self._base_url = (settings.embedding_base_url or "").rstrip("/")
        self._api_key = settings.embedding_api_key
        self._model = settings.embedding_model

    @property
    def configured(self) -> bool:
        return bool(self._base_url and self._api_key)

    async def embed(self, texts: list[str]) -> list[list[float]]:
        if not self.configured:
            raise FaqVectorError("未配置 EMBEDDING_BASE_URL 或 EMBEDDING_API_KEY")
        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                response = await client.post(
                    f"{self._base_url}/embeddings",
                    headers={"Authorization": f"Bearer {self._api_key}"},
                    json={
                        "model": self._model,
                        "input": texts,
                        "encoding_format": "float",
                    },
                )
                response.raise_for_status()
                data = response.json().get("data", [])
        except (httpx.HTTPError, ValueError) as exc:
            raise FaqVectorError("嵌入服务请求失败") from exc

        try:
            vectors = [item["embedding"] for item in sorted(data, key=lambda item: item["index"])]
        except (KeyError, TypeError):
            raise FaqVectorError("嵌入服务返回格式不符合约定") from None
        if len(vectors) != len(texts) or not all(isinstance(vector, list) for vector in vectors):
            raise FaqVectorError("嵌入服务未返回完整向量")
        return vectors


class QdrantFaqRetriever:
    def __init__(self, settings: Settings) -> None:
        self._qdrant_url = settings.faq_qdrant_url.rstrip("/")
        self._collection = settings.faq_qdrant_collection
        self._threshold = settings.faq_vector_score_threshold
        self._embedder = OpenAICompatibleEmbedder(settings)

    @property
    def configured(self) -> bool:
        return self._embedder.configured

    async def find_answer(self, question: str) -> str | None:
        if not self.configured:
            logger.warning("faq_vector_lookup_skipped reason=embedding_not_configured")
            return None
        try:
            query = normalize_faq_text(question)
            vector = (await self._embedder.embed([query]))[0]
            points = await self._query(vector)
            match = self._rerank(query, points)
            return match.answer if match and match.score >= self._threshold else None
        except FaqVectorError:
            logger.exception("faq_vector_lookup_failed")
            return None

    async def sync(self, faqs: list[Faq]) -> int:
        """兼容原有脚本调用，仅返回本次写入的 FAQ 数量。"""
        return (await self.sync_with_result(faqs)).indexed_count

    async def sync_with_result(self, faqs: list[Faq]) -> VectorFaqSyncResult:
        """写入启用 FAQ，并删除已在 Java 侧下线的旧向量。"""
        if not self.configured:
            raise FaqVectorError("向量同步需要配置嵌入服务")
        if not faqs:
            collection = await self._request(
                "GET",
                f"/collections/{self._collection}",
                allow_not_found=True,
            )
            if collection is None:
                return VectorFaqSyncResult(indexed_count=0, removed_count=0)
            removed_ids = await self._get_point_ids()
            if removed_ids:
                await self._request(
                    "POST",
                    f"/collections/{self._collection}/points/delete?wait=true",
                    json={"points": sorted(removed_ids)},
                )
            return VectorFaqSyncResult(indexed_count=0, removed_count=len(removed_ids))
        texts = [normalize_faq_text(faq.question) for faq in faqs]
        # text-embedding-v4 的批量输入上限为 10 条；分批可兼容该限制，
        # 也避免未来 FAQ 数量增长后一次同步失败。
        vectors: list[list[float]] = []
        for start in range(0, len(texts), 10):
            vectors.extend(await self._embedder.embed(texts[start : start + 10]))
        await self._ensure_collection(len(vectors[0]))
        points = [
            {
                "id": faq.id,
                "vector": vector,
                "payload": {
                    "faq_id": faq.id,
                    "question": faq.question,
                    "normalized_question": text,
                    "answer": faq.answer,
                    "category_id": faq.category_id,
                },
            }
            for faq, text, vector in zip(faqs, texts, vectors, strict=True)
        ]
        existing_ids = await self._get_point_ids()
        await self._request(
            "PUT",
            f"/collections/{self._collection}/points?wait=true",
            json={"points": points},
        )
        removed_ids = existing_ids.difference(str(faq.id) for faq in faqs)
        if removed_ids:
            await self._request(
                "POST",
                f"/collections/{self._collection}/points/delete?wait=true",
                json={"points": sorted(removed_ids)},
            )
        return VectorFaqSyncResult(
            indexed_count=len(points),
            removed_count=len(removed_ids),
        )

    async def _ensure_collection(self, vector_size: int) -> None:
        response = await self._request(
            "GET",
            f"/collections/{self._collection}",
            allow_not_found=True,
        )
        if response is not None:
            return
        await self._request(
            "PUT",
            f"/collections/{self._collection}",
            json={"vectors": {"size": vector_size, "distance": "Cosine"}},
        )

    async def _query(self, vector: list[float]) -> list[dict[str, Any]]:
        payload = await self._request(
            "POST",
            f"/collections/{self._collection}/points/query",
            json={"query": vector, "limit": 5, "with_payload": True},
        )
        result = payload.get("result", payload) if isinstance(payload, dict) else {}
        points = result.get("points", []) if isinstance(result, dict) else []
        return points if isinstance(points, list) else []

    async def _get_point_ids(self) -> set[str]:
        payload = await self._request(
            "POST",
            f"/collections/{self._collection}/points/scroll",
            json={"limit": 10_000, "with_payload": False, "with_vector": False},
        )
        result = payload.get("result", payload) if isinstance(payload, dict) else {}
        points = result.get("points", []) if isinstance(result, dict) else []
        if not isinstance(points, list):
            return set()
        return {
            str(point["id"])
            for point in points
            if isinstance(point, dict) and point.get("id") is not None
        }

    def _rerank(self, query: str, points: list[dict[str, Any]]) -> VectorFaqMatch | None:
        best: VectorFaqMatch | None = None
        for point in points:
            payload = point.get("payload", {})
            if not isinstance(payload, dict):
                continue
            answer = payload.get("answer")
            candidate = payload.get("normalized_question") or payload.get("question")
            if not isinstance(answer, str) or not isinstance(candidate, str):
                continue
            semantic_score = float(point.get("score", 0.0))
            lexical_score = SequenceMatcher(None, query, normalize_faq_text(candidate)).ratio()
            score = semantic_score * 0.8 + lexical_score * 0.2
            if best is None or score > best.score:
                best = VectorFaqMatch(answer=answer, score=score)
        return best

    async def _request(
        self,
        method: str,
        path: str,
        *,
        json: dict[str, Any] | None = None,
        allow_not_found: bool = False,
    ) -> dict[str, Any] | None:
        try:
            async with httpx.AsyncClient(base_url=self._qdrant_url, timeout=10.0) as client:
                response = await client.request(method, path, json=json)
        except httpx.HTTPError as exc:
            raise FaqVectorError("Qdrant 服务不可用") from exc
        if allow_not_found and response.status_code == 404:
            return None
        if response.is_error:
            raise FaqVectorError(f"Qdrant 请求失败（HTTP {response.status_code}）")
        try:
            payload = response.json()
        except ValueError as exc:
            raise FaqVectorError("Qdrant 返回格式不符合约定") from exc
        return payload if isinstance(payload, dict) else {}

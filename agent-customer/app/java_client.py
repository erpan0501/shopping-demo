"""Java 商城接口的受控客户端。"""

from __future__ import annotations

import asyncio
from collections.abc import Callable, Mapping
from math import ceil
from time import monotonic
from typing import Any

import httpx
from pydantic import ValidationError

from .config import Settings
from .models import (
    FaqPage,
    JavaCurrentUserResult,
    JavaFaqResult,
    JavaOrderResult,
    JavaOrdersResult,
    JavaResult,
    ShoppingOrder,
)


class JavaApiError(RuntimeError):
    """Java 服务不可用、返回业务错误或返回体不符合约定时抛出。"""

    def __init__(
        self,
        message: str,
        *,
        status_code: int | None = None,
        business_code: int | None = None,
        retryable: bool = False,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.business_code = business_code
        self.retryable = retryable


class JavaCircuitOpenError(JavaApiError):
    """Java 服务持续失败时快速失败，避免持续耗尽聊天请求的等待时间。"""

    def __init__(self, retry_after_seconds: int) -> None:
        super().__init__("商城服务正在恢复，请稍后再试。", retryable=True)
        self.retry_after_seconds = retry_after_seconds


class JavaClient:
    """仅调用固定 GET 接口；瞬时网络错误和 5xx 会有限重试。"""

    _RETRYABLE_STATUS_CODES = {429, 500, 502, 503, 504}

    def __init__(
        self,
        settings: Settings,
        *,
        transport: httpx.AsyncBaseTransport | None = None,
        clock: Callable[[], float] = monotonic,
    ) -> None:
        self._base_url = settings.java_base_url.rstrip("/")
        self._timeout = settings.java_timeout_seconds
        self._retry_attempts = settings.java_retry_attempts
        self._retry_delay_seconds = settings.java_retry_delay_seconds
        self._circuit_failure_threshold = settings.java_circuit_failure_threshold
        self._circuit_recovery_seconds = settings.java_circuit_recovery_seconds
        self._transport = transport
        self._clock = clock
        self._circuit_failures = 0
        self._circuit_opened_until = 0.0
        self._circuit_lock = asyncio.Lock()

    async def search_faq(
        self,
        *,
        page: int = 1,
        size: int = 20,
        category_id: int | None = None,
    ) -> FaqPage:
        params: dict[str, int] = {"page": page, "size": size}
        if category_id is not None:
            params["categoryId"] = category_id

        payload = await self._get_json("/faq/search", params=params)
        result = self._validate(JavaResult, payload, "Java FAQ 列表接口")
        if result.code != 200:
            raise self._business_error(result.code, result.message)
        if result.data is None:
            raise JavaApiError("Java FAQ 接口没有返回 data")
        return result.data

    async def get_faq_answer(self, question: str) -> str | None:
        """调用 Java `/faq/answer`，返回匹配到的答案文本。"""
        if not question or not question.strip():
            raise JavaApiError("question 不能为空")

        payload = await self._get_json("/faq/answer", params={"question": question})
        result = self._validate(JavaFaqResult, payload, "Java FAQ 匹配接口")
        if result.code != 200:
            raise self._business_error(result.code, result.message)
        return result.data.answer if result.data else None

    async def get_user_orders(
        self,
        user_id: int,
        status: int | None = None,
    ) -> list[ShoppingOrder]:
        if user_id <= 0:
            raise JavaApiError("user_id 必须大于 0")

        params: dict[str, int] = {}
        if status is not None:
            params["status"] = status
        payload = await self._get_json(
            "/user/orders/findUserOrders",
            params=params,
            headers={"userId": str(user_id)},
        )
        result = self._validate(JavaOrdersResult, payload, "Java 订单列表接口")
        if result.code != 200:
            raise self._business_error(result.code, result.message)
        return result.data

    async def get_order_by_id(
        self,
        user_id: int,
        order_id: str,
    ) -> ShoppingOrder | None:
        if user_id <= 0:
            raise JavaApiError("user_id 必须大于 0")
        if not order_id or not order_id.strip():
            raise JavaApiError("order_id 不能为空")

        payload = await self._get_json(
            "/user/orders/findById",
            params={"id": order_id},
            headers={"userId": str(user_id)},
        )
        result = self._validate(JavaOrderResult, payload, "Java 订单详情接口")
        if result.code != 200:
            raise self._business_error(result.code, result.message)
        return result.data

    async def get_current_user_id(self, authorization: str) -> int | None:
        if not authorization.startswith("Bearer "):
            return None
        payload = await self._get_json(
            "/user/shoppingUser/auth/current",
            headers={"Authorization": authorization},
        )
        result = self._validate(
            JavaCurrentUserResult,
            payload,
            "Java 用户身份接口",
        )
        if result.code != 200:
            raise self._business_error(result.code, result.message)
        return result.data

    async def _get_json(
        self,
        path: str,
        *,
        params: Mapping[str, Any] | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Any:
        response = await self._request("GET", path, params=params, headers=headers)
        try:
            return response.json()
        except ValueError as exc:
            raise JavaApiError(
                "Java 服务返回了无法解析的数据",
                status_code=response.status_code,
            ) from exc

    async def _request(
        self,
        method: str,
        path: str,
        *,
        params: Mapping[str, Any] | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> httpx.Response:
        await self._ensure_circuit_available()
        last_error: JavaApiError | None = None
        for attempt in range(1, self._retry_attempts + 1):
            try:
                async with httpx.AsyncClient(
                    base_url=self._base_url,
                    timeout=self._timeout,
                    transport=self._transport,
                ) as client:
                    response = await client.request(
                        method,
                        path,
                        params=params,
                        headers=headers,
                    )
            except httpx.RequestError as exc:
                last_error = JavaApiError(
                    "Java 服务网络连接失败",
                    retryable=True,
                )
            else:
                if response.status_code < 400:
                    await self._record_circuit_success()
                    return response
                retryable = response.status_code in self._RETRYABLE_STATUS_CODES
                last_error = JavaApiError(
                    f"Java 服务请求失败（HTTP {response.status_code}）",
                    status_code=response.status_code,
                    retryable=retryable,
                )
                if not retryable:
                    raise last_error

            if attempt < self._retry_attempts:
                await asyncio.sleep(
                    self._retry_delay_seconds * (2 ** (attempt - 1)),
                )

        assert last_error is not None
        await self._record_circuit_failure()
        raise last_error

    async def _ensure_circuit_available(self) -> None:
        now = self._clock()
        async with self._circuit_lock:
            if self._circuit_opened_until <= now:
                if self._circuit_opened_until:
                    self._circuit_opened_until = 0.0
                    self._circuit_failures = 0
                return
            raise JavaCircuitOpenError(
                max(1, ceil(self._circuit_opened_until - now)),
            )

    async def _record_circuit_success(self) -> None:
        async with self._circuit_lock:
            self._circuit_failures = 0
            self._circuit_opened_until = 0.0

    async def _record_circuit_failure(self) -> None:
        async with self._circuit_lock:
            self._circuit_failures += 1
            if self._circuit_failures >= self._circuit_failure_threshold:
                self._circuit_opened_until = (
                    self._clock() + self._circuit_recovery_seconds
                )

    @staticmethod
    def _validate(model_type: type[Any], payload: Any, endpoint_name: str) -> Any:
        try:
            return model_type.model_validate(payload)
        except ValidationError as exc:
            raise JavaApiError(f"{endpoint_name}返回格式不符合约定") from exc

    @staticmethod
    def _business_error(code: int, message: str | None) -> JavaApiError:
        return JavaApiError(
            message or f"Java API 业务错误 code={code}",
            business_code=code,
        )

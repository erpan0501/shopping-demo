import unittest

import httpx

from app.config import Settings
from app.java_client import JavaApiError, JavaCircuitOpenError, JavaClient


def settings(**overrides) -> Settings:
    return Settings(
        deepseek_api_key="test",
        java_retry_delay_seconds=0,
        **overrides,
    )


def faq_payload() -> dict[str, object]:
    return {
        "code": 200,
        "message": "OK",
        "data": {
            "id": "faq-1",
            "question": "如何查询订单？",
            "answer": "进入我的订单查看。",
            "status": 1,
        },
    }


class JavaClientTests(unittest.IsolatedAsyncioTestCase):
    async def test_opens_circuit_after_consecutive_transient_failures(self) -> None:
        clock = [0.0]
        calls = 0

        def handler(request: httpx.Request) -> httpx.Response:
            nonlocal calls
            calls += 1
            return httpx.Response(503, request=request)

        client = JavaClient(
            settings(
                java_retry_attempts=1,
                java_circuit_failure_threshold=2,
                java_circuit_recovery_seconds=30,
            ),
            transport=httpx.MockTransport(handler),
            clock=lambda: clock[0],
        )

        with self.assertRaises(JavaApiError):
            await client.get_faq_answer("如何查询订单？")
        with self.assertRaises(JavaApiError):
            await client.get_faq_answer("如何查询订单？")
        with self.assertRaises(JavaCircuitOpenError) as context:
            await client.get_faq_answer("如何查询订单？")

        self.assertEqual(calls, 2)
        self.assertEqual(context.exception.retry_after_seconds, 30)

    async def test_retries_transient_http_error_then_returns_answer(self) -> None:
        calls = 0

        def handler(request: httpx.Request) -> httpx.Response:
            nonlocal calls
            calls += 1
            if calls == 1:
                return httpx.Response(503, request=request)
            return httpx.Response(200, json=faq_payload(), request=request)

        client = JavaClient(settings(), transport=httpx.MockTransport(handler))

        answer = await client.get_faq_answer("如何查询订单？")

        self.assertEqual(answer, "进入我的订单查看。")
        self.assertEqual(calls, 2)

    async def test_does_not_retry_non_transient_http_error(self) -> None:
        calls = 0

        def handler(request: httpx.Request) -> httpx.Response:
            nonlocal calls
            calls += 1
            return httpx.Response(400, request=request)

        client = JavaClient(settings(), transport=httpx.MockTransport(handler))

        with self.assertRaises(JavaApiError) as context:
            await client.get_faq_answer("如何查询订单？")

        self.assertEqual(calls, 1)
        self.assertEqual(context.exception.status_code, 400)
        self.assertFalse(context.exception.retryable)

    async def test_retries_network_error(self) -> None:
        calls = 0

        def handler(request: httpx.Request) -> httpx.Response:
            nonlocal calls
            calls += 1
            if calls < 3:
                raise httpx.ConnectError("connection refused", request=request)
            return httpx.Response(200, json=faq_payload(), request=request)

        client = JavaClient(settings(), transport=httpx.MockTransport(handler))

        self.assertEqual(
            await client.get_faq_answer("如何查询订单？"),
            "进入我的订单查看。",
        )
        self.assertEqual(calls, 3)

    async def test_exposes_java_business_error_code(self) -> None:
        def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(
                200,
                json={"code": 5001, "message": "订单不存在", "data": None},
                request=request,
            )

        client = JavaClient(settings(), transport=httpx.MockTransport(handler))

        with self.assertRaises(JavaApiError) as context:
            await client.get_faq_answer("如何查询订单？")

        self.assertEqual(context.exception.business_code, 5001)
        self.assertEqual(str(context.exception), "订单不存在")

    async def test_resolves_user_id_from_java_identity_endpoint(self) -> None:
        def handler(request: httpx.Request) -> httpx.Response:
            self.assertEqual(request.url.path, "/user/shoppingUser/auth/current")
            self.assertEqual(request.headers["Authorization"], "Bearer token")
            return httpx.Response(
                200,
                json={"code": 200, "message": "OK", "data": 1},
                request=request,
            )

        client = JavaClient(settings(), transport=httpx.MockTransport(handler))

        self.assertEqual(await client.get_current_user_id("Bearer token"), 1)
        self.assertIsNone(await client.get_current_user_id("token"))


if __name__ == "__main__":
    unittest.main()

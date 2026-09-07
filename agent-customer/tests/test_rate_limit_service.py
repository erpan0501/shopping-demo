import unittest

from app.service.rate_limit_service import RateLimitExceeded, SlidingWindowRateLimiter


class MutableClock:
    def __init__(self) -> None:
        self.value = 0.0

    def __call__(self) -> float:
        return self.value


class SlidingWindowRateLimiterTests(unittest.IsolatedAsyncioTestCase):
    async def test_rejects_requests_over_limit_and_reports_retry_after(self) -> None:
        clock = MutableClock()
        limiter = SlidingWindowRateLimiter(
            max_requests=2,
            window_seconds=10,
            clock=clock,
        )

        await limiter.check("user:1")
        await limiter.check("user:1")

        with self.assertRaises(RateLimitExceeded) as context:
            await limiter.check("user:1")

        self.assertEqual(context.exception.retry_after_seconds, 10)

    async def test_window_expiry_allows_new_request(self) -> None:
        clock = MutableClock()
        limiter = SlidingWindowRateLimiter(
            max_requests=1,
            window_seconds=10,
            clock=clock,
        )

        await limiter.check("user:1")
        clock.value = 10.0
        await limiter.check("user:1")

    async def test_different_users_have_independent_limits(self) -> None:
        limiter = SlidingWindowRateLimiter(max_requests=1, window_seconds=10)

        await limiter.check("user:1")
        await limiter.check("user:2")


if __name__ == "__main__":
    unittest.main()

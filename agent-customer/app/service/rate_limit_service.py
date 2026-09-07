"""内存和 Redis 两种滑动窗口限流实现。"""

from __future__ import annotations

import asyncio
import secrets
from collections import defaultdict, deque
from collections.abc import Callable
from math import ceil
from time import monotonic
from typing import Protocol

import redis.asyncio as redis

from ..config import Settings


class RateLimitExceeded(RuntimeError):
    def __init__(self, retry_after_seconds: int) -> None:
        super().__init__("请求频率超过限制")
        self.retry_after_seconds = retry_after_seconds


class RateLimitStoreUnavailable(RuntimeError):
    """Redis 限流存储不可用，调用方应返回受控错误而不是绕过限流。"""


class RateLimiter(Protocol):
    async def check(self, key: str) -> None: ...

    async def aclose(self) -> None: ...


class SlidingWindowRateLimiter:
    def __init__(
        self,
        *,
        max_requests: int,
        window_seconds: int,
        clock: Callable[[], float] = monotonic,
    ) -> None:
        self._max_requests = max_requests
        self._window_seconds = window_seconds
        self._clock = clock
        self._requests: dict[str, deque[float]] = defaultdict(deque)
        self._lock = asyncio.Lock()

    async def check(self, key: str) -> None:
        now = self._clock()
        cutoff = now - self._window_seconds
        async with self._lock:
            timestamps = self._requests[key]
            while timestamps and timestamps[0] <= cutoff:
                timestamps.popleft()

            if len(timestamps) >= self._max_requests:
                retry_after = max(1, ceil(timestamps[0] + self._window_seconds - now))
                raise RateLimitExceeded(retry_after)

            timestamps.append(now)

    async def aclose(self) -> None:
        return None


class RedisSlidingWindowRateLimiter:
    """通过一段 Lua 脚本原子执行 Redis ZSET 滑动窗口。"""

    _CHECK_SCRIPT = """
local key = KEYS[1]
local now = tonumber(ARGV[1])
local window = tonumber(ARGV[2])
local max_requests = tonumber(ARGV[3])
local member = ARGV[4]
local cutoff = now - window
redis.call('ZREMRANGEBYSCORE', key, 0, cutoff)
local count = redis.call('ZCARD', key)
if count >= max_requests then
  local oldest = redis.call('ZRANGE', key, 0, 0, 'WITHSCORES')[2]
  return {0, math.max(1, math.ceil((tonumber(oldest) + window - now) / 1000))}
end
redis.call('ZADD', key, now, member)
redis.call('PEXPIRE', key, window)
return {1, 0}
"""

    def __init__(
        self,
        *,
        redis_client: redis.Redis,
        max_requests: int,
        window_seconds: int,
        key_prefix: str,
        clock: Callable[[], float] = monotonic,
    ) -> None:
        self._redis = redis_client
        self._max_requests = max_requests
        self._window_ms = window_seconds * 1000
        self._key_prefix = key_prefix.rstrip(":")
        self._clock = clock

    async def check(self, key: str) -> None:
        now_ms = int(self._clock() * 1000)
        try:
            result = await self._redis.eval(
                self._CHECK_SCRIPT,
                1,
                f"{self._key_prefix}:{key}",
                now_ms,
                self._window_ms,
                self._max_requests,
                f"{now_ms}:{secrets.token_urlsafe(8)}",
            )
        except redis.RedisError as exc:
            raise RateLimitStoreUnavailable("Redis 限流存储不可用") from exc

        if not isinstance(result, (list, tuple)) or len(result) != 2:
            raise RateLimitStoreUnavailable("Redis 限流脚本返回异常")
        if int(result[0]) == 0:
            raise RateLimitExceeded(int(result[1]))

    async def aclose(self) -> None:
        await self._redis.aclose()


def create_rate_limiter(settings: Settings) -> RateLimiter:
    if settings.rate_limit_backend == "redis":
        return RedisSlidingWindowRateLimiter(
            redis_client=redis.from_url(settings.redis_url, decode_responses=False),
            max_requests=settings.chat_rate_limit_max_requests,
            window_seconds=settings.chat_rate_limit_window_seconds,
            key_prefix=settings.rate_limit_redis_key_prefix,
        )
    return SlidingWindowRateLimiter(
        max_requests=settings.chat_rate_limit_max_requests,
        window_seconds=settings.chat_rate_limit_window_seconds,
    )

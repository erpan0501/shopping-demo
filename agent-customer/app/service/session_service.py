"""客服会话存储。

生产环境使用 Redis，以便多进程、多节点共享会话；本地开发可显式使用
``SESSION_BACKEND=memory``。会话中的订单号等敏感内容不得写入应用日志。
"""

from __future__ import annotations

import json
from collections import defaultdict
from typing import Protocol

from redis.asyncio import Redis

from ..config import Settings


History = list[tuple[str, str]]


class SessionStore(Protocol):
    async def get_history(self, session_id: str) -> History: ...

    async def add_message(self, session_id: str, role: str, content: str) -> None: ...

    async def set_pending_action(self, session_id: str, action: str) -> None: ...

    async def get_pending_action(self, session_id: str) -> str | None: ...

    async def clear_pending_action(self, session_id: str) -> None: ...

    async def aclose(self) -> None: ...


class InMemorySessionService:
    """仅用于显式本地开发模式；重启或多实例时状态不会保留。"""

    def __init__(self, *, history_max_messages: int) -> None:
        self.history_max_messages = history_max_messages
        self.histories: dict[str, History] = defaultdict(list)
        self.pending_actions: dict[str, str] = {}

    async def get_history(self, session_id: str) -> History:
        return list(self.histories[session_id])

    async def add_message(self, session_id: str, role: str, content: str) -> None:
        self.histories[session_id].append((role, content))
        self.histories[session_id] = self.histories[session_id][
            -self.history_max_messages :
        ]

    async def set_pending_action(self, session_id: str, action: str) -> None:
        self.pending_actions[session_id] = action

    async def get_pending_action(self, session_id: str) -> str | None:
        return self.pending_actions.get(session_id)

    async def clear_pending_action(self, session_id: str) -> None:
        self.pending_actions.pop(session_id, None)

    async def aclose(self) -> None:
        return None


class RedisSessionService:
    """Redis Hash 存储的会话服务，所有读写都会续期 TTL。"""

    _HISTORY_FIELD = "history"
    _PENDING_ACTION_FIELD = "pending_action"

    _ADD_MESSAGE_SCRIPT = """
local raw_history = redis.call('HGET', KEYS[1], ARGV[1])
local history = {}
if raw_history then
    history = cjson.decode(raw_history)
end
table.insert(history, {ARGV[2], ARGV[3]})
while #history > tonumber(ARGV[4]) do
    table.remove(history, 1)
end
redis.call('HSET', KEYS[1], ARGV[1], cjson.encode(history))
redis.call('EXPIRE', KEYS[1], ARGV[5])
return 1
"""

    def __init__(
        self,
        *,
        redis_url: str,
        key_prefix: str,
        ttl_seconds: int,
        history_max_messages: int,
    ) -> None:
        self._client = Redis.from_url(redis_url, decode_responses=True)
        self._key_prefix = key_prefix
        self._ttl_seconds = ttl_seconds
        self._history_max_messages = history_max_messages

    def _key(self, session_id: str) -> str:
        return f"{self._key_prefix}:{session_id}"

    async def get_history(self, session_id: str) -> History:
        key = self._key(session_id)
        async with self._client.pipeline(transaction=False) as pipe:
            pipe.hget(key, self._HISTORY_FIELD)
            pipe.expire(key, self._ttl_seconds)
            raw_history, _ = await pipe.execute()
        return self._decode_history(raw_history)

    async def add_message(self, session_id: str, role: str, content: str) -> None:
        await self._client.eval(
            self._ADD_MESSAGE_SCRIPT,
            1,
            self._key(session_id),
            self._HISTORY_FIELD,
            role,
            content,
            self._history_max_messages,
            self._ttl_seconds,
        )

    async def set_pending_action(self, session_id: str, action: str) -> None:
        key = self._key(session_id)
        async with self._client.pipeline(transaction=True) as pipe:
            pipe.hset(key, self._PENDING_ACTION_FIELD, action)
            pipe.expire(key, self._ttl_seconds)
            await pipe.execute()

    async def get_pending_action(self, session_id: str) -> str | None:
        key = self._key(session_id)
        async with self._client.pipeline(transaction=False) as pipe:
            pipe.hget(key, self._PENDING_ACTION_FIELD)
            pipe.expire(key, self._ttl_seconds)
            action, _ = await pipe.execute()
        return action

    async def clear_pending_action(self, session_id: str) -> None:
        key = self._key(session_id)
        async with self._client.pipeline(transaction=True) as pipe:
            pipe.hdel(key, self._PENDING_ACTION_FIELD)
            pipe.expire(key, self._ttl_seconds)
            await pipe.execute()

    async def aclose(self) -> None:
        await self._client.aclose()

    @staticmethod
    def _decode_history(raw_history: str | None) -> History:
        if not raw_history:
            return []
        try:
            messages = json.loads(raw_history)
        except json.JSONDecodeError:
            return []
        if not isinstance(messages, list):
            return []
        return [
            (str(message[0]), str(message[1]))
            for message in messages
            if isinstance(message, list) and len(message) == 2
        ]


def create_session_service(settings: Settings) -> SessionStore:
    if settings.session_backend == "memory":
        return InMemorySessionService(
            history_max_messages=settings.session_history_max_messages,
        )
    return RedisSessionService(
        redis_url=settings.redis_url,
        key_prefix=settings.redis_key_prefix,
        ttl_seconds=settings.session_ttl_seconds,
        history_max_messages=settings.session_history_max_messages,
    )

import unittest

from app.service.session_service import (
    InMemorySessionService,
    RedisSessionService,
)


class InMemorySessionServiceTests(unittest.IsolatedAsyncioTestCase):
    async def test_history_is_trimmed_and_pending_action_can_be_cleared(self) -> None:
        store = InMemorySessionService(history_max_messages=2)

        await store.add_message("session-1", "human", "第一条")
        await store.add_message("session-1", "assistant", "第二条")
        await store.add_message("session-1", "human", "第三条")

        self.assertEqual(
            await store.get_history("session-1"),
            [("assistant", "第二条"), ("human", "第三条")],
        )

        await store.set_pending_action("session-1", "after_sale_wait_order")
        self.assertEqual(
            await store.get_pending_action("session-1"),
            "after_sale_wait_order",
        )
        await store.clear_pending_action("session-1")
        self.assertIsNone(await store.get_pending_action("session-1"))


class RedisSessionServiceTests(unittest.TestCase):
    def test_decode_history_rejects_invalid_redis_content(self) -> None:
        self.assertEqual(
            RedisSessionService._decode_history('[["human", "你好"]]'),
            [("human", "你好")],
        )
        self.assertEqual(RedisSessionService._decode_history("not-json"), [])
        self.assertEqual(RedisSessionService._decode_history('{"bad": true}'), [])


if __name__ == "__main__":
    unittest.main()

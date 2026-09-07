import unittest

from app.agent.faq_agent import FaqAgent
from app.llm.intent_classifier import LlmIntentDecision
from app.service.intent_service import IntentService
from app.service.session_service import InMemorySessionService


class StubFaqService:
    def __init__(self, answer: str | None = None) -> None:
        self.answer = answer
        self.questions: list[str] = []

    async def get_answer(self, question: str) -> str | None:
        self.questions.append(question)
        return self.answer


class StubDeepSeekClient:
    async def reply(self, question: str, history: list[tuple[str, str]]) -> str:
        return "模型兜底回复"


class StubIntentClassifier:
    def __init__(self, decision: LlmIntentDecision) -> None:
        self.decision = decision
        self.calls = 0

    async def classify(self, question: str) -> LlmIntentDecision:
        self.calls += 1
        return self.decision


class StubOrderService:
    async def get_order_by_id(self, user_id: int, order_id: str):
        return type("Order", (), {"id": order_id})()

    async def get_order_detail_summary(self, user_id: int, order_id: str) -> str:
        return f"订单详情：{order_id}"

    async def get_orders_summary(self, user_id: int, status: int | None) -> str:
        return f"订单列表：{status}"


class StubHandoffService:
    def __init__(self) -> None:
        self.created: dict[str, object] | None = None

    def create_ticket(self, **kwargs):
        self.created = kwargs
        return type("Ticket", (), {"ticket_id": "CS-TEST"})()


class FaqAgentGraphTests(unittest.IsolatedAsyncioTestCase):
    def _create_agent(
        self,
        *,
        faq_answer: str | None = None,
        classifier_intent: str = "other",
    ) -> tuple[FaqAgent, InMemorySessionService, StubIntentClassifier, StubHandoffService]:
        classifier = StubIntentClassifier(
            LlmIntentDecision(intent=classifier_intent, status=None),
        )
        sessions = InMemorySessionService(history_max_messages=10)
        handoff = StubHandoffService()
        agent = FaqAgent(
            StubFaqService(faq_answer),
            StubDeepSeekClient(),
            sessions,
            StubOrderService(),
            handoff,
            IntentService(classifier),
        )
        return agent, sessions, classifier, handoff

    async def test_faq_result_skips_llm_intent_classification(self) -> None:
        agent, sessions, classifier, _ = self._create_agent(faq_answer="可以支付宝支付。")

        result = await agent.chat("faq-session", "支持什么付款方式", user_id=1)

        self.assertEqual(result.source, "faq")
        self.assertEqual(result.answer, "可以支付宝支付。")
        self.assertEqual(classifier.calls, 0)
        self.assertEqual(len(await sessions.get_history("faq-session")), 2)

    async def test_rule_order_skips_faq_and_llm_classification(self) -> None:
        agent, _, classifier, _ = self._create_agent(faq_answer="不应命中")

        result = await agent.chat("order-session", "帮我查个快递", user_id=1)

        self.assertEqual(result.source, "order")
        self.assertEqual(result.answer, "订单列表：4")
        self.assertEqual(classifier.calls, 0)

    async def test_after_sale_state_spans_multiple_messages(self) -> None:
        agent, sessions, _, _ = self._create_agent(classifier_intent="after_sale")
        order_id = "2087106115733889025"

        first = await agent.chat("after-sale-session", "商品有质量问题", user_id=1)
        second = await agent.chat("after-sale-session", order_id, user_id=1)
        third = await agent.chat("after-sale-session", "我想换货，屏幕有划痕", user_id=1)

        self.assertEqual([first.source, second.source, third.source], ["after_sale"] * 3)
        self.assertIsNone(await sessions.get_pending_action("after-sale-session"))

    async def test_clear_after_sale_request_precedes_semantic_faq(self) -> None:
        agent, _, classifier, _ = self._create_agent(faq_answer="不应进入 FAQ")

        result = await agent.chat("after-sale-rule", "商品坏了，我要申请售后", user_id=1)

        self.assertEqual(result.source, "after_sale")
        self.assertEqual(classifier.calls, 0)

    async def test_after_sale_guide_keeps_faq_path(self) -> None:
        agent, _, classifier, _ = self._create_agent(faq_answer="请在订单中申请售后。")

        result = await agent.chat("after-sale-guide", "如何申请退货？", user_id=1)

        self.assertEqual(result.source, "faq")
        self.assertEqual(classifier.calls, 0)

    async def test_handoff_ticket_receives_current_conversation(self) -> None:
        agent, sessions, _, handoff = self._create_agent()

        result = await agent.chat("handoff-session", "请帮我转人工客服", user_id=1)

        self.assertEqual(result.source, "handoff")
        self.assertIsNotNone(handoff.created)
        self.assertEqual(handoff.created["question"], "请帮我转人工客服")
        self.assertEqual(
            handoff.created["history"],
            [("human", "请帮我转人工客服")],
        )
        self.assertEqual(len(await sessions.get_history("handoff-session")), 2)


if __name__ == "__main__":
    unittest.main()

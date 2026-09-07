import logging
from dataclasses import dataclass
from typing import TypedDict

from langgraph.graph import END, START, StateGraph

from ..llm.deep_seek_client import DeepSeekClient
from ..service.faq_service import FaqService
from ..service.handoff_service import HandoffService
from ..service.intent_service import IntentResult, IntentService, IntentType
from ..service.order_service import OrderService
from ..service.session_service import SessionStore

logger = logging.getLogger(__name__)


@dataclass
class AgentResult:
    matched: bool
    answer: str
    source: str


class CustomerServiceState(TypedDict, total=False):
    session_id: str
    question: str
    user_id: int | None
    pending_action: str | None
    rule_intent: IntentResult
    faq_answer: str | None
    llm_intent: IntentResult
    result: AgentResult


class FaqAgent:
    """由 LangGraph 编排的商城客服 Agent。

    图中的节点只负责一个业务步骤，路由决策保持规则优先：售后续办、人工、
    明确订单问题、FAQ、LLM 意图识别、LLM 受限兜底。
    """

    def __init__(
        self,
        faq_service: FaqService,
        deepseek_client: DeepSeekClient,
        session_service: SessionStore,
        order_service: OrderService,
        handoff_service: HandoffService,
        intent_service: IntentService,
    ) -> None:
        self.faq_service = faq_service
        self.deepseek_client = deepseek_client
        self.session_service = session_service
        self.order_service = order_service
        self.handoff_service = handoff_service
        self.intent_service = intent_service
        self._graph = self._build_graph()

    async def chat(
        self,
        session_id: str,
        question: str,
        user_id: int | None = None,
    ) -> AgentResult:
        final_state = await self._graph.ainvoke(
            {
                "session_id": session_id,
                "question": question,
                "user_id": user_id,
            },
        )
        return final_state["result"]

    def _build_graph(self):
        graph = StateGraph(CustomerServiceState)
        graph.add_node("load_context", self._load_context)
        graph.add_node("after_sale_order", self._after_sale_order)
        graph.add_node("after_sale_description", self._after_sale_description)
        graph.add_node("handoff", self._handoff)
        graph.add_node("rule_order", self._rule_order)
        graph.add_node("faq_lookup", self._faq_lookup)
        graph.add_node("faq_result", self._faq_result)
        graph.add_node("classify_intent", self._classify_intent)
        graph.add_node("start_after_sale", self._start_after_sale)
        graph.add_node("fallback_order", self._fallback_order)
        graph.add_node("llm_reply", self._llm_reply)
        graph.add_node("record_result", self._record_result)

        graph.add_edge(START, "load_context")
        graph.add_conditional_edges(
            "load_context",
            self._route_after_context,
            {
                "after_sale_order": "after_sale_order",
                "after_sale_description": "after_sale_description",
                "handoff": "handoff",
                "start_after_sale": "start_after_sale",
                "rule_order": "rule_order",
                "faq_lookup": "faq_lookup",
            },
        )
        graph.add_edge("after_sale_order", "record_result")
        graph.add_edge("after_sale_description", "record_result")
        graph.add_edge("handoff", END)
        graph.add_edge("rule_order", "record_result")
        graph.add_conditional_edges(
            "faq_lookup",
            self._route_after_faq,
            {"faq_result": "faq_result", "classify_intent": "classify_intent"},
        )
        graph.add_edge("faq_result", "record_result")
        graph.add_conditional_edges(
            "classify_intent",
            self._route_after_classification,
            {
                "start_after_sale": "start_after_sale",
                "fallback_order": "fallback_order",
                "llm_reply": "llm_reply",
            },
        )
        graph.add_edge("start_after_sale", "record_result")
        graph.add_edge("fallback_order", "record_result")
        graph.add_edge("llm_reply", "record_result")
        graph.add_edge("record_result", END)
        return graph.compile(name="mall_customer_service")

    async def _load_context(
        self,
        state: CustomerServiceState,
    ) -> dict[str, object]:
        return {
            "pending_action": await self.session_service.get_pending_action(
                state["session_id"],
            ),
            "rule_intent": self.intent_service.parse(state["question"]),
        }

    @staticmethod
    def _route_after_context(state: CustomerServiceState) -> str:
        intent = state["rule_intent"]
        if (
            state.get("pending_action") == "after_sale_wait_order"
            and intent.intent == IntentType.ORDER_DETAIL
            and intent.order_id
        ):
            return "after_sale_order"
        if (
            state.get("pending_action") == "after_sale_wait_description"
            and intent.intent != IntentType.HANDOFF
        ):
            return "after_sale_description"
        if intent.intent == IntentType.HANDOFF:
            return "handoff"
        if intent.intent == IntentType.AFTER_SALE:
            return "start_after_sale"
        if intent.intent != IntentType.OTHER:
            return "rule_order"
        return "faq_lookup"

    async def _after_sale_order(
        self,
        state: CustomerServiceState,
    ) -> dict[str, AgentResult]:
        intent = state["rule_intent"]
        user_id = state.get("user_id")
        if user_id is None:
            answer = "为了核验售后订单，请先提供登录后的测试 userId。"
        else:
            order = await self.order_service.get_order_by_id(user_id, intent.order_id or "")
            if order is None:
                answer = "没有查询到该订单，或该订单不属于当前用户，请确认订单号后重新发送。"
            else:
                await self.session_service.set_pending_action(
                    state["session_id"],
                    "after_sale_wait_description",
                )
                answer = (
                    f"已核验订单号：{order.id}。"
                    "请继续说明您希望退货、退款、换货，"
                    "或商品遇到的具体问题。"
                )
        return {"result": AgentResult(True, answer, "after_sale")}

    async def _after_sale_description(
        self,
        state: CustomerServiceState,
    ) -> dict[str, AgentResult]:
        await self.session_service.clear_pending_action(state["session_id"])
        return {
            "result": AgentResult(
                True,
                "已收到您的售后诉求。为避免自动执行退款、退货或换货，"
                "请发送“转人工”，人工客服会结合订单与问题描述继续处理。",
                "after_sale",
            )
        }

    async def _handoff(self, state: CustomerServiceState) -> dict[str, AgentResult]:
        session_id = state["session_id"]
        question = state["question"]
        # 先写入本轮问题，再把完整对话快照放进工单。
        await self.session_service.add_message(session_id, "human", question)
        ticket = self.handoff_service.create_ticket(
            session_id=session_id,
            user_id=state.get("user_id"),
            question=question,
            history=await self.session_service.get_history(session_id),
        )
        answer = (
            f"已为您创建人工客服工单：{ticket.ticket_id}。"
            "人工客服会结合当前会话和订单信息继续处理；"
            "如有补充，可继续在本会话说明。"
        )
        await self.session_service.add_message(session_id, "assistant", answer)
        return {"result": AgentResult(True, answer, "handoff")}

    async def _rule_order(self, state: CustomerServiceState) -> dict[str, AgentResult]:
        return {"result": await self._get_order_result(state, state["rule_intent"])}

    async def _faq_lookup(self, state: CustomerServiceState) -> dict[str, str | None]:
        return {"faq_answer": await self.faq_service.get_answer(state["question"])}

    @staticmethod
    def _route_after_faq(state: CustomerServiceState) -> str:
        return "faq_result" if state.get("faq_answer") else "classify_intent"

    @staticmethod
    def _faq_result(state: CustomerServiceState) -> dict[str, AgentResult]:
        return {"result": AgentResult(True, state["faq_answer"] or "", "faq")}

    async def _classify_intent(
        self,
        state: CustomerServiceState,
    ) -> dict[str, IntentResult]:
        return {
            "llm_intent": await self.intent_service.classify_fallback(
                state["question"],
            )
        }

    @staticmethod
    def _route_after_classification(state: CustomerServiceState) -> str:
        intent = state["llm_intent"]
        if intent.intent == IntentType.AFTER_SALE:
            return "start_after_sale"
        if intent.intent != IntentType.OTHER:
            return "fallback_order"
        return "llm_reply"

    async def _start_after_sale(
        self,
        state: CustomerServiceState,
    ) -> dict[str, AgentResult]:
        await self.session_service.set_pending_action(
            state["session_id"],
            "after_sale_wait_order",
        )
        return {
            "result": AgentResult(
                True,
                "已收到您的售后问题。请提供订单号，并说明需要退货、退款、"
                "换货，或商品遇到的具体问题；如情况紧急，也可以发送“转人工”。",
                "after_sale",
            )
        }

    async def _fallback_order(
        self,
        state: CustomerServiceState,
    ) -> dict[str, AgentResult]:
        return {"result": await self._get_order_result(state, state["llm_intent"])}

    async def _get_order_result(
        self,
        state: CustomerServiceState,
        intent: IntentResult,
    ) -> AgentResult:
        user_id = state.get("user_id")
        if user_id is None:
            answer = "查询订单需要登录信息，请提供测试 userId。"
        elif intent.intent == IntentType.ORDER_DETAIL and intent.order_id:
            answer = await self.order_service.get_order_detail_summary(
                user_id,
                intent.order_id,
            )
        else:
            answer = await self.order_service.get_orders_summary(
                user_id,
                intent.order_status,
            )
        return AgentResult(True, answer, "order")

    async def _llm_reply(self, state: CustomerServiceState) -> dict[str, AgentResult]:
        try:
            history = await self.session_service.get_history(state["session_id"])
            answer = await self.deepseek_client.reply(state["question"], history)
            return {"result": AgentResult(False, answer, "llm")}
        except Exception:
            logger.exception("DeepSeek 调用失败")
            return {
                "result": AgentResult(
                    False,
                    "暂时无法获取答案，请稍后再试或联系人工客服。",
                    "fallback",
                )
            }

    async def _record_result(
        self,
        state: CustomerServiceState,
    ) -> dict[str, object]:
        result = state["result"]
        await self.session_service.add_message(
            state["session_id"],
            "human",
            state["question"],
        )
        await self.session_service.add_message(
            state["session_id"],
            "assistant",
            result.answer,
        )
        return {}

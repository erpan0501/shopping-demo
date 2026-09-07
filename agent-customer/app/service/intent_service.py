import logging
import re
from dataclasses import dataclass
from enum import StrEnum

from ..llm.intent_classifier import IntentClassifier
from ..llm.intent_classifier import LlmIntentDecision

logger = logging.getLogger(__name__)


class IntentType(StrEnum):
    ORDER_DETAIL = "order_detail"
    ORDER_LIST = "order_list"
    OTHER = "other"
    HANDOFF = "handoff"
    AFTER_SALE = "after_sale"


@dataclass(frozen=True)
class IntentResult:
    intent: IntentType
    order_id: str | None = None
    order_status: int | None = None


class IntentService:
    def __init__(
        self,
        intent_classifier: IntentClassifier | None = None,
    ):
        self.intent_classifier = intent_classifier

    def parse(self, question: str) -> IntentResult:
        if self._is_handoff_request(question):
            return IntentResult(intent=IntentType.HANDOFF)
        """仅使用规则识别明确的订单与售后问题。"""
        order_id = self._extract_order_id(question)
        if order_id:
            return IntentResult(
                intent=IntentType.ORDER_DETAIL,
                order_id=order_id,
            )

        if self._is_after_sale_request(question):
            return IntentResult(intent=IntentType.AFTER_SALE)

        if self._is_order_query(question):
            return IntentResult(
                intent=IntentType.ORDER_LIST,
                order_status=self._extract_order_status(question),
            )

        return IntentResult(intent=IntentType.OTHER)

    async def classify_fallback(self, question: str) -> IntentResult:
        """规则无法识别且 FAQ 未命中时，才调用大模型。"""
        if self.intent_classifier is None:
            return IntentResult(intent=IntentType.OTHER)

        try:
            decision: LlmIntentDecision = await self.intent_classifier.classify(
                question
            )

            if decision.intent == "order_list":
                return IntentResult(
                    intent=IntentType.ORDER_LIST,
                    order_status=decision.status,
                )
            if decision.intent == "after_sale":
                return IntentResult(intent=IntentType.AFTER_SALE)
        except Exception:
            logger.exception("LLM 意图识别失败，按普通问题处理")

        return IntentResult(intent=IntentType.OTHER)

    def _extract_order_id(self, question: str) -> str | None:
        match = re.search(r"(?<!\d)\d{19}(?!\d)", question)
        return match.group(0) if match else None

    def _is_order_query(self, question: str) -> bool:
        question = question.strip()

        # 操作指南、规则说明类问题应交给 FAQ。
        guide_keywords = (
            "如何查询",
            "怎么查询",
            "怎样查询",
            "在哪里查看",
            "在哪查看",
            "在哪查",
            "怎么找",
            "怎么查看",
            "在哪看",
            "订单查询方法",
            "订单多久",
            "一般多久",
            "通常多久",
            "几天发货",
        )
        if any(keyword in question for keyword in guide_keywords):
            return False

        # “支付成功但仍待付款怎么办”是规则说明/异常处理，而不是查询订单列表。
        if any(keyword in question for keyword in ("怎么办", "仍显示", "为什么", "怎么还是")):
            return False

        has_order_context = "订单" in question or "单号" in question
        has_logistics_context = any(
            keyword in question
            for keyword in ("物流", "快递", "包裹")
        )

        action_keywords = (
            "查",
            "看",
            "状态",
            "进度",
            "发货",
            "到哪",
            "没动静",
            "没收到",
            "派送",
        )
        has_action = any(keyword in question for keyword in action_keywords)

        # “取消订单去哪了”“待付款订单”等即使没写“查”，也属于真实订单查询。
        has_status = self._extract_order_status(question) is not None
        has_implicit_list_context = any(
            keyword in question
            for keyword in ("还有", "哪些", "单吗", "的单", "有单")
        )

        if has_order_context and (has_action or has_status):
            return True

        # “还有未付款的单吗”没有完整写出“订单”，但明确在查询本人订单列表。
        if has_status and has_implicit_list_context:
            return True

        # “帮我查个快递”“包裹一直没动静”不一定出现“订单”二字。
        if has_logistics_context and has_action:
            return True

        return False



    def _extract_order_status(self, question: str) -> int | None:
        status_keywords = {
            1: ("待付款", "未付款"),
            2: ("已付款", "已经付款", "付款成功"),
            3: ("待发货", "未发货", "还没发货"),
            4: ("已发货", "物流", "快递", "派送"),
            5: ("交易成功", "已完成"),
            6: ("交易关闭", "已关闭", "已取消", "取消的订单"),
            7: ("待评价",),
        }

        for status, keywords in status_keywords.items():
            if any(keyword in question for keyword in keywords):
                return status

        return None

    @staticmethod
    def _is_after_sale_request(question: str) -> bool:
        """识别真实售后诉求，避免 FAQ 的流程说明抢占多轮核验流程。"""
        guide_keywords = (
            "如何申请",
            "怎么申请",
            "怎样申请",
            "申请流程",
            "退货流程",
            "退款流程",
            "售后流程",
        )
        if any(keyword in question for keyword in guide_keywords):
            return False

        issue_keywords = (
            "质量问题",
            "商品坏",
            "坏了",
            "不能用",
            "有问题",
            "和描述不一样",
            "货不对板",
            "少件",
            "漏发",
        )
        request_keywords = (
            "我要退货",
            "想退货",
            "我要退款",
            "想退款",
            "想换货",
            "我要换货",
            "申请售后",
            "售后处理",
        )
        return any(keyword in question for keyword in issue_keywords) or any(
            keyword in question for keyword in request_keywords
        )
    def _is_handoff_request(self, question: str) -> bool:
        handoff_keywords = (
            "转人工",
            "人工客服",
            "人工服务",
            "联系客服",
            "找客服",
            "真人客服",
        )

        return any(keyword in question for keyword in handoff_keywords)

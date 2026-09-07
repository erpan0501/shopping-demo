import unittest

from app.service.intent_service import IntentService, IntentType


class IntentServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.service = IntentService()

    def test_implicit_unpaid_order_list_is_a_rule_order_query(self) -> None:
        result = self.service.parse("还有未付款的单吗")

        self.assertEqual(result.intent, IntentType.ORDER_LIST)
        self.assertEqual(result.order_status, 1)

    def test_paid_order_list_accepts_spoken_status_variant(self) -> None:
        result = self.service.parse("我已经付款的订单有哪些")

        self.assertEqual(result.intent, IntentType.ORDER_LIST)
        self.assertEqual(result.order_status, 2)

    def test_payment_exception_keeps_faq_path(self) -> None:
        result = self.service.parse("支付成功但订单仍显示待付款怎么办")

        self.assertEqual(result.intent, IntentType.OTHER)

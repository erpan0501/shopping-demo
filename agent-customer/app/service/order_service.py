from ..java_client import JavaClient
from ..models import ShoppingOrder


ORDER_STATUS_TEXT = {
    1: "未付款",
    2: "已付款",
    3: "未发货",
    4: "已发货",
    5: "交易成功",
    6: "交易关闭",
    7: "待评价",
}


class OrderService:
    def __init__(self, java_client: JavaClient):
        self.java_client = java_client

    async def get_user_orders(
        self,
        user_id: int,
        status: int | None = None,
    ) -> list[ShoppingOrder]:
        return await self.java_client.get_user_orders(
            user_id=user_id,
            status=status,
        )

    async def get_orders_summary(
        self,
        user_id: int,
        status: int | None = None,
    ) -> str:
        orders = await self.get_user_orders(
            user_id=user_id,
            status=status,
        )

        if not orders:
            return "当前没有查询到订单。"

        lines = [f"为您查询到 {len(orders)} 条订单："]

        for order in orders:
            status_text = ORDER_STATUS_TEXT.get(order.status, "状态未知")
            goods_names = "、".join(
                item.goods_name or "商品"
                for item in order.cart_goods
            ) or "商品信息暂缺"

            parts = [
                f"订单号：{order.id}",
                f"状态：{status_text}",
                f"商品：{goods_names}",
            ]

            if order.status == 4:
                if order.shipping_name:
                    parts.append(f"物流公司：{order.shipping_name}")

                if order.shipping_code:
                    parts.append(f"运单号：{order.shipping_code}")

            lines.append("；".join(parts) + "。")

        return "\n".join(lines)


    async def get_order_detail_summary(
    self,
    user_id: int,
    order_id: str,
) -> str:
        order = await self.java_client.get_order_by_id(
            user_id=user_id,
            order_id=order_id,
        )

        if order is None:
            return "没有查询到该订单，或该订单不属于当前用户。"

        status_text = ORDER_STATUS_TEXT.get(order.status, "状态未知")
        goods_names = "、".join(
            item.goods_name or "商品"
            for item in order.cart_goods
        ) or "商品信息暂缺"

        lines = [
            f"订单号：{order.id}",
            f"状态：{status_text}",
            f"商品：{goods_names}",
        ]

        if order.shipping_name:
            lines.append(f"物流公司：{order.shipping_name}")

        if order.shipping_code:
            lines.append(f"运单号：{order.shipping_code}")

        return "；".join(lines) + "。"
    async def get_order_by_id(
        self,
        user_id: int,
        order_id: str,
    ) -> ShoppingOrder | None:
        return await self.java_client.get_order_by_id(
            user_id=user_id,
            order_id=order_id,
        )
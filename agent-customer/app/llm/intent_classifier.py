from typing import Literal

from pydantic import BaseModel, Field

from .deep_seek_client import DeepSeekClient



class LlmIntentDecision(BaseModel):
    intent: Literal["order_list", "after_sale", "other"] = Field(
        description=(
            "order_list 表示查询用户自己的真实订单、订单状态或物流；"
            "after_sale 表示退货、退款、换货、商品质量问题、售后处理；"
            "other 表示其他问题。"
        )
    )

    status: Literal[1, 2, 3, 4, 5, 6, 7] | None = Field(
        default=None,
        description="仅 order_list 使用订单状态；其他意图必须为 null。",
    )


class IntentClassifier:
    def __init__(self, deepseek_client: DeepSeekClient):
        self.structured_llm = deepseek_client.llm.with_structured_output(
            LlmIntentDecision
        )

    async def classify(self, question: str) -> LlmIntentDecision:
        return await self.structured_llm.ainvoke(
            [
                (
                    "你只负责判断用户意图，不回答用户问题。"
                    "只输出受限分类结果。"
                    "用户想查询自己当前订单、订单状态或物流时，intent 是 order_list。"
                    "用户咨询退货、退款、换货、商品质量问题、售后处理时，intent 是 after_sale。"
                    "“如何查询订单”“订单规则是什么”等操作说明问题必须返回 other。"
                    "无法确定时返回 other。"
                    "只有 order_list 可以填写 status，其他情况 status 必须为 null。"
                ),
                ("human", question),
            ]
        )
from langchain_deepseek import ChatDeepSeek
from ..config import Settings,get_settings



class DeepSeekClient:
    def __init__(self, settings: Settings):
      self.llm = ChatDeepSeek(
        model=settings.deepseek_model,
        api_key=settings.deepseek_api_key,
        temperature=0.2,
        max_tokens=300,
        extra_body={
            "thinking": {
                "type": "disabled",
            }
        },
    )

    async def reply(
        self,
        question: str,
        history: list[tuple[str, str]],
    ) -> str:
        messages = [
            (
                "system",
                "你是商城客服。优先根据已知上下文回答。没有可靠的 FAQ 或业务数据时，"
                "不要编造商城政策、价格、库存、订单状态；应请用户补充信息或建议转人工。",
            )
        ]

        for role, content in history:
            messages.append((role, content))

        messages.append(("human", question))

        response = await self.llm.ainvoke(messages)
        content = response.content if isinstance(response.content, str) else str(response.content)
        answer = content.strip()

        if not answer:
            raise RuntimeError("DeepSeek 返回了空回答")

        return answer
# async def main() -> None:
#     client = DeepSeekClient(get_settings())

#     result = await client.reply(
#         "请问你们商城的退货政策是什么？"
#     )

#     print(result)


# if __name__ == "__main__":
#     import asyncio
#     asyncio.run(main())
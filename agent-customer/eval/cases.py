"""稳定、可复现的客服路由评测集（共 200 条）。"""

from dataclasses import dataclass


@dataclass(frozen=True)
class EvalCase:
    case_id: str
    category: str
    question: str
    expected_sources: tuple[str, ...]
    has_side_effect: bool = False


VARIANTS = (
    "",
    "，麻烦帮我看一下",
    "，谢谢",
    "，急用",
    "啊",
)


def _expand(
    category: str,
    seeds: tuple[str, ...],
    expected_sources: tuple[str, ...],
    *,
    order_id: str,
    has_side_effect: bool = False,
) -> list[EvalCase]:
    cases: list[EvalCase] = []
    for seed_index, seed in enumerate(seeds, start=1):
        for variant_index, suffix in enumerate(VARIANTS, start=1):
            cases.append(
                EvalCase(
                    case_id=f"{category}-{seed_index:02d}-{variant_index}",
                    category=category,
                    question=(seed.format(order_id=order_id) + suffix).strip(),
                    expected_sources=expected_sources,
                    has_side_effect=has_side_effect,
                )
            )
    return cases


def get_eval_cases(order_id: str) -> list[EvalCase]:
    """返回 200 条真实客服口语风格用例。

    ``order_id`` 应替换成运行环境中属于 ``USER_ID`` 的有效 19 位订单号，
    以覆盖订单详情与物流正文断言。
    """
    cases: list[EvalCase] = []
    cases += _expand(
        "order_detail",
        (
            "帮我查下订单 {order_id}",
            "订单号 {order_id} 现在什么状态",
            "我这个单 {order_id} 到哪一步了",
            "麻烦看看 {order_id} 发货没有",
            "{order_id} 这个订单怎么还没动静",
            "帮忙核实一下订单 {order_id}",
            "订单 {order_id} 的商品明细是什么",
            "{order_id} 是不是已经支付成功了",
            "查一下单号 {order_id}",
            "我想知道 {order_id} 的处理进度",
        ),
        ("order",),
        order_id=order_id,
    )
    cases += _expand(
        "order_list",
        (
            "帮我看看我的订单",
            "我买的东西现在什么状态",
            "查下待付款订单",
            "还有未付款的单吗",
            "看看待发货订单",
            "我已经付款的订单有哪些",
            "帮我找一下交易成功的订单",
            "取消的订单在哪里看",
        ),
        ("order",),
        order_id=order_id,
    )
    cases += _expand(
        "logistics",
        (
            "帮我查个快递",
            "我的物流到哪里了",
            "已发货订单的运单号是什么",
            "包裹怎么一直没动静",
            "快递什么时候派送",
            "我想看一下物流信息",
        ),
        ("order",),
        order_id=order_id,
    )
    cases += _expand(
        "handoff",
        (
            "我要转人工客服",
            "帮我联系人工客服",
            "找真人客服处理",
            "请安排人工服务",
        ),
        ("handoff",),
        order_id=order_id,
        has_side_effect=True,
    )
    cases += _expand(
        "faq",
        (
            "如何查询我的订单？",
            "订单多久可以发货？",
            "如何申请退货？",
            "商城支持哪些支付方式？",
            "退款多久到账？",
            "忘记密码怎么办？",
        ),
        ("faq",),
        order_id=order_id,
    )
    cases += _expand(
        "after_sale",
        (
            "收到的商品有质量问题，想换货",
            "商品坏了，我要申请售后",
            "我想退货，商品和描述不一样",
            "刚收到就不能用了，能退款吗",
        ),
        ("after_sale",),
        order_id=order_id,
    )
    cases += _expand(
        "other",
        (
            "你好，在吗",
            "这个商品还能便宜一点吗",
        ),
        ("llm", "fallback"),
        order_id=order_id,
    )

    assert len(cases) == 200
    assert len({case.case_id for case in cases}) == len(cases)
    return cases

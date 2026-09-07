"""调用运行中的 Agent，执行 200 条客服路由评测。"""

from __future__ import annotations

import argparse
import asyncio
import json
from collections import Counter
from dataclasses import asdict
from pathlib import Path

import httpx

from cases import EvalCase, get_eval_cases


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="商城客服路由评测")
    parser.add_argument("--base-url", default="http://127.0.0.1:8000")
    parser.add_argument("--user-id", type=int, default=1)
    parser.add_argument("--order-id", default="2087106115733889025")
    parser.add_argument(
        "--include-side-effects",
        action="store_true",
        help="执行会创建本地人工工单的 handoff 用例",
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=Path("eval/report.json"),
        help="评测结果 JSON 路径",
    )
    return parser.parse_args()


async def run_case(
    client: httpx.AsyncClient,
    case: EvalCase,
    user_id: int,
) -> dict[str, object]:
    response = await client.post(
        "/chat",
        json={
            "sessionId": f"eval-{case.case_id}",
            "userId": user_id,
            "question": case.question,
        },
    )
    payload = response.json() if response.content else {}
    source = payload.get("source")
    return {
        **asdict(case),
        "status_code": response.status_code,
        "actual_source": source,
        "answer": payload.get("answer"),
        "passed": response.status_code == 200 and source in case.expected_sources,
    }


async def main() -> int:
    args = parse_args()
    cases = get_eval_cases(args.order_id)
    results: list[dict[str, object]] = []
    async with httpx.AsyncClient(base_url=args.base_url, timeout=30.0) as client:
        for case in cases:
            if case.has_side_effect and not args.include_side_effects:
                results.append({
                    **asdict(case),
                    "skipped": True,
                    "reason": "requires --include-side-effects",
                })
                continue
            try:
                results.append(await run_case(client, case, args.user_id))
            except (httpx.HTTPError, ValueError) as exc:
                results.append({
                    **asdict(case),
                    "passed": False,
                    "error": str(exc),
                })

    executed = [result for result in results if not result.get("skipped")]
    passed = [result for result in executed if result.get("passed")]
    category_totals = Counter(result["category"] for result in executed)
    category_passed = Counter(result["category"] for result in passed)
    summary = {
        "total_cases": len(cases),
        "executed": len(executed),
        "skipped": len(cases) - len(executed),
        "passed": len(passed),
        "failed": len(executed) - len(passed),
        "by_category": {
            category: {
                "passed": category_passed[category],
                "total": total,
            }
            for category, total in sorted(category_totals.items())
        },
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(
        json.dumps({"summary": summary, "results": results}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print(f"结果已写入 {args.report}")
    return 0 if summary["failed"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))

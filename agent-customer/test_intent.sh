#!/usr/bin/env bash
set -u

BASE="${BASE:-http://127.0.0.1:8000}"
USER_ID="${USER_ID:-1}"
ORDER_ID="${ORDER_ID:-2087106115733889025}"

QUESTIONS=(
  "帮我看看这个订单 ${ORDER_ID} 到哪一步了"
  "${ORDER_ID}"
  "查询订单号 1999999999999999999"
  "帮我查查我的订单呗"
  "我的订单现在是什么状态啊"
  "帮我看看我还有没有待付款的订单"
  "我订单的快递到哪了呀"
  "帮我查下我交易成功的订单"
  "你们这怎么申请退货啊"
  "你们支持支付宝付款吗"
  "我密码忘了咋办"
  "你好，有人吗"
  "有没有推荐的好用手机啊"
  "这个能便宜点吗"
  "在哪查我的订单啊"
  "订单多久可以发货"
  "我取消的订单去哪了"
  "帮我查个快递"
  "给我转人工客服吧"
  "订单号 ${ORDER_ID} 有问题，转人工"
  "收到的商品有质量问题，想换货"
  "我买到的商品坏了，怎么处理"
)


# 多个结果用 | 分隔，表示任意一个都算通过。
EXPECTED_SOURCES=(
  "order"
  "order"
  "order"
  "order"
  "order"
  "order"
  "order"
  "order"
  "faq|llm"
  "faq"
  "faq|llm"
  "llm"
  "llm"
  "llm"
  "faq"
  "faq"
  "order|llm"
  "order"
  "handoff"
  "handoff"
  "after_sale"
  "after_sale"
)

passed=0
failed=0
total="${#QUESTIONS[@]}"
echo "== Agent 意图回归测试 =="
echo "BASE=$BASE USER_ID=$USER_ID"
echo

for ((i = 0; i < total; i++)); do
  question="${QUESTIONS[$i]}"
  expected="${EXPECTED_SOURCES[$i]}"
  session_id="intent-regression-$((i + 1))"

  response=$(
    /usr/bin/curl -sS -m 30 -X POST "$BASE/chat" \
      -H "Content-Type: application/json" \
      -d "{\"sessionId\":\"$session_id\",\"question\":\"$question\",\"userId\":$USER_ID}"
  )

  source=$(
    printf '%s' "$response" |
      uv run python -c 'import json, sys; print(json.load(sys.stdin).get("source", ""))' \
      2>/dev/null
  )

  if [[ "|$expected|" == *"|$source|"* ]]; then
    result="PASS"
    passed=$((passed + 1))
  else
    result="FAIL"
    failed=$((failed + 1))
  fi

  printf '[%s] %02d source=%-8s expected=%-10s %s\n' \
    "$result" "$((i + 1))" "${source:-none}" "$expected" "$question"
done

echo
echo "== 售后多轮流程测试 =="

AFTER_SALE_SESSION="after-sale-regression-001"

response_1=$(
  /usr/bin/curl -sS -m 30 -X POST "$BASE/chat" \
    -H "Content-Type: application/json" \
    -d "{\"sessionId\":\"$AFTER_SALE_SESSION\",\"question\":\"收到的商品有质量问题，想换货\",\"userId\":$USER_ID}"
)

response_2=$(
  /usr/bin/curl -sS -m 30 -X POST "$BASE/chat" \
    -H "Content-Type: application/json" \
    -d "{\"sessionId\":\"$AFTER_SALE_SESSION\",\"question\":\"$ORDER_ID\",\"userId\":$USER_ID}"
)

response_3=$(
  /usr/bin/curl -sS -m 30 -X POST "$BASE/chat" \
    -H "Content-Type: application/json" \
    -d "{\"sessionId\":\"$AFTER_SALE_SESSION\",\"question\":\"我想换货，商品屏幕有划痕\",\"userId\":$USER_ID}"
)

source_1=$(printf '%s' "$response_1" | uv run python -c 'import json,sys; print(json.load(sys.stdin).get("source",""))')
source_2=$(printf '%s' "$response_2" | uv run python -c 'import json,sys; print(json.load(sys.stdin).get("source",""))')
source_3=$(printf '%s' "$response_3" | uv run python -c 'import json,sys; print(json.load(sys.stdin).get("source",""))')

total=$((total + 1))

if [[ "$source_1" == "after_sale" && "$source_2" == "after_sale" && "$source_3" == "after_sale" ]]; then
  passed=$((passed + 1))
  echo "[PASS] 售后多轮流程：售后问题 → 订单号 → 问题描述"
else
  failed=$((failed + 1))
  echo "[FAIL] 售后多轮流程：source 分别为 $source_1 / $source_2 / $source_3"
fi

echo
echo "== 结果：$passed / $total 通过，$failed 失败 =="

# 转人工用例会创建本地测试工单；清理固定测试会话产生的记录。
uv run python - <<'PY'
import sqlite3

with sqlite3.connect("data/customer_service.db") as connection:
    connection.execute(
        "DELETE FROM handoff_ticket WHERE session_id IN (?, ?)",
        ("intent-regression-19", "intent-regression-20"),
    )
PY

if [[ "$failed" -gt 0 ]]; then
  exit 1
fi

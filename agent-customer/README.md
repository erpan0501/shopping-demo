# 商城智能客服 Agent

面向商城售前、订单、物流与售后的 FastAPI 客服服务。它只通过受控的 Java 商城接口读取业务数据；模型不直接访问 MySQL，也不能自行拼接业务 URL 或执行 SQL。

> 本目录默认对接兼容的 Java 商城服务 `http://127.0.0.1:8080`。目标仓库根目录的 `shopping_demo` 演示后端使用 `8090` 端口且接口契约不同，不能直接替代该依赖。

## 功能

- FAQ：Java 精确与模糊匹配优先；可选 Qdrant 向量检索与重排序。
- 订单与物流：订单号、订单状态、待发货、已发货和物流单号查询。
- 售后多轮：订单归属核验后收集退货、退款、换货和质量问题诉求。
- 人工转接：创建 SQLite 工单；提供内部客服工作台与工单状态管理接口。
- 安全与稳定性：JWT 用户身份桥接、手机号与订单号脱敏、限流、审计、Java 重试和短暂熔断。

## 架构

```text
用户端 / 后台工作台
        │
        ▼
FastAPI /chat  ──► LangGraph 状态图 ──► Java 商城 API
                       │       │             │
                       │       ├─────────────┤ FAQ / 订单 / 物流 / JWT
                       │       ▼             ▼
                       │     Qdrant       Redis（生产可选）
                       ▼
                 LLM 受限兜底
                       │
                       ▼
              SQLite 人工工单与审计
```

路由顺序为：售后待办与明确规则 → FAQ → Qdrant（可选）→ 结构化意图识别 → 订单/售后处理或受限兜底。商品搜索、商品详情与购物车操作仍由商城 UI 处理，不进入正式客服链路。

## 本地启动

环境要求：Python 3.13+、[uv](https://docs.astral.sh/uv/)，以及一个兼容的 Java 商城服务。

```bash
cd agent-customer
cp .env.example .env
# 在 .env 中填写 DEEPSEEK_API_KEY 与 STAFF_API_KEY
uv sync
uv run uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload --reload-dir app
```

先启动 Java 服务并确认 `http://127.0.0.1:8080` 可访问。开发联调可使用请求体 `userId`；生产环境应设置 `ALLOW_TEST_USER_ID=false`，并由商城 JWT 的 `Authorization: Bearer <token>` 解析用户身份。

启动后可访问：

| 地址 | 用途 |
| --- | --- |
| `http://127.0.0.1:8000/health` | Agent 存活检查 |
| `http://127.0.0.1:8000/health/java` | Java 连通性检查 |
| `http://127.0.0.1:8000/health/session` | 会话后端检查 |
| `http://127.0.0.1:8000/docs` | OpenAPI 文档 |
| `http://127.0.0.1:8000/internal/console` | 内部客服工作台 |

示例请求：

```bash
curl -X POST http://127.0.0.1:8000/chat \
  -H 'Content-Type: application/json' \
  -d '{"sessionId":"demo-001","userId":1,"question":"帮我查一下已发货订单"}'
```

## 环境变量

以 `.env.example` 为准。下列配置在生产环境必须显式设置：

| 变量 | 说明 |
| --- | --- |
| `DEEPSEEK_API_KEY` | LLM 调用密钥，不可提交 |
| `STAFF_API_KEY` | 内部工单接口密钥，应使用高强度随机值 |
| `JAVA_BASE_URL` | Java 商城服务地址 |
| `ALLOW_TEST_USER_ID=false` | 禁止客户端自行声明用户 ID |
| `SESSION_BACKEND=redis` | 跨实例会话与售后状态 |
| `RATE_LIMIT_BACKEND=redis` | 多实例共享限流 |
| `FAQ_RETRIEVAL_BACKEND=qdrant` | 启用 FAQ 语义检索时设置 |

`.env`、本地工单数据库、评测报告与虚拟环境均已忽略，不能提交到 Git。

## 人工客服与运维

用户发送“转人工”“人工客服”等请求后，Agent 会在 `data/customer_service.db` 创建工单。内部接口需携带 `X-Staff-Key: <STAFF_API_KEY>`：

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| `GET` | `/internal/tickets?status=waiting_human` | 待处理工单 |
| `GET` | `/internal/tickets/{ticketId}` | 工单和会话记录 |
| `PATCH` | `/internal/tickets/{ticketId}` | 更新处理状态 |
| `GET` | `/internal/audit-events` | 审计事件 |
| `GET` | `/internal/audit-events/summary` | 时间窗口汇总 |

## 测试与评测

```bash
cd agent-customer
DEEPSEEK_API_KEY=test uv run python -m unittest discover -s tests -v
uv run python eval/run.py --user-id 1 --order-id 2087106115733889025
```

评测集包含 200 条口语化客服路由用例。默认跳过会创建工单的转人工用例；需要完整执行时增加 `--include-side-effects`。生成的 `eval/report.json` 仅用于本地查看。

## Docker Compose

`compose.yaml` 可联动 MySQL、Redis、Qdrant、Java 和 Agent。该 Compose 文件的 Java 构建上下文默认指向本机的兼容 Java 商城项目；将 `JAVA_PROJECT_DIR` 设置为该项目的绝对路径后，再执行：

```bash
cp .env.compose.example .env.compose
# 填写数据库密码、DEEPSEEK_API_KEY 和 STAFF_API_KEY
docker compose --env-file .env.compose up --build
```

## 目录

```text
app/
├── agent/faq_agent.py       # LangGraph 客服状态图
├── router/                  # Chat、工单、审计、健康检查路由
├── service/                 # FAQ、订单、会话、限流、转人工服务
├── llm/                     # 结构化意图和受限回复
└── java_client.py           # Java API 封装与重试/熔断
tests/                       # 单元与回归测试
eval/                        # 200 条评测集
docker/                      # Compose 演示数据库初始化脚本
```

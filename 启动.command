#!/bin/bash
set -u

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
RUN_DIR="$ROOT_DIR/.run"
BACKEND_PID_FILE="$RUN_DIR/backend.pid"
CLIENT_PID_FILE="$RUN_DIR/client.pid"
ADMIN_PID_FILE="$RUN_DIR/admin.pid"

mkdir -p "$RUN_DIR"

is_running() {
  [[ -f "$1" ]] && kill -0 "$(<"$1")" 2>/dev/null
}

port_is_busy() {
  lsof -tiTCP:"$1" -sTCP:LISTEN >/dev/null 2>&1
}

wait_for_port() {
  local port="$1"
  local label="$2"
  for _ in {1..60}; do
    if port_is_busy "$port"; then
      echo "$label 已启动：端口 $port"
      return 0
    fi
    sleep 1
  done
  return 1
}

if is_running "$BACKEND_PID_FILE" || is_running "$CLIENT_PID_FILE" || is_running "$ADMIN_PID_FILE"; then
  echo "Java 商城演示已在运行。如需重启，请先双击“关闭.command”。"
  exit 0
fi

if ! command -v mvn >/dev/null 2>&1 || ! command -v npm >/dev/null 2>&1; then
  echo "未找到 Maven 或 npm，请先安装 Java 17、Maven 和 Node.js。"
  exit 1
fi

if port_is_busy 8090 || port_is_busy 8081 || port_is_busy 8082; then
  echo "8090、8081 或 8082 端口正在被占用，请先关闭占用该端口的项目。"
  exit 1
fi

if [[ ! -d "$ROOT_DIR/前端/shopping_client/node_modules" ]]; then
  echo "首次启动，正在安装商城端依赖…"
  (cd "$ROOT_DIR/前端/shopping_client" && npm install) || exit 1
fi
if [[ ! -d "$ROOT_DIR/前端/vue3-admin-main/node_modules" ]]; then
  echo "首次启动，正在安装管理端依赖…"
  (cd "$ROOT_DIR/前端/vue3-admin-main" && npm install) || exit 1
fi

echo "正在启动 Java 后端…"
nohup bash -lc 'cd "$1" && exec mvn -q -pl shopping_demo spring-boot:run' -- "$ROOT_DIR" \
  > "$RUN_DIR/backend.log" 2>&1 &
echo $! > "$BACKEND_PID_FILE"

echo "正在启动商城端 Vue 前端…"
nohup bash -lc 'cd "$1" && exec npm run serve -- --host 127.0.0.1 --port 8081' -- "$ROOT_DIR/前端/shopping_client" \
  > "$RUN_DIR/client.log" 2>&1 &
echo $! > "$CLIENT_PID_FILE"

echo "正在启动管理端 Vue 前端…"
nohup bash -lc 'cd "$1" && exec npm run serve -- --host 127.0.0.1 --port 8082' -- "$ROOT_DIR/前端/vue3-admin-main" \
  > "$RUN_DIR/admin.log" 2>&1 &
echo $! > "$ADMIN_PID_FILE"

if ! wait_for_port 8090 "后端" || ! wait_for_port 8081 "商城端" || ! wait_for_port 8082 "管理端"; then
  echo "启动超时，请查看：$RUN_DIR"
  bash "$ROOT_DIR/关闭.command"
  exit 1
fi

echo "Java 商城已启动：商城端 http://localhost:8081，管理端 http://localhost:8082"
echo "日志目录：$RUN_DIR"
open "http://localhost:8081"

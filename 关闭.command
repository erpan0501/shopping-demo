#!/bin/bash
set -u

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
RUN_DIR="$ROOT_DIR/.run"

terminate_process_tree() {
  local target_pid="$1"
  local child
  for child in $(pgrep -P "$target_pid" 2>/dev/null || true); do
    terminate_process_tree "$child"
  done
  kill -TERM "$target_pid" 2>/dev/null || true
}

stop_pid_file() {
  local label="$1"
  local pid_file="$2"
  local pid

  [[ -f "$pid_file" ]] || return 0
  pid="$(<"$pid_file")"
  if kill -0 "$pid" 2>/dev/null; then
    terminate_process_tree "$pid"
    echo "正在关闭${label}（PID ${pid}）…"
  fi
  rm -f "$pid_file"
}

stop_pid_file "管理端 Vue 前端" "$RUN_DIR/admin.pid"
stop_pid_file "商城端 Vue 前端" "$RUN_DIR/client.pid"
stop_pid_file "Java 后端" "$RUN_DIR/backend.pid"
echo "Java 商城演示已关闭。"

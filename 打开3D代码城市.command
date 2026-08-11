#!/bin/zsh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ATLAS_DIR="$SCRIPT_DIR/code-atlas"
MAP_FILE="$ATLAS_DIR/generated/shopping.cc.json.gz"

cd "$ATLAS_DIR"
if [[ ! -x "node_modules/.bin/ccsh" ]]; then
  npm install
fi
if [[ ! -f "$MAP_FILE" ]]; then
  npm run city:generate
fi

open -R "$MAP_FILE"
open "https://codecharta.com/visualization/app/index.html"
echo "已打开 CodeCharta，并在 Finder 中选中 shopping.cc.json.gz。"
echo "请把该文件拖入 CodeCharta 页面。"

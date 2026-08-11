#!/bin/zsh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ATLAS_DIR="$SCRIPT_DIR/code-atlas"

cd "$ATLAS_DIR"
if [[ ! -x "node_modules/.bin/ccsh" ]]; then
  npm install
fi
if [[ ! -f "generated/shopping.cc.json.gz" ]]; then
  npm run city:generate
fi
npm run atlas
open "$ATLAS_DIR/site/index.html"

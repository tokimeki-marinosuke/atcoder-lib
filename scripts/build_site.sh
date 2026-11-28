#!/usr/bin/env bash
# 教材のMarkdownを build/docs へコピーし、MkDocs でサイトを作る。
# 使い方: bash scripts/build_site.sh          （build/site に生成）
#         bash scripts/build_site.sh serve    （http://127.0.0.1:8000 でプレビュー）
set -euo pipefail
cd "$(dirname "$0")/.."

rm -rf build/docs
mkdir -p build/docs
cp README.md problem-solving-index.md build/docs/
# tests/ は教材からリンクされているテストコードとして同梱する
cp -r algorithms techniques contests learning-notes tests templates build/docs/

if [ "${1:-build}" = "serve" ]; then
  python -m mkdocs serve
else
  python -m mkdocs build --strict
fi

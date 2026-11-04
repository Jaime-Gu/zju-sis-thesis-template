#!/bin/bash
set -u
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT" || exit 1
export PATH="$HOME/.local/bin:/Library/TeX/texbin:$HOME/Library/TinyTeX/bin/universal-darwin:/opt/homebrew/bin:/usr/local/bin:$PATH"

if command -v python3 >/dev/null 2>&1; then
  PYTHON=python3
else
  echo "没有找到 Python 3。请先按照 使用说明.md 安装 Python。"
  read -r -p "按回车键关闭窗口……"
  exit 1
fi

"$PYTHON" scripts/build.py
STATUS=$?
if [ "$STATUS" -eq 0 ]; then
  open "$ROOT/output/毕业论文.pdf"
else
  echo
  echo "生成失败。请把上面的错误信息完整复制下来，再对照 使用说明.md 的“遇到问题怎么办”处理。"
fi
read -r -p "按回车键关闭窗口……"
exit "$STATUS"

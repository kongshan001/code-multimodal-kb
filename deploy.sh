#!/usr/bin/env bash
# ============================================================
# 一键部署（macOS / Linux）：装全部环境 + 接入项目（代码+文档+本地记忆+注册）
# 用法: ./deploy.sh <代码目录> [文档目录] [项目名]
# 前置：仅 Python 3.12+。其余（cmm/graphify/ollama/mem0ai）本脚本自动装。
# Windows 用 deploy.bat。
# ============================================================
set -euo pipefail
cd "$(dirname "$0")"
CODE="${1:?用法: $0 <代码目录> [文档目录] [项目名]}"
shift || true
DOCS=""; [ "$#" -ge 1 ] && [ -n "$1" ] && DOCS="$1" && shift
NAME="${1:-$(basename "$CODE")}"
echo "=== 一键部署: $NAME (code=$CODE docs=${DOCS:-<无>}) ==="
python3 setup-kb.py --full --code "$CODE" ${DOCS:+--docs "$DOCS"} --name "$NAME" --memory-mode local
echo "=== ✅ 完成：重启 Claude Code 后 mcp__* 工具可用 ==="

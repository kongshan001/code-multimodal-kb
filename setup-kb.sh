#!/usr/bin/env bash
# ============================================================
#  KB+Memory 交互式接入（macOS / Linux）
#  逐项提示录入，回车用默认。Windows 用 setup-kb.bat。
#  前置：Python 3.12+ + codebase-memory-mcp + graphify + claude
# ============================================================
cd "$(dirname "$0")" || exit 1
python3 setup-kb.py --interactive "$@"

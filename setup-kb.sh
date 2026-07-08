#!/usr/bin/env bash
# setup-kb.sh — KB + Memory 便捷接入（给任意项目工程一键部署）
#   知识库(codebase-memory-mcp + graphify) + 记忆(Mem0, 可选) + agent MCP 注册
#
# 用法:
#   ./setup-kb.sh --code <代码目录> --docs <文档目录> --name <项目名>
#                 [--cmm-mode fast|moderate|full] [--no-memory] [--dry-run]
#                 [--llm-key X --llm-base Y --llm-model Z]
#
# 新设备: git clone <engineer_demo> && cd engineer_demo && ./setup-kb.sh ...
# 新项目: 同上，--code/--docs 指向新项目目录即可。
# 详见 docs/deployment-runbook.md。
set -euo pipefail

CODE=""; DOCS=""; NAME=""; CMM_MODE="moderate"; MEMORY_SKIP=0; DRY=0
LLM_KEY=""; LLM_BASE=""; LLM_MODEL=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --code) CODE="$2"; shift 2;; --docs) DOCS="$2"; shift 2;; --name) NAME="$2"; shift 2;;
    --cmm-mode) CMM_MODE="$2"; shift 2;; --no-memory) MEMORY_SKIP=1; shift;;
    --dry-run) DRY=1; shift;;
    --llm-key) LLM_KEY="$2"; shift 2;; --llm-base) LLM_BASE="$2"; shift 2;; --llm-model) LLM_MODEL="$2"; shift 2;;
    *) echo "未知参数: $1（见 docs/deployment-runbook.md）" >&2; exit 2;;
  esac
done
[[ -z "$CODE" || -z "$NAME" ]] && { echo "需 --code <代码目录> --name <项目名>" >&2; exit 2; }
[[ ! -d "$CODE" ]] && { echo "代码目录不存在: $CODE" >&2; exit 1; }
[[ -n "$DOCS" && ! -d "$DOCS" ]] && { echo "文档目录不存在: $DOCS" >&2; exit 1; }

run() { echo "▶ $*"; [[ $DRY -eq 1 ]] || "$@"; }

echo "=== KB+Memory 接入: $NAME (code=$CODE docs=${DOCS:-<无>}) ==="

# [1/6] precheck
echo "=== [1/6] precheck ==="
need() { command -v "$1" >/dev/null 2>&1 || { echo "✗ 缺依赖: $1（见 runbook §0/§A/§B 安装）" >&2; exit 1; }; }
need codebase-memory-mcp
[[ -n "$DOCS" ]] && need graphify
need claude
echo "  ✓ 工具就位"

# [2/6] LLM backend（默认复用 ~/.claude.json openspace 的 BigModel key）
echo "=== [2/6] LLM backend ==="
if [[ -z "$LLM_KEY" ]]; then
  LLM_KEY=$(python3 -c "import json,os;print(json.load(open(os.path.expanduser('~/.claude.json')))['mcpServers']['openspace']['env']['OPENSPACE_LLM_API_KEY'])" 2>/dev/null || echo "")
  LLM_BASE="${LLM_BASE:-https://open.bigmodel.cn/api/anthropic}"; LLM_MODEL="${LLM_MODEL:-glm-4.6}"
  [[ -n "$LLM_KEY" ]] && echo "  ℹ 复用环境 BigModel key ($LLM_MODEL)" || { echo "✗ 无 LLM key（用 --llm-key 传，或配 ~/.claude.json openspace）" >&2; exit 1; }
fi
export ANTHROPIC_API_KEY="$LLM_KEY" ANTHROPIC_BASE_URL="${LLM_BASE:-https://open.bigmodel.cn/api/anthropic}" ANTHROPIC_MODEL="${LLM_MODEL:-glm-4.6}"
echo "  ✓ backend=$ANTHROPIC_BASE_URL model=$ANTHROPIC_MODEL"

# [3/6] 代码 KB
echo "=== [3/6] 代码 KB (cmm index, mode=$CMM_MODE) ==="
run codebase-memory-mcp cli index_repository "{\"repo_path\":\"$CODE\",\"mode\":\"$CMM_MODE\"}"

# [4/6] 文档 KB
if [[ -n "$DOCS" ]]; then
  echo "=== [4/6] 文档 KB (graphify, docs-only) ==="
  ( cd "$DOCS" && run graphify . )
else
  echo "=== [4/6] 跳过文档 KB（未提供 --docs）==="
fi

# [5/6] 记忆 (Mem0) — 最重，Docker；V1 未自动化
if [[ $MEMORY_SKIP -eq 1 ]]; then
  echo "=== [5/6] 跳过记忆层（--no-memory）==="
else
  echo "=== [5/6] 记忆层 (Mem0) ==="
  echo "  ⚠ Mem0 自托管需 Docker（API + pg/pgvector + Neo4j，或全本地 Qdrant+Neo4j+Ollama）。"
  echo "  ⚠ 本 V1 未自动化此步；见 docs/deployment-runbook.md + add-agent-memory task 2.2 手动部署。"
  echo "  ⚠ 完成后: claude mcp add -s user mem0 -- mem0-mcp  (TODO 待 Mem0 docker-compose 就位)"
fi

# [6/6] agent MCP 注册 + 验证
echo "=== [6/6] agent MCP 注册 ==="
run codebase-memory-mcp install -y || echo "  ℹ cmm install 跳过（已注册 / 见 runbook §A.4）"
if [[ -n "$DOCS" ]]; then
  GRAPH_JSON="$DOCS/graphify-out/graph.json"
  if [[ -f "$GRAPH_JSON" ]]; then
    run claude mcp add -s user "graphify-$NAME" -- "$(command -v graphify-mcp)" "$GRAPH_JSON" \
      || echo "  ℹ graphify-mcp 注册失败（venv 需 mcp extra：uv tool install --force graphifyy --with mcp）"
  fi
fi

echo "=== ✅ 接入完成: $NAME ==="
echo "验证: claude mcp list   |   重启 Claude Code 后 mcp__* 工具可用"
[[ -n "$DOCS" ]] && echo "文档检索示例: graphify query \"<问题>\" --graph $DOCS/graphify-out/graph.json"

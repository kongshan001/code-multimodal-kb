#!/usr/bin/env bash
# engineer_demo 一键 setup（降接入成本 · 固化本会话踩过的坑）
#
# 用法：
#   ./setup.sh python     # 只装 Python 评测依赖（最轻，跑 pytest + 检索层 bench）
#   ./setup.sh tools      # 装 4 个 KB 工具（cmm/graphify/codegraph/mempalace）
#   ./setup.sh render     # 装 SVG→PNG 渲染器（fireworks-tech-graph 流程图用）
#   ./setup.sh creds      # 检查/提示 LLM 凭据配置
#   ./setup.sh all        # 全装
#
# 详见 docs/deployment-runbook.md（A 代码 / B 文档 / C 评测 / D 记忆层）。
set -e
REPO="$(cd "$(dirname "$0")" && pwd)"

install_python() {
  echo "=== Python 评测依赖（pytest + anthropic，实测兼容）==="
  pip install -r "$REPO/eval/requirements.txt"
  # 关键：锁 numpy<2（torch/transformers 若装了，numpy2 会 ABI 崩；eval 本身不用 numpy，但防全局环境污染）
  pip install "numpy<2" 2>/dev/null || true
  python -c "import pytest, anthropic; print('✓ pytest + anthropic OK')"
  echo "→ 零依赖测试：pytest eval/tests/   检索层：python -m eval.cli run code --target godot --method bm25"
}

install_tools() {
  echo "=== 4 个 KB 工具（各有安装坑，详见 deployment-runbook）==="
  # 1. cmm（代码 KB）—— 二进制下载，见 runbook §A
  if ! command -v codebase-memory-mcp >/dev/null 2>&1; then
    echo "  [cmm] 装：见 docs/deployment-runbook.md §A（官方源下载二进制，禁 curl|bash 抓 main）"
  else echo "  [cmm] ✓ $(codebase-memory-mcp --version 2>&1 | tail -1)"; fi
  # 2. graphify（文档 KB）—— npm，建图花 LLM
  if ! command -v graphify >/dev/null 2>&1; then
    echo "  [graphify] 装：npm install -g graphify（见 runbook §B，需 LLM key 建图）"
  else echo "  [graphify] ✓ 已装"; fi
  # 3. codegraph（第二代码 KB）—— npm
  if ! command -v codegraph >/dev/null 2>&1; then
    echo "  [codegraph] 装：npm install -g @colbymchenry/codegraph（接 A/B codegraph 臂 + goldgen 枚举；npm 上的裸 codegraph 是撞名空壳包，必须带 @colbymchenry scope）"
  else echo "  [codegraph] ✓ $(codegraph --version 2>&1 | tail -1)"; fi
  # 4. MemPalace（记忆层）—— Intel Mac 必须 py3.11（onnxruntime wheel 限制）
  if ! command -v mempalace >/dev/null 2>&1; then
    echo "  [mempalace] 装：uv tool install --python 3.11 mempalace（Intel Mac 必须 py3.11，见 runbook §D.1）"
  else echo "  [mempalace] ✓ $(mempalace --version 2>&1 | tail -1)"; fi
  echo "  ⚠️ auto-save hook 先别配（非 idempotent，会 bloat，见 runbook §D.4）；用手动 mempalace sweep"
}

install_render() {
  echo "=== SVG→PNG 渲染器（fireworks-tech-graph 流程图用，二选一）==="
  if command -v rsvg-convert >/dev/null 2>&1; then echo "  ✓ rsvg-convert 已装"; return; fi
  if command -v brew >/dev/null 2>&1; then
    echo "  brew install librsvg（提供 rsvg-convert，推荐）..."
    brew install librsvg || echo "  brew 失败，试 qlmanage（macOS 自带，够用）"
  else
    echo "  无 brew——macOS 可用 qlmanage（系统自带）：qlmanage -t -s 1600 -o /tmp file.svg"
    echo "  或 pip install cairosvg（需 brew install cairo 提供 libcairo）"
  fi
}

check_creds() {
  echo "=== LLM 凭据（agent A/B + 答案质量层需要）==="
  if [ -n "$AB_API_KEY" ]; then echo "  ✓ env AB_API_KEY 已设"; return; fi
  if [ -f ~/.cc-connect/config.toml ]; then
    echo "  ✓ ~/.cc-connect/config.toml 存在（GLM anthropic 兼容端点，本项目默认通路）"
  else
    cat <<'EOF'
  ⚠️ 未找到凭据。agent A/B + 答案质量层（ab-agent/doc-ragas/memory-quality）需 LLM key。两条路：
    1) env AB_API_KEY / AB_BASE_URL / AB_MODEL（推荐 glm：https://open.bigmodel.cn/api/anthropic）
    2) ~/.cc-connect/config.toml 的 [projects.agent.providers]（本项目复用此配置）
  注：检索层（code/doc/cross/memory/ab Stage0）零 LLM，不需凭据。
EOF
  fi
}

case "${1:-help}" in
  python) install_python ;;
  tools) install_tools ;;
  render) install_render ;;
  creds) check_creds ;;
  all) install_python; install_tools; install_render; check_creds ;;
  *) echo "用法: ./setup.sh {python|tools|render|creds|all}"; echo "详见 docs/deployment-runbook.md" ;;
esac
echo "=== 完成。下一步：docs/benchmark-runbook.md（怎么跑 bench）==="

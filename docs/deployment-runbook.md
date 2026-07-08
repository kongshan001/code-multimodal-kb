# 代码 + 多模态知识库 · 部署 Runbook

> **状态（2026-07-08）**：A 代码侧 ✅、B 文档侧 ✅ 均在真实 Godot 上实测通过；LLM 凭据墙已破（复用环境 BigModel/GLM key）。
> 对应 OpenSpec change：`add-code-multimodal-kb`（tasks §6）。
> **范围**：KB（代码 + 文档）；agent 记忆层（Mem0）见 `add-agent-memory` Stage 1（凭据已解锁）。

## 快速接入（一键脚本 · 新设备/新项目通用）

`setup-kb.sh` 把本 runbook 全流程封装成一条命令：

```bash
# 新设备先 git clone 本仓库，再：
./setup-kb.sh --code <代码目录> --docs <文档目录> --name <项目名> [--cmm-mode moderate] [--no-memory]
```

自动：precheck → LLM backend（默认复用环境 BigModel key）→ cmm index 代码 → graphify 建文档图 → agent MCP 注册 → 验证。
- 记忆层（Mem0）需 Docker，V1 未自动化（`--no-memory` 跳过；手动见 `add-agent-memory` §2）。
- graphify-mcp 注册需 venv 装 `mcp` extra（失败见 §B 末）。
- 下文 §0–§C 是全手工步骤/排错；本脚本是它们的封装。

## 0. 前置（task 6.1）

| 项 | 要求 |
|---|---|
| OS | macOS（arm64/amd64）/ Linux / Windows |
| agent | Claude Code / Codex / OpenCode / VS Code / Cursor（任一，install 自动检测） |
| Python + uv | graphify 需要（`uv tool install`） |
| 网络（CN） | 本机代理 `127.0.0.1:7897`（github API/raw 有瞬时抖动，见 FAQ） |

## A. 代码知识库 · codebase-memory-mcp ✅ 已验证

来源：`DeusData/codebase-memory-mcp`（27.7K★，single static binary，tree-sitter + 类型解析，**零 API key、建图不调 LLM**）。

### A.1 锁版本 + 下载（task 6.2 — 禁止 `curl|bash` 抓 main）

```bash
# 查最新 release（走代理；gh 直连 api.github.com 偶发抖动，必走代理）
export HTTPS_PROXY=http://127.0.0.1:7897 HTTP_PROXY=http://127.0.0.1:7897
gh release view -R DeusData/codebase-memory-mcp --json tagName,publishedAt,isPrerelease
# → 锁定 tagName（实测 v0.8.1，2026-06-12，正式版）

ARCH=$(uname -m)                       # arm64→darwin-arm64 / x86_64→darwin-amd64
case "$ARCH" in arm64|aarch64) A=darwin-arm64;; x86_64) A=darwin-amd64;; esac
V=v0.8.1
BASE=https://github.com/DeusData/codebase-memory-mcp/releases/download/$V
F=codebase-memory-mcp-$A.tar.gz
curl -fsSL --retry 3 -o "$F"        "$BASE/$F"
curl -fsSL --retry 3 -o checksums.txt "$BASE/checksums.txt"
```

### A.2 checksum 校验 + 解压 + 签名（task 6.2）

```bash
grep "$F" checksums.txt | shasum -a 256 -c -     # 必须输出 OK
tar -xzf "$F"
BIN=./codebase-memory-mcp
xattr -d com.apple.quarantine "$BIN" 2>/dev/null || true   # 剥 macOS 隔离
codesign --sign - --force "$BIN" 2>/dev/null || true        # ad-hoc 签名
./codebase-memory-mcp --version                            # → 0.8.1
```

### A.3 落位 + 通道验证（task 1.2）

```bash
mkdir -p ~/.local/bin && cp ./codebase-memory-mcp ~/.local/bin/ && chmod +x ~/.local/bin/codebase-memory-mcp
# cli 子命令可直接调工具，无需起 MCP server / 注册 agent：
codebase-memory-mcp cli list_projects '{}'                                  # → projects:[]
codebase-memory-mcp cli index_repository '{"repo_path":"<你的代码仓库>"}'    # 建图
```

实测（graphify 源码，168 文件 / 42 .py）：**2192 节点 / 802 函数 / 4979 边 / 2.6s**。

### A.4 注册到 agent（task 4.1 — 有副作用，先 dry-run）

```bash
codebase-memory-mcp install --dry-run    # 预览：会改哪些 agent 配置 + hooks
codebase-memory-mcp install -y           # 实装（建议先备份 ~/.claude.json 等）
```

**副作用清单**（dry-run 可见）：
- Claude Code：写 `~/.claude.json` + `~/.claude/.mcp.json`；装 **PreToolUse hook**（Grep/Glob search-graph 增强，non-blocking）+ **SessionStart hook** + 1 个 `codebase-memory` skill
- Codex / OpenCode / VS Code：各自 mcp 配置 + instructions（+ Codex SessionStart hook）
- `~/.zshrc`：追加 `~/.local/bin` 到 PATH
- **⚠️ 会删除已建索引要求重建**（install 提示 `Delete these indexes?`）→ 重建即可：`cli index_repository`

回滚：`codebase-memory-mcp uninstall`，或还原 `/tmp/cmm-config-backup/`（本机备份）。

### A.5 验证查询（task 2.2，全不调 LLM）

```bash
codebase-memory-mcp cli search_code      '{"project":"<名>","pattern":"extract","limit":5}'  # 符号定位，带 file:start_line
codebase-memory-mcp cli trace_path       '{"project":"<名>","function_name":"build_from_json"}' # callees+callers 多跳
codebase-memory-mcp cli get_code_snippet '{"project":"<名>","qualified_name":"…"}'           # 完整源码
codebase-memory-mcp cli detect_changes   '{"project":"<名>"}'                                # 增量检测
```

> `query_graph` 吃**结构化 DSL**，不接裸自然语言（裸 NL 报 `expected token type 0`）。NL 检索由 agent 用 `search_code`+`trace_path` 组合完成（design 决策 4）。

## B. 多模态文档知识库 · graphify ✅ 已验证（BigModel/GLM 后端）

来源：graphify（uv tool `graphifyy`，docs-only，**建图标 LLM backend**）。

```bash
uv tool install graphifyy          # 已装 v0.8.46
graphify --version                 # → 0.8.46，无 warning
```

**建图（task 3.1，✅ 已跑通）**——复用环境里 BigModel（智谱）的 Anthropic-compatible 端点，无需另备 Anthropic key：

```bash
export ANTHROPIC_API_KEY=<BigModel key>                              # 复用 ~/.claude.json openspace 的 OPENSPACE_LLM_API_KEY
export ANTHROPIC_BASE_URL=https://open.bigmodel.cn/api/anthropic     # graphify claude backend 读 ANTHROPIC_BASE_URL（非 ANTHROPIC_BASE）
export ANTHROPIC_MODEL=glm-4.6                                       # 覆盖默认 claude 模型名（glm-4.5-air 亦可；glm-4-air 易 429）
graphify <纯文档目录>           # Part A 代码自动跳过；Part B 语义抽取走 BigModel
```

> 实测（3 个 Godot 小文档，2026-07-08）：`found 0 code, 3 docs` → graph.json 13 节点/12 边/4 社区，~$0.027。抽取节点正确（`Node / Node2D / Signal / Vector2 / _ready / connect / emit_signal / add_child …`）。
> **凭据墙已破**：这一把 key 同时解锁文档侧 KB + memory Stage 1（Mem0）+ 文档评测（LLM judge），不再卡。

**起 MCP server（task 1.3，入口是独立命令 `graphify-mcp`，非 `graphify --mcp`）**：

```bash
graphify-mcp --help                # python -m graphify.serve，serve 一个 graph.json
graphify-mcp <graph_path>          # 默认 stdio；--transport http 可起 HTTP
```

> graphify 的 `update`/`watch` 子命令是 AST-only（不跑 Part B 语义），docs-only 增量需 `--update` + LLM，见 design Open Question 1。

## C. 评测环境（task 6.4，可选）

```bash
pip install deepeval               # 文档答案质量（faithfulness/G-Eval）
# 代码侧 harness / 数据集（RepoBench-R、SWE-Lancer-Loc）见 change tasks §5
```

## 验证清单（task 6.5）

- [ ] A：`cli list_projects` 显示已建图项目
- [ ] A：`search_code` / `trace_path` 返回带 `file:start_line` 的结果
- [ ] A：重启 agent 后，`codebase-memory-mcp` 出现在 MCP 工具列表
- [ ] B：（待 LLM 凭据）`graphify <docs>` 产出 `graphify-out/graph.json`
- [ ] B：`graphify-mcp` 能 serve 该图

## FAQ（实测踩坑）

| 现象 | 原因 / 处理 |
|---|---|
| `gh`/curl 报 `error connecting to api.github.com` | github API 瞬时抖动 → `HTTPS_PROXY=http://127.0.0.1:7897` + 重试（实测 3 次内必成） |
| `raw.githubusercontent.com` 超时（CN） | 走代理或 ghproxy 镜像 |
| 二进制首跑被 Gatekeeper 拦 | `install` 自动 `xattr`/`codesign`；手动则 `xattr -d com.apple.quarantine` |
| `install` 后旧索引消失 | install 要求重建索引（提示 `Delete these indexes?`）→ 重新 `cli index_repository` |
| `query_graph` 报 `expected token type 0` | 它吃结构化 DSL，不接裸 NL；用 `search_code`+`trace_path` 代替 |
| 新会话仍看不到 cmm 工具 | MCP 列表在会话启动时加载；`/clear` 或重开 |
| `auto_index=false` | 默认不自动索引；`codebase-memory-mcp config set auto_index true` 按需开 |

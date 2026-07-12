# 代码 + 多模态知识库 · 部署 Runbook

> **状态（2026-07-08）**：A 代码侧 ✅、B 文档侧 ✅ 均在真实 Godot 上实测通过；LLM 凭据墙已破（复用环境 BigModel/GLM key）。
> 对应 OpenSpec change：`add-code-multimodal-kb`（tasks §6）。
> **范围**：KB（代码 + 文档）+ 记忆（Mem0，§D）；均由跨平台 `setup-kb.py` 一键接入。

## 快速接入（一键脚本 · 跨平台 macOS / Linux / Windows）

`setup-kb.py`（Python，工具链本就 Python，**Win 原生可跑**）把本 runbook 全流程封装成一条命令：

```bash
# 新设备先 git clone 本仓库，再（Win/Mac/Linux 通用）：
python3 setup-kb.py --code <代码目录> --docs <文档目录> --name <项目名> [--cmm-mode moderate] [--no-memory]
```

**或交互式管理菜单**（双击进菜单，覆盖全部操作，不用记命令）：
- **Windows**：双击 `setup-kb.bat`（或命令行 `setup-kb.bat`）
- macOS / Linux：`./setup-kb.sh`
- 任意平台：`python3 setup-kb.py --interactive`

菜单：`[1] 环境检查/自动安装工具` · `[2] 接入/初始化项目` · `[3] 查看已接入(状态)` · `[4] 查询某项目代码` · `[5] 删除某项目` · `[6] 退出`。**新设备先跑 `[1]`**：自动装 cmm(下载二进制)+graphify(uv，含 mcp extra)+uv，检查 Python/claude/docker。所有用户需求都在菜单里完成。

自动 6 步：precheck → LLM backend（默认复用环境 BigModel key）→ cmm index 代码 → graphify 建文档图 → [Mem0 docker compose] → agent MCP 注册 + 验证。
- 已实测：1-4 + 6 步在全新靶子上真跑零 bug（cmm index + graphify 建图 + 注册）。
- Mem0（第 5 步）：`--memory-mode local`（Ollama+qdrant，**已实测通过** add→search）/ `docker`（未测，本机无 Docker）/ `none` 跳过。
- graphify-mcp 注册需 venv 装 `mcp` extra（失败见 §B 末）。
- 下文 §0–§D 是全手工步骤/排错；本脚本是它们的封装。（旧 `setup-kb.sh` 已由 `.py` 取代。）

### 操作清单（日常）
| 操作 | 命令 |
|---|---|
| 初始化某项目 | `python3 setup-kb.py --code <代码路径> --name <标签> --no-memory`（有文档加 `--docs <文档目录>`）|
| 交互式初始化 | Win 双击 `setup-kb.bat` / Mac·Linux `./setup-kb.sh` |
| 查已初始化哪些 | `python3 setup-kb.py --status`（cmm 已索引项目 + 文档图 + MCP 注册）|
| CLI 查某项目 | `codebase-memory-mcp cli search_code '{"project":"<--status 里的项目名>","pattern":"关键词"}'` |
| 删某项目 | `codebase-memory-mcp cli delete_project '{"project":"<项目名>"}'` |

> **项目名**：cmm 的项目名是**从代码路径自动派生**的长名（如 `Users-ks_128-...-src`），查询用它，从 `--status` 输出复制；`--name` 只用于 graphify MCP 注册标签。重复初始化是**增量**的（只更新改动文件），安全。

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

## D. 记忆层 · MemPalace（实测 2026-07）

> 选型 MemPalace（替换 Mem0，[design D2](../openspec/changes/add-agent-memory/design.md)）：`uv install` + ChromaDB embedded（零外部服务/零 Docker）+ 核心零 LLM（解绑凭据墙）+ 内置 temporal KG（吸收 Stage 2）。原 Mem0 Docker 路线（`deploy/mem0*`）弃用留历史。

### D.1 安装（仅官方源 GitHub/PyPI/mempalaceofficial.com，防 impostor）

```bash
uv tool install --python 3.11 mempalace      # Intel Mac 必须 py3.11（onnxruntime 无 x86_64 新 wheel）
mempalace --version                           # → MemPalace 3.5.0
```

> **Intel Mac 约束**（实测 i7-5650U）：chromadb 1.5.x → onnxruntime，新版无 macOS x86_64 wheel、旧版无 cp312/cp313 → 必须 Python 3.11（onnxruntime 1.16.3 有 cp311 + macOS x86_64）。ARM Mac / Linux 可 3.12/3.13。uv tool 隔离环境，不碰系统 Python。

### D.2 初始化 palace

```bash
mempalace init <项目目录> --yes --no-llm      # --no-llm: heuristics-only 零 LLM（契 D4）
# → 建 ~/.mempalace/（config.json + palace/），探测项目生成 wing/room
# → 项目根生成 mempalace.yaml；.gitignore 自动加 mempalace.yaml/entities.json
```

### D.3 MCP 注册到 agent（user scope 全局）

```bash
claude mcp add mempalace -s user -- /Users/<user>/.local/bin/mempalace-mcp   # 绝对路径不依赖 PATH
claude mcp list | grep mempalace                                             # → mempalace ✔ Connected
```

> 下个会话 agent 可调 `mcp__mempalace__*`（35 工具：palace reads/writes、KG、cross-wing、drawer、diary）。当前会话 MCP 已加载，新会话生效。

### D.4 auto-save hooks（`~/.claude/settings.json`）⚠️ 当前已禁用

**原配置**（已禁，见下）：
```json
{"hooks":{
  "Stop":[{"matcher":"","hooks":[{"type":"command","command":"/Users/<user>/.local/bin/mempalace hook run --hook stop --harness claude-code"}]}],
  "PreCompact":[{"matcher":"","hooks":[{"type":"command","command":"/Users/<user>/.local/bin/mempalace hook run --hook precompact --harness claude-code"}]}]
}}
```

**⚠️ 2026-07-12 禁用原因（实测事故）**：`mempalace hook run --hook stop` **非 idempotent**——每次 Stop 都把
**整个会话 transcript** re-mine 进 palace。Stop hook 是全局的（作用于所有 Claude Code 会话），导致**别项目
的会话也被 mine 进同一 palace**。实测 palace 从 1485 drawers 膨胀到 14605（sessions wing 13115 全是另一项目
的 Unity 代码碎片），**记忆召回 hit@5 从 0.933 跌到 0.6**（被噪声淹没）。

**禁用**：清空 settings.json 的 Stop/PreCompact mempalace 条目（保留 SessionStart/PreToolUse 等无关 hook）：
```bash
cp ~/.claude/settings.json /tmp/settings.json.bak.$(date +%s)   # 备份（可逆）
# 编辑：把 hooks.Stop / hooks.PreCompact 的数组清空为 []（结构保留，命令移除）
```

**当前状态**：auto-save 暂停——跨会话记忆**不自动持久化**。memory 文件（`memory/*.md`）仍在磁盘不受影响；
需要持久化会话记忆时走 **D.6 手动 sweep**（idempotent）。

### D.6 手动持久化 / 恢复 auto-save（idempotent 路径）

**手动按需存（idempotent，不重复）**——重要会话后跑：
```bash
# sweep 是 message-level、timestamp-coordinated、idempotent（只存增量，不重复 mine）
mempalace sweep ~/.claude/projects/-Users-ks-128-Documents-engineer-demo/   # 扫该项目的会话 jsonl，增量入库
mempalace status                                                            # 验 drawer 数（应稳定，不爆涨）
```
> `sweep` 吃 jsonl 文件/目录，不走 hook stdin——所以能 idempotent。`hook run --hook stop` 走 stdin、非幂等，故弃用。

**恢复 auto-save 的条件**（待 mempalace 上游）：
- 等 `mempalace hook run --hook stop` 改成 idempotent（或新增 `--hook sweep` 之类幂等 hook 入口）
- 验证方法：开 hook 后跑一个长会话、多次 Stop，`mempalace status` 看 drawer 数是否**只随会话内容增长、不随 Stop 次数翻倍**
- 验证通过再把 D.4 的 Stop/PreCompact 配回去

**临时自检**（确认 palace 没再膨胀）：每周 / 长会话后 `mempalace status`，drawer 数应与内容量正相关，**Stop 次数不应让它翻倍**。

### D.5 验证 / 排错 / 回滚

```bash
mempalace status                                  # palace 概览（mine 后有 chroma.sqlite3）
mempalace mine ~/.claude/projects/ --mode convos  # backfill 历史会话（task 2.4）
mempalace wake-up                                 # 新会话召回（前摄铺垫，D1）
```

| issue | 现象 | 解 |
|---|---|---|
| Intel Mac onnxruntime | py3.12/3.13 装失败 | `--python 3.11` |
| #74 ARM64 segfault | M 系列导入崩 | pin chromadb（见 issue） |
| #100 chromadb 冲突 | 版本解析失败 | pin 范围 / 切 `sqlite_exact` 后端 |
| #110 hook injection | hook 路径不信任 | 仅官方 hook 路径，不喂不受信输入 |
| **Stop hook 非 idempotent**（2026-07 实测） | palace 爆涨（1485→14605）、召回掉（hit@5 0.933→0.6）| 禁 hook（D.4）+ 重置 palace（擦→init→mine）+ 手动 sweep（D.6）。详见 memory-baseline §7 |

**回滚**：`claude mcp remove mempalace -s user` + 还原 `settings.json` 备份 + `uv tool uninstall mempalace` + `rm -rf ~/.mempalace`。

## F. 前端可视化 · Measurement Lab（2026-07 新增）

### 起前端（零额外依赖）
```bash
python -m eval.cli web --port 8765      # 或 bench web（加 alias）
# → http://127.0.0.1:8765
```
后端是 stdlib http.server（零依赖），前端是 vanilla JS SPA（无构建）。
API 路由：`/api/reports`（归档）、`/api/health`（依赖体检）、`/api/run`（触发评测）、`/api/goldgen*`（扩题）、`/api/onboard`（索引/建图/会话）。

### 8 个视图
| 视图 | 功能 |
|---|---|
| Dashboard | 4 hero 指标（代码/记忆/A/B/答案质量）+ 最近 run |
| Run console | 选 subject + 参数 → 触发评测 → 看结果 |
| Reports | 16 份归档列表，点行进 detail |
| Detail | aggregate + per_query + lockfile |
| Compare | 两份报告 aggregate diff |
| Setup | 依赖体检表 + 健康门禁 |
| Onboarding | 5 步向导：索引/文档图/会话/gold/就绪 |
| Gold lab | 扩题全流程：挖拟题→验收→人审→fold |

### 关闭
`Ctrl-C` 停服务。前端不改后端——CLI 仍是自动化通路。

## E. 离线 / 内网部署（无外网）

内网无外网时，`deploy.sh/.bat` 联网装依赖会失败——脚本会逐项打印 `❌...离线补救`（怎么备、拷哪）。下面是一次性预置清单：有网机备好 → U盘/内网拷入 → 重跑 deploy。

### 预置清单（有网机备，拷入内网）
| 依赖 | 有网机怎么备 | 内网放哪 |
|---|---|---|
| **cmm 二进制** | github.com/DeusData/codebase-memory-mcp/releases 下 v0.8.1（选对应平台）| `~/.local/bin/codebase-memory-mcp` + `chmod +x` |
| **pip 包**（mem0ai/qdrant-client/ollama/mcp）| `pip download mem0ai qdrant-client ollama mcp -d ./wheels` | `pip install --no-index --find-links=./wheels mem0ai qdrant-client ollama mcp` |
| **graphify** | `uv tool install graphifyy --with mcp`（装好）| 拷 `~/.local/share/uv/tools/graphifyy` 整目录过来 |
| **ollama 二进制** | ollama.com 下载 | 装上（mac .app / linux 二进制 / win winget） |
| **ollama 模型** | `ollama pull nomic-embed-text` + `ollama pull llama3.2` | 拷 `~/.ollama/models` 到内网机同名目录 |
| Python 3.12+ / Claude Code | 预装 | — |

### 流程
1. 内网机跑 `./deploy.sh <项目>`（或 `deploy.bat`）→ 看哪些依赖 ❌（联网装失败）。
2. 按 ❌ 提示（或上表）在有网机备好，拷入内网对应位置。
3. 重跑 `./deploy.sh <项目>` → 装齐 → 自动接入（代码 index + 文档图 + 本地记忆 + 注册）。

### 离线能用到的程度
- **代码 KB（cmm）= 完全离线可用**（纯 tree-sitter 结构索引，零网络零 LLM，二进制预置即可）✅
- **文档 KB（graphify）/ 记忆（Mem0）= 本地 Ollama 驱动**（模型预置，不走 BigModel 云）✅
- ⚠ 若无本地 Ollama + 模型：只能用代码 KB（文档/记忆不可用）。LLM 抽取无法绕过 Ollama。

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

## 1. Stage 0：边界落地与文件记忆加固（零凭据·零新工具）

- [x] 1.1 把 D1 四层归属规则 + 判定测试（"忘了这条 agent 会不会被纠正"）写入 `CLAUDE.md` 作为强制纪律 — 新建项目级 `CLAUDE.md`（repo 根，git 跟踪），含四层归属表 + 判定测试金句 + 范围边界
- [x] 1.2 给文件记忆设分类纪律：每条 fact 的 frontmatter `type` 限定为 user/feedback/project/reference 之一；为 MEMORY.md 索引设容量上限规则 — 写入项目 `CLAUDE.md`「分类纪律」(type 四选一, 无匹配则拒) +「容量上限」(~20 条, 超限降级为按需召回, Stage 1 后失效)；实测 MEMORY.md 现 3 条远低于上限
- [x] 1.3 建决策→情景锚机制：决策型 memory 条目 MUST 附带 git commit 或 tasks 条目引用 — 规则入 `CLAUDE.md`「决策锚」；演示: 新写 `memory/agent-memory-approach.md` (type: project) 锚 commit `daf359b` + tasks §2，并在 MEMORY.md 加索引行
- [x] 1.4 端到端验证 Stage 0 → 验证：新会话启动时相关偏好被正确铺垫；构造 4 条候选事实（客观/程序/事件/主观各一）按判定测试全部正确路由 — 铺垫: MEMORY.md 本会话已注入上下文（2 条原条目可见），新条目下会话生效；路由 4 案全对：①"cmm search_code ~112ms"→否→KB/cmm ②"部署 cmm 步骤"→否→程序/runbook ③"7/7 完成 task 4.1"→否→情景/commit 6ae72e5 ④"用户偏好全局工具"→**是**→memory/✓；实测 memory/ 仅含 project/feedback（主观），无客观/程序/情景泄漏

## 2. Stage 1：MemPalace 接入（核心零 LLM·不卡凭据）

> 2026-07 修订：Mem0 → MemPalace（design D2/D3/D4）。理由：部署成本（pip + ChromaDB embedded vs 3 容器）+ 核心零 LLM（解绑凭据墙）+ 内置 temporal KG（吸收 Stage 2）。

- [x] 2.1 装 MemPalace（`uv tool install mempalace`，仅官方源 PyPI）+ `mempalace init` → 验证：**MemPalace 3.5.0**（`uv tool install --python 3.11 mempalace`——Intel Mac i7-5650U 实测：onnxruntime 新版无 macOS x86_64 wheel、旧版无 cp312/cp313，必须 py3.11）+ `mempalace init engineer_demo --yes --no-llm` → palace 生成（`~/.mempalace/config.json` + palace/，wing/room: eval/openspec/testing/planning/general）✓
- [x] 2.2 MCP 注册到 agent（`claude mcp add mempalace -s user -- /Users/ks_128/.local/bin/mempalace-mcp`，绝对路径不依赖 PATH）→ 验证：`claude mcp list` = **mempalace ✔ Connected**（server 启动 OK，空 palace 也能起）；下个会话 agent 可调 `mcp__mempalace__*`（当前会话 MCP 已加载、新会话生效）✓
- [x] 2.3 配置 auto-save hooks（Stop / PreCompact 写入 `~/.claude/settings.json`：`mempalace hook run --hook <stop|precompact> --harness claude-code`，绝对路径；备份 `/tmp/settings.json.bak.*`）→ 验证：`echo '{}' | mempalace hook run --hook stop` exit=0 graceful（不阻断会话）；实际入库待新会话 Stop 触发后 `mempalace status` 验（归 2.5 联调）✓
- [x] 2.4 backfill engineer_demo 会话进 palace（`mempalace mine ~/.claude/projects/-Users-ks-128-Documents-engineer-demo/ --mode convos` → **1484 drawers**：technical 1382 / architecture 83 / planning 19）→ 验证：`mempalace search "记忆层 MemPalace 替换 Mem0"` 召回 `agent-memory-approach.md`（cosine_sim=0.529, bm25=1.462）+ 本次会话 jsonl ✓；全量 mine（所有项目）可选，留用户决定
- [x] 2.5 端到端联调 → 验证：MemPalace search 召回主观记忆 work（见 2.4）；KB（cmm/graphify）走各自 MCP server 天然隔离、不污染；agent 内 `mcp__mempalace__*` 新会话生效（`claude mcp list` = ✔ Connected）✓
- [x] 2.6 部署 issue 防护：官方源（防 impostor）+ runbook 排错表（Intel Mac py3.11 / #74 / #100 / #110 / `sqlite_exact` 后端）→ 本机 Intel Mac 用 py3.11 解 onnxruntime（非 pin chromadb）；runbook §D.5 沉淀 ✓

## 3. Stage 2：时序召回（先 MemPalace KG，不够再上 Zep）

> 2026-07 修订：MemPalace 内置 temporal KG（SQLite，validity windows），先评估它是否够；不足才引 Zep/Graphiti。

- [ ] 3.1 用 MemPalace temporal KG 做决策/事件时序召回（`KnowledgeGraph.add_triple/query_entity/invalidate`，带 valid_from/ended）→ 验证：按时间线/实体回溯某决策脉络，结果带 validity window
- [ ] 3.2 触发评估：仅当 MemPalace KG 不足（如需跨实体复杂时序推理）才启动 Zep/Graphiti（Neo4j/FalkorDB）+ MCP 注册 → 验证：Zep 时序图建图 + MCP 工具可调；否则跳过

## 4. 评测（记忆召回质量基线）

> **归属**：记忆评测归横切变更 `add-evaluation-baseline` §4；本节为历史 task，实际进度以该变更为准。
> 2026-07 修订：subject 从 Mem0 换 MemPalace。MemPalace 核心零 LLM，可复现性更易（无抽取非确定）。

- [ ] 4.1 评测 harness：封装"调 MemPalace search 收集 (query, 召回结果, gold)"，锁定 backend 版本（chromadb / embedding 模型）保证可复现
- [ ] 4.2 召回质量指标：recall@k / 命中率 + 实体去重正确率 + 注入体积收敛曲线（verbatim 不遗忘，体积收敛是关键）
- [ ] 4.3 边界正确率：候选事实（主观/客观/程序/事件）路由准确率，验证 D1 归属规则可操作
- [ ] 4.4 verbatim 召回质量实测：本项目对话风格下 raw 模式 recall，评估需否 hybrid rerank（需 LLM）

## 5. 部署与文档

- [x] 5.1 runbook §D 重写：MemPalace 安装（`uv install --python 3.11`）+ init + MCP 注册 + auto-save hooks + 排错表（Intel Mac py3.11 / #74 / #100 / #110）+ 回滚 → `docs/deployment-runbook.md` §D（基于 2.1/2.2/2.3 实测命令）✓
- [ ] 5.2 把 D1 边界纪律 + Stage 0/1/2 路线沉淀进 `docs/deployment-runbook.md` 与 `CLAUDE.md`；标注 `deploy/mem0*` 为弃用历史

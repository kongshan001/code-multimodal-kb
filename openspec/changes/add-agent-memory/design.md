## Context

agent（Claude Code 经 cc-connect 桥跨多会话运行）需要跨会话"记忆"，但当前是 **5 个互不连通的记忆孤岛**：

```
工作记忆      语义-客观         情景           程序         语义-主观
context win   cmm + graphify   git+tasks.md   skills/      MEMORY.md
(会话即失)    (KB项目进行中)   (人工翻·散落)  (静态SOP)    (仅2条·全量注入)
```

两个真实缺口：
1. **语义-主观层太薄**——MEMORY.md 全量注入会随事实增长无限膨胀、无相关性召回、靠人手写
2. **情景不可主动召回**——关键决策散落在 git commit / tasks.md，agent 不会主动"想起上次定的事"，每次靠人提醒

关键约束：本机**无 LLM 凭据**——这同时卡住 doc-side graphify 与任何需 LLM 抽取的记忆方案。**2026-07 修订**：选型从 Mem0 改为 **MemPalace**（核心路径零 LLM），Stage 1 **不再卡凭据墙**（见 D2/D4）。

参考架构现状（2026-07 调研）：MemPalace（19.5K★，MCP + ChromaDB embedded + 内置 temporal KG，核心零 LLM）/ Mem0 / Letta(MemGPT) / Cognee / Zep(Graphiti) 均有 MCP server，适配性差异巨大（见 D2/D3）。

## Goals / Non-Goals

**Goals:**
- 把"记忆"确立为与 KB / skills / git 并列、职责清晰的一层，附归属判定规则
- Stage 0 零凭据即产出可用价值（加固文件记忆 + 把情景源接成可指回）
- Stage 1 用成熟 MCP（**MemPalace**）把主观记忆从"手动全量注入"升级为"自动入 palace + 相关性召回"
- 沿用复用原则：不建网关、不引平台、几乎零自建代码

**Non-Goals:**
- 不替换/不碰 cmm（代码）与 graphify（文档内容）——它们是客观层，记忆是主观层
- 不自建记忆引擎（向量库 / 图引擎一律复用成熟实现）
- 不做跨用户/多租户记忆（单用户、本地优先）
- Stage 2（Zep 时序召回）非必须——MemPalace 内置 temporal KG 先顶，不足才上 Zep
- 不继续 Mem0 路线（`deploy/mem0*` 标记弃用历史）

## Decisions

### D1 — 四层归属规则 + 判定测试（核心）

| 层 | 载体 | 召回方式 | 归属判定 |
|---|---|---|---|
| 工作 | context window | 隐式 | 当前任务，会话结束即失 |
| 情景 | git log + tasks.md | 人工/检索 | "何时做了何事"（事件、决策时间线） |
| 程序 | skills/ | 显式调用 | "如何做某类事"（SOP） |
| 语义-客观 | KB：cmm / graphify | 反应式查询 | 关于代码/文档的**客观事实** |
| 语义-主观 | Memory（文件 → MemPalace） | 前摄式铺垫 | 关于**用户/工作方式/决策**的主观事实 |

**一句话边界**：KB = 反应式查询（被问到才查，客观）；记忆 = 前摄式铺垫（主动召回以防犯错，主观）。

**判定测试**（一条事实该进哪层）：
> "忘了这条，agent 会不会做出用户必须纠正的事？" 会 → Memory；不会但要被问起 → KB；讲怎么做 → Skill；讲何时发生 → git/tasks。

**Alternatives**：把记忆并入 KB（用 graphify/cmm 同时存主观事实）——否决，因客观/主观召回模式不同（反应式 vs 前摄式），混存会污染 KB 检索精度且 MEMORY.md 注入语义无法表达。

### D2 — 复用 MemPalace（替换 Mem0）而非自建

沿用 `add-code-multimodal-kb` 确立的"复用成熟 MCP + 注册到 agent"原则。**MemPalace**（[github.com/MemPalace/mempalace](https://github.com/MemPalace/mempalace)，MIT，19.5K★，2026-04 爆红）是 local-first AI agent 记忆系统：MCP server（35 工具）+ ChromaDB **embedded**（零外部服务）+ 内置 temporal KG，专为给 MCP agent 加持久主观记忆设计。

**为何替换 Mem0**（2026-07 修订，原 D2 选 Mem0）：

| 维度 | Mem0（原选） | MemPalace（现选） |
|---|---|---|
| 外部服务 | API + Postgres/pgvector + Neo4j（3 容器）或 Qdrant+Neo4j+Ollama | **零**（ChromaDB embedded，~300MB 磁盘）|
| 安装 | Docker compose | `uv tool install mempalace` 一条 |
| LLM 凭据 | 抽取必需（卡凭据墙） | **核心路径零 LLM**（LongMemEval R@5 raw 96.6% 不调 LLM）|
| 时序 KG | 无（Stage 2 另接 Zep） | **内置 temporal KG**（SQLite，validity windows）|
| 范式 | extract 成结构化事实条目 | verbatim 存对话原文 + 语义检索 |

部署成本显著更低 + 解绑凭据墙（D4）+ 内置 temporal KG 吸收 Stage 2（D3），三重收益。

**范式代价（诚实记录）**：MemPalace verbatim 存对话原文，不 extract 成"事实条目"。D1 的"主观层=前摄式铺垫"仍成立（`wake-up` 注入相关片段），但 spec 的"四分类(user/feedback/project/reference)"落地从"meta 标签"变"MemPalace wing/room 结构 + `mine --extract general`(decisions/preferences/milestones/problems/emotional) 5 类"——后者语义覆盖前者，spec 仍满足，召回过滤维度更细。

**Alternatives**：
- 自建轻量记忆（SQLite + 手写召回）——否决，召回质量（向量相似 + 实体去重 + 衰减）自己实现成本高、偏离复用路线
- 继续 Mem0——否决，3 容器 + 凭据墙在无 Docker/无 LLM key 环境实测阻塞（`deploy/mem0/` compose 未实测、`deploy/mem0-local/` 闭环但未接 agent）
- Cognee / Letta——见 D3 排除

### D3 — 排除 Cognee 与 Letta；MemPalace temporal KG 吸收 Stage 2

- **Cognee**：架构上"摄入任意数据 → 建 KG"，与 graphify **同物撞车**，会出现两个竞争性文档/数据 KG。→ 出局（不变）
- **Letta / MemGPT**：记忆要求 agent 运行在 Letta 运行时内（自管理分页 / memory editing），Claude Code 架构错配。→ 出局（不变）
- **MemPalace 不撞上述排除**：它存对话 verbatim（主观层），不建文档/数据 KG（不撞 graphify）；是 stdio MCP server（不要求 agent 跑在其内）。→ 采用
- **Zep / Graphiti**（修订）：原留作 Stage 2。MemPalace **内置 temporal entity-relationship graph**（SQLite，validity windows，免费 Graphiti 替代），已覆盖"实体+关系+时间线"的情景时序召回。→ Stage 2 降级为"评估 MemPalace temporal KG 是否够；不足再上 Zep"，默认不引 Neo4j/FalkorDB

### D4 — 凭据时序：MemPalace 核心零 LLM，Stage 1 解绑凭据墙

Mem0 抽取必需 LLM（原 D4 与 doc-side graphify 共享 key）。**MemPalace 核心路径零 LLM**（verbatim 存储 + 语义检索，raw 模式不调任何 LLM；hybrid rerank 才可选 LLM）。→ Stage 1 **不再卡凭据墙**，可独立于 doc-side KB 推进。

凭据仅当启用 MemPalace 的 LLM rerank / extract extras 时才需要，且仍可复用 doc-side key（不引入新凭据来源）。

### D5 — 范围边界：只管主观层

记忆层只存"用户 / 决策 / 工作情景"。**不碰代码**（归 cmm）、**不碰文档内容**（归 graphify）。跨层协作走"锚定"模式（概念在文档图锚定 → 抽真实标识符 → 交 cmm 定位），与 `code-knowledge-base` spec 的 anchoring 要求一致，不在记忆层重复存储客观内容。

## Risks / Trade-offs

- **[MEMORY.md 全量注入膨胀]** → Stage 0 已设容量上限 + 分类；Stage 1 改 MemPalace `wake-up` 相关性召回后该问题消失
- **[主观/客观边界灰区]**（如"我们决定用 MemPalace"既是决策也是事实）→ D1 判定测试兜底：默认进 Memory（主观），KB 只收"代码/文档本身说了什么"
- **[MemPalace verbatim 范式代价]**（替换 Mem0 的 trade-off）：不 extract 成事实条目，召回是"相关原文片段"而非"结构化事实"。→ spec 四分类由 MemPalace wing/room + extract-general 5 类覆盖；决策型记忆仍附情景锚（spec req 5 不变）
- **[MemPalace 已知部署 issue]**：macOS ARM64 segfault（Issue #74，pin chromadb）、chromadb 版本冲突（#100）、hook shell injection（#110）。→ runbook 沉淀 pin 版本 + 仅信任 hook 路径；可切 `sqlite_exact` 后端绕开 chromadb
- **[impostor 站点]**：MemPalace 仅 GitHub / PyPI / mempalaceofficial.com 官方源，其他域名（`.tech`/`.net`/其他 `.com`）可能恶意。→ runbook 明确只从官方装
- **[LLM 抽取质量决定记忆质量]**（仅当启用 extract/rerank extras）→ 抽取模型锁定版本 + 抽样校验；核心 raw 路径零 LLM 不受影响
- **[Stage 0 文件记忆纪律靠人遵守]** → Stage 1 auto-save hooks（Stop/PreCompact）后自动化；Stage 0 过渡期写 CLAUDE.md 纪律

## Migration Plan

```
Stage 0（已完成·零凭据·零新工具）
  ① 边界模型落 spec + 写 CLAUDE.md 纪律 ✓
  ② 加固文件记忆：分类 + 容量上限 + 决策锚 ✓
  → 回滚：删纪律、还原 MEMORY.md

Stage 1（MemPalace·核心零 LLM·不再卡凭据）
  ③ `uv tool install mempalace` + `mempalace init` → MCP 注册到 agent（`claude mcp add` 或 plugin install）
  ④ 配置 auto-save hooks（Stop 每 15 条 / PreCompact 压缩前）→ 对话自动入 palace
  ⑤ backfill 现有 MEMORY.md + ~/.claude/projects 会话进 palace（`mempalace mine --mode convos`）；召回从全量注入切到 `wake-up` 相关性召回
  → 回滚：停 MCP + hooks、回退文件记忆

Stage 2（可选·MemPalace temporal KG 不足时）
  ⑥ 先用 MemPalace 内置 temporal KG 做决策/事件时序召回；评估不足才上 Zep/Graphiti（Neo4j）
```

## Open Questions

- 记忆的**衰减/遗忘策略**：MemPalace verbatim 不自动遗忘，长期膨胀？需否定期 `sweep` / `invalidate`？（Stage 1 落地时定）
- **决策该落 Memory 还是 git**：当前两者都留锚（git 留事件、Memory 留"决策结论+为何"），是否过度？（Stage 0 已完成，待评估）
- 是否需要**跨 agent 共享**记忆：MemPalace 支持 multi-wing specialist agents，Codex/Cursor 等是否各自 wing？（Stage 1 时定）
- **verbatim 召回质量实测**：raw 96.6% 是 LongMemEval，本项目对话风格下需否 hybrid rerank（需 LLM）？（Stage 1 落地后评测，归 `add-evaluation-baseline` §4）

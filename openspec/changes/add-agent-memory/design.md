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

关键约束：本机**无 LLM 凭据**——这同时卡住 doc-side graphify（见 `add-code-multimodal-kb`）与任何需要 LLM 抽取的记忆方案。因此记忆方案必须**分阶段**，且 Stage 1 与 doc-side KB **共享同一凭据解锁**。

参考架构现状（2026 调研）：Mem0 / Letta(MemGPT) / Cognee / Zep(Graphiti) 均有 MCP server，但适配性差异巨大（见 D3）。

## Goals / Non-Goals

**Goals:**
- 把"记忆"确立为与 KB / skills / git 并列、职责清晰的一层，附归属判定规则
- Stage 0 零凭据即产出可用价值（加固文件记忆 + 把情景源接成可指回）
- Stage 1 用成熟 MCP（Mem0）把主观记忆从"手动全量注入"升级为"自动抽取 + 相关性召回"
- 沿用复用原则：不建网关、不引平台、几乎零自建代码

**Non-Goals:**
- 不替换/不碰 cmm（代码）与 graphify（文档内容）——它们是客观层，记忆是主观层
- 不自建记忆引擎（向量库 / 图引擎一律复用成熟实现）
- 不做跨用户/多租户记忆（单用户、本地优先）
- Stage 2（Zep 时序召回）非必须，仅在情景召回成为真实痛点时启动

## Decisions

### D1 — 四层归属规则 + 判定测试（核心）

| 层 | 载体 | 召回方式 | 归属判定 |
|---|---|---|---|
| 工作 | context window | 隐式 | 当前任务，会话结束即失 |
| 情景 | git log + tasks.md | 人工/检索 | "何时做了何事"（事件、决策时间线） |
| 程序 | skills/ | 显式调用 | "如何做某类事"（SOP） |
| 语义-客观 | KB：cmm / graphify | 反应式查询 | 关于代码/文档的**客观事实** |
| 语义-主观 | Memory（文件 → Mem0） | 前摄式铺垫 | 关于**用户/工作方式/决策**的主观事实 |

**一句话边界**：KB = 反应式查询（被问到才查，客观）；记忆 = 前摄式铺垫（主动召回以防犯错，主观）。

**判定测试**（一条事实该进哪层）：
> "忘了这条，agent 会不会做出用户必须纠正的事？" 会 → Memory；不会但要被问起 → KB；讲怎么做 → Skill；讲何时发生 → git/tasks。

**Alternatives**：把记忆并入 KB（用 graphify/cmm 同时存主观事实）——否决，因客观/主观召回模式不同（反应式 vs 前摄式），混存会污染 KB 检索精度且 MEMORY.md 注入语义无法表达。

### D2 — 复用 Mem0 而非自建

沿用 `add-code-multimodal-kb` 确立的"复用成熟 MCP + 注册到 agent"原则。Mem0 / OpenMemory MCP 是专为"给 MCP agent 加持久主观记忆"设计、自托管、向量+图双存储，直接对接 Claude Code。

**Alternatives**：自建轻量记忆（SQLite + 手写召回）——否决，召回质量（向量相似 + 实体去重 + 衰减）自己实现成本高、且偏离已验证的复用路线。

### D3 — 排除 Cognee 与 Letta（附理由）

- **Cognee**：架构上"摄入任意数据 → 建 KG"，与 graphify **同物撞车**。若同时引入，会出现两个竞争性文档/数据 KG，职责无法切分。→ 出局
- **Letta / MemGPT**：其记忆**要求 agent 运行在 Letta 运行时内**（自管理分页 / memory editing）。Claude Code 不在 Letta 内运行，架构错配；强行接入只能用其 MCP 皮，拿不到核心价值。→ 出局
- **Zep / Graphiti**：时序知识图，强在"实体 + 关系 + 时间线"，是**情景层**的优质补强，但需要 Neo4j/FalkorDB，偏重。→ 留作 Stage 2 可选，不进 Stage 1

### D4 — 凭据时序：与 doc-side KB 共享解锁

Mem0 抽取 / Zep 建图均需 LLM。本变更**不引入额外凭据来源**：Stage 1 复用 doc-side graphify 同一把 LLM key。即用户提供一次凭据 → doc-side KB 与 agent 记忆**同时解锁**。

### D5 — 范围边界：只管主观层

记忆层只存"用户 / 决策 / 工作情景"。**不碰代码**（归 cmm）、**不碰文档内容**（归 graphify）。跨层协作走"锚定"模式（概念在文档图锚定 → 抽真实标识符 → 交 cmm 定位），与 `code-knowledge-base` spec 的 anchoring 要求一致，不在记忆层重复存储客观内容。

## Risks / Trade-offs

- **[MEMORY.md 全量注入膨胀]** → Stage 0 即设容量上限 + 分类；Stage 1 改向量召回后该问题消失
- **[主观/客观边界灰区]**（如"我们决定用 Mem0"既是决策也是事实）→ D1 判定测试兜底：默认进 Memory（主观），KB 只收"代码/文档本身说了什么"
- **[Mem0 自托管运维成本]**（Docker 多容器）→ 复用 KB 项目已建立的 runbook 模式；全本地栈（Qdrant+Neo4j+Ollama）作为无云依赖退路
- **[LLM 抽取质量决定记忆质量]** → 抽取模型锁定版本 + 抽样人工校验（同 graphify 的评测思路，归 §后续评测）
- **[Stage 0 文件记忆纪律靠人遵守]** → 写入 CLAUDE.md / skill 作为强制纪律，降低人为遗漏

## Migration Plan

```
Stage 0（现在·零凭据·零新工具）
  ① 边界模型落 spec（本变更）+ 写 CLAUDE.md 纪律
  ② 加固文件记忆：分类 user/feedback/project/reference + MEMORY.md 容量上限 + 决策显式落 memory 并在 git/tasks 留锚
  → 回滚：删纪律、还原 MEMORY.md

Stage 1（凭据到位·与 doc-side KB 同解锁）
  ③ 自托管 Mem0/OpenMemory MCP（Docker 或全本地栈）→ 注册到 agent
  ④ 迁移现有 MEMORY.md 事实进 Mem0；召回从全量注入切到相关性召回
  → 回滚：停 MCP、回退文件记忆

Stage 2（可选·情景召回成真痛点时）
  ⑤ Zep/Graphiti（Neo4j/FalkorDB）做决策/事件时序图召回
```

## Open Questions

- 记忆的**衰减/遗忘策略**：保留期多长、何时合并/淘汰旧事实？（Stage 1 落地时定）
- **决策**该落 Memory 还是 git：当前两者都留锚（git 留事件、Memory 留"决策结论+为何"），是否过度？（Stage 0 试行后评估）
- 是否需要**跨 agent 共享**记忆（Codex/Cursor 等已注册 cmm 的 agent 是否也接 Mem0）？（Stage 1 时按 `add-code-multimodal-kb` task 4.x 的多 agent 注册模式决定）

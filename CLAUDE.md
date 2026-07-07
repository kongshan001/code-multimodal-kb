# engineer_demo — agent 纪律

本仓库是**规格仓库**（承载 openspec 变更：`add-code-multimodal-kb`、`add-agent-memory`），无源码。所有产出是 spec / 设计 / 文档 / 配置；改动一律提交 main + push（带 Co-Authored-By）。

## 铁则：新需求一律走 OpenSpec

**所有非琐碎需求 MUST 经 OpenSpec 推进**——先 spec 后码，不直接写实现、不口头推进：

| 阶段 | 做什么 | skill |
|---|---|---|
| 探索 / 调研 | 想清楚再动 | `openspec-explore` |
| 立项 | 生成 proposal / design / specs / tasks | `openspec-propose` |
| 实施 | 逐 task 落地，完成的带验证证据 | `openspec-apply-change` |

**例外**（可直接做，不必开变更）：单行修复、笔误、读文件、回答问题、跑命令、整理文档。

## Memory 纪律（来自 `add-agent-memory` D1）

记忆是独立于 KB / skills / git 的**一层**。每遇到一条候选事实，先按四层归属路由，再决定写入哪：

| 层 | 载体 | 归属判定 |
|---|---|---|
| 语义-客观 | KB：`cmm`（代码）/ `graphify`（文档） | "代码 / 文档本身说了什么" |
| 程序 | `skills/` | "如何做某类事"（SOP） |
| 情景 | git log + openspec `tasks.md` | "何时做了何事"（事件 / 决策时间线） |
| 语义-主观 | `memory/`（文件 → Stage 1 Mem0） | "用户是谁 / 工作方式 / 决策" |

**判定测试**（金句）：忘了这条，agent 会不会做出用户必须纠正的事？
- **会** → Memory（语义-主观层）
- 不会、但要被问起 → KB（cmm / graphify）
- 讲"怎么做" → Skill
- 讲"何时发生" → git / tasks

### 分类纪律
memory 文件 frontmatter `metadata.type` 限定四选一：`user` / `feedback` / `project` / `reference`。无匹配类型 → 拒绝入库（大概率它本就不属于主观层，按判定测试重路由）。

### 容量上限
`MEMORY.md` 索引每会话**全量注入**上下文，**上限 ~20 条**。超限处置：合并同主题条目、把低相关 / 过时条目降级为按需召回（Stage 1 Mem0 到位后，全量注入自动切为相关性召回，该上限随之失效）。

### 决策锚
`type: project` 的**决策型**记忆 MUST 附情景锚——正文引用对应的 git commit 或 openspec `tasks.md` 条目，使"我们何时、为何定了这件事"可回溯。事件本身仍留在 git/tasks（情景层），Memory 只存"决策结论 + 为何 + 锚点"。

### 范围边界（不越界）
Memory 只管主观层。**不存代码符号 / 调用链**（归 cmm）、**不存文档正文**（归 graphify）。跨层协作走"锚定"：文档图锚定概念 → 抽真实标识符 → 交 cmm 定位。

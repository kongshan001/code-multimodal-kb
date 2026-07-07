## Why

评测是当前**唯一"task 丰满 / spec 贫瘠"的缺口**：`add-code-multimodal-kb` §5（12 task）+ `add-agent-memory` §4（3 task）都有评测待办，却无 capability spec 立约；KB 的 design.md（95–137 行）把评测想得很透但埋在设计文档里，Memory 的评测设计几乎空白。评测是**横切能力**——一个 harness、一套 ground-truth 哲学、一套可复现约束——同时测三个 subject：`code-knowledge-base` / `multimodal-knowledge-base` / `agent-memory`。且**代码侧评测零 LLM 凭据**，是当前能立刻产出 recall@k 硬指标、反向验证整条 KB / 记忆路线是否值得的下一步。

## What Changes

- 新增横切 capability `evaluation`：系统 SHALL 可评测、SHALL 达 recall / 质量阈值、SHALL 可复现
- **一个评测 harness 测三个 subject**（不每变更各搞一套）
- 把 `add-code-multimodal-kb` design 95–137 的评测设计**提升为 capability 主干**，并补 Memory 评测维度（recall@k / 去重 / 边界路由准确率）
- **代码侧评测零凭据立即可跑**（结构指标 + PR 反挖 gold，不调 LLM）；文档侧 / 记忆侧凭据门控（与 doc-side KB / Memory Stage 1 共享同一把 LLM key）
- 接管 `add-code-multimodal-kb` §5 + `add-agent-memory` §4 的评测 task（在两变更 tasks.md 标注归属本变更）

## Capabilities

### New Capabilities
- `evaluation`: 跨 code / doc / memory 三 subject 的**检索 / 召回 / 路由 / 抽取质量**评测——harness、ground-truth 反挖、阈值门禁、可复现约束；只评检索质量层，不评 agent 端到端回答（归各 subject 变更的联调）

### Modified Capabilities
（无——本变更新增评测能力作为三个 subject 的**测量层**，不改它们的现有需求）

## Impact

- **新增依赖（数据集 / 库）**：RepoBench-R（ICLR24）、SWE-Lancer-Loc（216 条）、CoIR 子集、DeepEval（pip）、GraphRAG-Bench / WildGraphBench 子集；自建图指标 + MS GraphRAG LLM grader（几十行复刻）
- **凭据**：代码侧零 LLM（结构指标 + PR gold）；文档侧 / 记忆侧需 LLM judge / gold，**与现有两变更共享同一道凭据墙**
- **跨变更**：`add-code-multimodal-kb` §5（5.1–5.12）+ `add-agent-memory` §4（4.1–4.3）评测 task 归属本变更
- **无新增对外服务**（评测是本地 pytest 套件 + 报告）

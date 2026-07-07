## Context

三个 capability（`code-knowledge-base` / `multimodal-knowledge-base` / `agent-memory`）都需要"测好不好"，但评测此前散落：KB 有 12 个评测 task + 一段埋在 `add-code-multimodal-kb/design.md`（95–137 行）的详尽评测设计，Memory 只有 3 个 task stub、design 几乎空白，且两者都**无 capability spec**。本变更把评测立为**横切 capability**，统一 harness / ground-truth 哲学 / 可复现约束，测三个 subject。

凭据现实：代码侧评测**零 LLM**（结构指标 + PR 反挖 gold，可立即跑）；文档侧 / 记忆侧评测依赖 LLM（judge / gold），与 doc-side graphify / Memory Stage 1 共享同一道凭据墙。

## Goals / Non-Goals

**Goals:**
- 评测成为一等公民：有 spec 立约 + 统一 design + 一个 harness 测三 subject
- **代码侧评测零凭据即可产出 recall@k / 命中率硬指标**，反向验证 KB 路线是否值得
- 阈值门禁驱动改进（评测不为评分，为触发行动）
- 可复现：锁版本 + 锁模型 + 锁 temp，跨设备 / 跨时间分数可比

**Non-Goals:**
- 不评 agent 端到端回答质量（那是各 subject 变更的 Stage 2 联调，归原变更）
- 不自建标注平台 / 评测 SaaS（本地 pytest 套件 + 报告即可）
- 不做实时监控 / 在线 A/B（一次性基线评测，非持续）

## Decisions

### E1 — 评测是横切 capability，一个 harness 测三 subject
不为 code / doc / memory 各搞一套评测。一个 pytest harness 封装"调 subject 工具（cmm / graphify / Mem0）→ 收集 (query, 检索/图结果, gold) → 算指标"，三 subject 共享 harness、ground-truth 哲学、可复现约束，仅指标与 gold 来源不同。

### E2 — 代码侧优先（零凭据），文档侧 / 记忆侧凭据门控
代码侧评测（RepoBench-R + SWE-Lancer-Loc + 图指标 + PR gold）**不调 LLM**，立即可跑、立即出信号。文档侧（DeepEval / GraphRAG grader）与记忆侧（recall@k / 路由准确率）需 LLM judge / gold，与 doc-side KB / Memory Stage 1 共享凭据解锁。**实施顺序 = 代码侧先行**。

### E3 — Ground-truth 反挖 > LLM-as-judge
避"LLM 评 LLM"循环 + 作者自标偏见：
- **代码侧**：从真实 merged PR 反挖——NL issue 当 query，git diff 解析被改函数当 gold symbols，静态调用图当 gold 调用链；叠加 LSP goto-def 执行式反查。**零 LLM judge**。
- **文档侧**：借 MuSiQue / GraphRAG-Bench 的 gold path；gold 生成模型 ≠ 抽取模型；多裁判集成（Claude + GPT + Gemini 取均值）。
- **记忆侧**：构造人工标注集（用户偏 / 决策 / 事件 / 客观各若干）+ 路由 gold。

### E4 — 阈值门禁驱动行动
评测分数不进 dashboard 欣赏，每个指标绑阈值 + 触发动作（见下表）。不达标即触发具体改进，否则评测劳而无功。

### E5 — 范围：只评检索质量层
评"检索 / 召回 / 路由 / 抽取质量"。**不评 agent 最终回答的端到端质量**（归各 subject 变更的联调 task，如 KB 4.2 / Memory 2.5）。

## 三 subject 评测设计

### 代码侧（图 / 结构 / agent 检索）— 主轨道，零凭据

| 角色 | 选型 | 用途 |
|---|---|---|
| 主轨道 | **RepoBench-R**（ICLR24）+ **SWE-Lancer-Loc**（216 NL→文件/函数） | repo 级 ranking（recall@k / nDCG@10）+ agent 符号定位命中率 |
| 图检索专用（自建） | Symbol-Level Hit@k / Call-Chain Edge Recall / Path Precision@k | 测 cmm 真正关心的"定位符号 + 调用链"（gold 来自静态调用图） |
| 向量基线对照 | CoIR 子集（cosqa + codesearchnet + stackoverflow） | 降级 ~10–15%，仅防 nomic-embed-code 退化，不与榜单比 |
| 方法论锚 | RepoHyper（tree-sitter + 调用图 + GNN，架构最像） | 读它省试错 |

### 文档侧（GraphRAG / 跨文档）— 🔴 卡凭据

| 角色 | 选型 | 用途 |
|---|---|---|
| 答案质量 | **DeepEval**（缩小范围） | faithfulness / answer relevancy / G-Eval 评 graphify 文本节点 → 答案 |
| GraphRAG 答案 | **MS GraphRAG LLM grader**（复刻） | comprehensiveness / diversity / empowerment head-to-head vs 朴素 RAG |
| 抽取质量 | 独立模型抽样打 entity / relation / claim | 补"图构建质量"盲区 |
| 外部 held-out | GraphRAG-Bench / WildGraphBench 子集 | 避作者自标偏见 |

### 记忆侧（召回 / 去重 / 路由）— 🔴 卡凭据（依赖 Memory Stage 1）

| 角色 | 指标 | 用途 |
|---|---|---|
| 召回质量 | recall@k + 实体去重正确率 + 注入体积收敛 | 主观记忆按主题召回的相关性、无冗余、上下文有界 |
| 边界路由准确率 | 候选事实 4 类（客观/程序/事件/主观）路由命中率 | 验证 D1 归属规则可操作 |

## 阈值门禁（E4）

| 指标 | 阈值 | 触发动作 |
|---|---|---|
| 代码侧 Symbol Hit@k / 命中率 | < 设定基线 | 调 cmm 检索策略 / 补结构兜底 |
| 文档侧 recall@5 | < 0.6 | 评估补文档向量索引 |
| cross-tool anchoring 成功率 | < 70% | 重设计 bridging（走 `source_location` 而非裸字符串） |
| 抽取质量 entity/relation 准确率 | < 0.7 | 调 graphify 抽取 prompt / 换模型 |
| 记忆 recall@k | < 设定基线 | 调召回策略 |
| 记忆边界路由准确率 | < 设定基线 | 补 D1 规则 / 重审归属判定 |
| 查询 P95 延迟 | > 2s | 加查询缓存 |

## 可复现前提（must-fix）

graphify 语义抽取 / Mem0 抽取非确定（LLM 生成），评测基线可复现**必须先锁**：`temp=0 + 固定 LLM 模型 + 工具版本（graphify / cmm / Mem0）`，并在评测报告记录这三项——否则跨设备 / 跨时间分数无意义。（代码侧结构指标天然确定，不受此约束。）

## Risks / Trade-offs

- **数据集获取（CN 网络）** → RepoBench / SWE-Lancer / CoIR 从 GitHub 拉，走代理（`127.0.0.1:7897`）或 ghproxy
- **PR 反挖 gold 的质量** → 只取有清晰 NL issue + 干净 diff 的 merged PR；LSP goto-def 执行式验证兜底
- **LLM judge 成本**（文档侧 / 记忆侧）→ 子集抽样 + 多裁判取均值控成本；与生产抽取共凭据不额外开销
- **评测与生产代码耦合** → harness 只调 subject 的 MCP / CLI 接口，不改其内部，subject 升级不影响评测契约

## 跨变更关系

- 本变更 own `evaluation` capability（spec / design / tasks）
- `add-code-multimodal-kb` §5（5.1–5.12）+ `add-agent-memory` §4（4.1–4.3）评测 task → 归属本变更（在两变更 tasks.md 加一行指向）
- 凭据时序：代码侧零凭据立即可跑；文档侧 / 记忆侧与 doc-side KB / Memory Stage 1 共享同一把 LLM key

## Open Questions

- 代码侧"设定基线"的具体数值（RepoBench-R / SWE-Lancer 首跑后定，先跑出基线再设阈值）
- 记忆侧标注集规模与来源（Stage 1 Mem0 到位后定，先复用 Memory Stage 0 的 4 案 + 扩展）

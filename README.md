# engineer_demo — 知识库 + agent 记忆（规格仓库）

本仓库**无源码**，只承载 OpenSpec 变更与部署文档：给 agent（Claude Code 等）接入 **知识库**（代码 + 多模态文档）与 **记忆**（跨会话主观记忆）能力。沿用在 `add-code-multimodal-kb` 确立的原则：**复用成熟 MCP + 注册到 agent，不建网关、不引平台外壳、几乎零自建代码**。

## 目标靶子（B 模式 · 真实落地）

KB / 记忆 / 评测不再停在 infra——**指向真实靶子才算被证明**：
- **代码库**：[Godot](https://github.com/godotengine/godot) `4.7-stable`（~1M+ LOC C++，百万行级真实引擎 → cmm 的考场）
- **文档语料**：Godot 官方文档（docs.godotengine.org，待 LLM 凭据由 graphify 建图）
- **成功场景**：agent 能在 Godot 代码 + 文档上准确回答「X 在哪实现 / 谁调用 / 文档怎么说」，评测给出真实 recall@k

策略：**分片优先**——先 index `core/` 证 cmm 吃得下真实 Godot C++ → 建 Godot gold → 真 recall@k → scale up，不盲全量。

## 进行中的变更

| 变更 | 进度 | 主题 | 状态 |
|---|---|---|---|
| [`add-code-multimodal-kb`](openspec/changes/add-code-multimodal-kb/) | 7/33 | 代码 KB（cmm ✅）+ 多模态文档 KB（graphify 🟡 卡凭据） | 代码侧已交付，文档侧等凭据 |
| [`add-agent-memory`](openspec/changes/add-agent-memory/) | 4/17 | agent 记忆层（Stage 0 ✅ / Mem0 Stage 1 🔴 卡凭据） | Stage 0 已落地，Stage 1 等凭据 |

## 文档索引

| 文档 | 用途 | 状态 |
|---|---|---|
| `CLAUDE.md` | 项目 agent 纪律：记忆四层归属 + 判定测试 + 分类/容量/决策锚规则 | ✅ 新建（agent-memory Stage 0） |
| [`docs/deployment-runbook.md`](docs/deployment-runbook.md) | KB 部署实测步骤（cmm 全链 + graphify 待凭据）+ FAQ | ✅ A 侧实测 / 🟡 B 侧待凭据 |
| `openspec/changes/<change>/proposal.md` | 变更的 why / what / capabilities / impact | — |
| `…/design.md` | 决策 + 取舍 + 迁移计划 + open questions | — |
| `…/specs/<capability>/spec.md` | 需求 + 场景（SHALL/MUST，每条带 WHEN/THEN） | — |
| `…/tasks.md` | 实施任务清单（完成的带验证证据） | — |

## 待办（跨变更合并 · 按是否卡凭据分组）

### 🟢 现在可做（零凭据）
- **KB §5 评测 harness**（`add-code-multimodal-kb` 5.1–5.5，代码侧）—— pytest 骨架 + 调 cmm 收集 (query, 结果, gold)，跑 RepoBench-R / SWE-Lancer-Loc，产 recall@k / 命中率 → **反过来证明整个 KB 路线是否值得**（推荐下一步）
- KB 1.4 决策 graphify 图存储形态（`graph.json` vs Neo4j）—— 纯决策
- KB 4.3 两个 MCP server 的工具命名 / 优先级冲突 —— 纯分析

### 🔴 卡 LLM 凭据（一把 key 同时解锁两条线）
> 提供一把 LLM key 后，以下**并行**解锁：
- **KB 文档侧**（1.3 / 3.1–3.4）：graphify 建文档图 + 跨文档检索 + 文档评测
- **agent 记忆 Stage 1**（`add-agent-memory` 2.1–2.5）：Mem0/OpenMemory MCP 自托管 → 替换薄文件记忆为向量 + 图召回
- 两条线各自的评测（KB 5.6–5.9 文档侧 / memory 4.x）与部署 runbook 补全（KB 6.3 / memory 5.x）

### ⚪ 可选（痛点触发才做）
- agent 记忆 Stage 2（`add-agent-memory` 3.1–3.3）：Zep/Graphiti 时序召回
- KB 6.1–6.5 其他设备部署验证

## 关键约束

- **LLM 凭据是当前主瓶颈**：graphify 建图 + Mem0 抽取 + 评测 LLM judge 都需要；本机暂无 key
- 两个变更**共享同一道凭据墙**——给一次 key，文档侧 KB 与 agent 记忆 Stage 1 一起前进
- 记忆 vs KB 边界（金句）：*忘了这条 agent 会不会被纠正？会→Memory；不会但要查→KB；怎么做→Skill；何时→git*（详见 `CLAUDE.md`）
- 改动一律提交 main + push（带 Co-Authored-By）

# engineer-demo-memory · 本仓库自己的记忆层（demo target）

> ⚠️ **自指 demo**——测的是 engineer_demo 这个仓库**自己的** MemPalace 记忆。
> **不是"对接到别的项目"用的**：别人 fork 后建议**删掉/换成自己的记忆**。

## 这是什么

- **目标**：engineer_demo 的 MemPalace 记忆库（`palace=engineer_demo`）——存的是这个仓库跨会话的偏好 / 决策 / 事件。
- **gold 锚的是本仓库的 memory 文件名**（`agent-memory-approach.md` 等）+ 会话 jsonl，换项目就失效（这是设计上的"不可移植"，不是 bug）。

## 测什么

两部分：

1. **召回**（15 题）：给一句自然问题（`记忆层选型 MemPalace 还是 Mem0`），mempalace search 能不能召回含答案的 source 文件。**零 LLM**（本地 embedding，可复现）。
2. **路由**（13 题）：给一条候选事实，D1 四层归属规则能不能判对该存哪层（客观→KB / 程序→skills / 事件→git / 主观→memory）。

## 最新结果（2026-07-13）

### 召回（mempalace · 零 LLM）

| 指标 | 值 | 大白话 |
|---|---|---|
| `hit@5` | **0.933** | 前 5 条里有正确 source 的占 93.3% |
| `recall@5` | 0.867 | 标准 source 全召回到前 5 的占 86.7% |
| 去重正确率 `unique_source_ratio@5` | 0.64 | top-5 里不同 source 占 64%（有同源冗余） |

### 路由（D1 四层归属）

| 指标 | 值 | 大白话 |
|---|---|---|
| 总体准确率 | **1.0** | 13 条全判对 |
| 四类各自 | 各 1.0 | objective / procedural / episodic / subjective 全对 |

### 答案质量（Ragas 协议 · LLM 判）

| 指标 | 值 | 大白话 |
|---|---|---|
| `faithfulness` | **0.93** | 答案 93% 有依据（不瞎编） |
| `context_precision` | 0.48 | 召回的 context 只有一半相关（会话碎片嘈杂） |

**一句话结论**：召回准（hit@5=0.93）、路由全对（1.0）；答案忠实（0.93）但 context 嘈杂（0.48）——记忆 drawer 多是会话碎片，这是已知特征，不是 bug。

## 数字怎么看

- **`hit@5`**：前 5 条召回结果里，碰到任一正确 source 就算赢。
- **`routing_overall_accuracy`**：13 条候选事实判对几条。1.0 = 全对。
- **`faithfulness`**：答案是否都从给定的 context 里来（防瞎编）。高=忠实。
- **`context_precision`**：召回的 context 里有多少是真正相关的。低=召回嘈杂（记忆碎片天然如此）。

## 怎么自己跑

```bash
bench run memory         --target engineer-demo-memory   # 召回 + 路由（零 LLM）
bench run memory-quality --target engineer-demo-memory   # 答案质量（需 LLM 凭据）
```

## 诚实边界

- **不可移植**：gold 锚本仓库 memory 文件名。fork 后删这个 target，换成你自己的（建 `targets/<你的记忆>/` + 改 `memory.palace`）。
- 路由 1.0 部分源于"标注集和 D1 规则同源"——真实泛化需更大标注集。
- faithfulness / context_precision 由 GLM 判（生成与判分同家族，self-preference 风险），相对参考值。
- 2 道召回题标了 `tags: ["known_weak_probe"]`（诚实探针：答案原文未被 mine 进记忆库，**预期**召回弱——这是故意的探针，不是缺陷）。

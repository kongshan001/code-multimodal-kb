# godot-docs · Godot 文档语义检索

> 拿 **Godot 文档子集**（17 篇 .rst）建成"概念图"，测能不能用大白话问出对的文档节点。
> 文档检索 ≠ 代码检索——要听懂"概念"（signals、node lifecycle），不是字面匹配。

## 这是什么

- **目标文档**：Godot 文档子集（17 篇 reStructuredText → 72 个概念节点），用 graphify 建成文档知识图。
- **文档图路径**：`~/Documents/godot-docs-subset/graphify-out/graph.json`（你机器不同 → 改 `target.local.json`）。

## 测什么

给一句文档式提问（`how do nodes communicate with signals`、`node lifecycle ready callback`），看 graphify 能不能从文档图里找出对的节点（`Signals Concept`、`_ready Callback`、`Node Class`）。

- 10 道题，全是 NL 概念查询。
- graphify 用 BFS 遍历文档图：**建图花 LLM**（一次性，按量计费），**查询不调 LLM**（可复现）。

## 最新结果（2026-07-13 · 10 题）

| 指标 | 值 | 大白话 |
|---|---|---|
| `recall@5` | **0.7** | 前 5 个节点里有正确答案的占 70% |
| `recall@100` | 0.933 | 全图范围召回 93.3% |

**一句话结论**：答案基本都在图里（93.3%），graphify 把其中 70% 排进了前 5。剩下的提升空间在**重排（re-rank）**——把已经在图里的对答案往上挪。

## 数字怎么看

- **`recall@5`**：前 5 个返回节点里有没有标准答案。文档侧主指标。
- **`recall@100`** ≈ 全图召回：这个高（0.933）说明"答案在图里，只是排序没排上来"——是排序问题不是抽取问题。如果这个低，才说明建图漏了内容。

## 怎么自己跑

```bash
bench run doc --target godot-docs
```

前置：先 `graphify build <文档目录>` 建图（花 LLM，按量计费；`graph.json` 可提交 repo 团队共享）。建好后查询零 LLM。

## 诚实边界

- 文档子集只覆盖 vector/math 等主题——超出覆盖的主题 graphify 返空属正常。
- 答案质量（faithfulness 0.99）由单独的 `doc-ragas` runner 测，归 `run_doc_quality_ragas`（其 RST_DIR 路径配置化是后续变更 F1）。

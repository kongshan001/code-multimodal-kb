# 文档答案质量报告 · 2026-07-12（Ragas 协议：faithfulness + context_precision）

> 填 `value-benchmark §7` 标注的"答案质量 ○○○○（未量化）"缺口。Ragas 协议**直接实现**
> （ragas 0.4.3 与 langchain_community 0.4 import 链冲突，不值得解依赖；两指标是公开 LLM 判分协议，
> 复刻更稳，与项目既有"复刻版"模式一致）。
> 数字来自归档 `reports/archive/20260711T182027Z-doc-quality-ragas-protocol-docs-ragas.json`。

## 0. 设置

| 项 | 值 |
|---|---|
| 题集 | gold_docs 10 条 NL 概念题（Godot 17 篇 .rst 文档子集）|
| context 源 | graphify 定位节点 → 取节点 `src` 指向的 **.rst 真实文本**（前 5000 字符，top-3 文档）|
| 答案生成 | GLM（cc-connect glm-5.1）用 context 作答（强制作答，不轻易 refusal）|
| 判分 | GLM 当 judge（同家族——见边界）|
| 指标 | faithfulness + context_precision（reference-free，Ragas 协议）|

## 1. 核心结果

```
mean_faithfulness        0.971   答案高度忠实 context（低幻觉：claims 几乎都被 context 支撑）
mean_context_precision   0.533   检索切题率（graphify 返的文档约半数直接切题）
```

逐题：8/10 faithfulness=1.0（完全忠实），2/10 = 0.83/0.88（个别 claim 越出 context）。
context_precision 分布广：4/10 = 1.0（单文档命中即切题），3/10 = 0.33（3 文档只 1 切题），1/10 = 0（未切题）。

## 2. 解读

- **faithfulness 0.971（高）**：GLM 拿到 .rst 文本后**基本不幻觉**——答案的 claims 都能在 context 里找到支撑。说明 RAG 答案的**忠实度瓶颈不在生成**，而在**检索是否拿到对的文档**。
- **context_precision 0.533（中）**：检索（graphify）返回的约半数文档直接切题，另半是相邻主题。这与 doc-baseline 的 `recall@5=0.70` 量级一致——检索质量是当前主要改进点。
- **faithfulness 高 + context_precision 中**的组合：系统**不会瞎编**（给错文档时倾向保守/拒答而非幻觉），但**给对文档的概率待提升**。

## 3. 诚实边界（引用须注明）

1. **LLM-judged（核心边界）**：GLM 生成答案 + GLM 当 judge = **同家族 self-preference**（spec 反 LLM-judge 循环原则）。分数当**相对参考值**（改 prompt/换检索前后对比），**非绝对回归值**。要做绝对质量需第二家族 judge（待 Claude/OpenAI key）。
2. **Ragas 协议直接实现，非 ragas 库**：ragas 库 import 链断（langchain_community 0.4 移除 chat_models.vertexai）；faithfulness/context_precision 是公开协议，复刻等价，但未经 ragas 库的回归验证。
3. **.rst 前 5000 字符做 context**：未做段落级定位（dot product 等可能在文档中段），靠大 cap 覆盖；context_precision 受此影响。
4. **小 N=10**：gold_docs 子集规模，扩到 held-out（GraphRAG-Bench/WildGraphBench）是 scale-up（§3.5）。
5. **reference-free**：未用 context_recall/answer_correctness（需 reference answer）；只测了不需要标准答案的两指标。

## 4. 价值定位（接 value-benchmark §7）

| 维度 | 之前 | **现在** | 证据 |
|---|---|---|---|
| 文档答案质量 | ○○○○（未量化）| **●●○○**（faithfulness 实测）| mean_faithfulness=0.971 / context_precision=0.533（LLM-judged）|

**总判断**：答案质量层从"未量化"进入"部分量化"——**忠实度高（0.971，不幻觉）、检索切题率中（0.533，待提）**。
改进方向明确：**提检索精度**（context_precision），而非压幻觉（faithfulness 已满）。忠实度天花板 + self-preference 边界待第二家族 judge 解锁。

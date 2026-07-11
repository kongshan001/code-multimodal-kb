# 记忆答案质量报告 · 2026-07-12（Ragas 协议：faithfulness + context_precision）

> 填 memory-baseline §6 的"记忆答案质量 ○○○○（需 LLM judge）"最后一格。
> 与 doc-quality-ragas 同构（Ragas 协议直接实现），context 从 .rst 换成 mempalace 召回的 drawer。
> 数字来自归档 `reports/archive/20260711T210800Z-memory-quality-ragas-protocol-memory-ragas.json`。

## 0. 设置

| 项 | 值 |
|---|---|
| 题集 | RECALL_GOLD 15 条（记忆召回用的 NL query）|
| context 源 | mempalace_search top-5 **drawers**（会话碎片为主，非结构化）|
| 答案生成 + 判分 | GLM（cc-connect glm-5.1），Ragas 协议 faithfulness + context_precision |

## 1. 核心结果

```
mean_faithfulness        0.951   答案高度忠实 drawer context（低幻觉，逼近文档层 0.971）
mean_context_precision   0.360   检索切题率（会话碎片不如 .rst 切题，低于文档 0.533）
```

逐题：12/15 faithfulness=1.0（完全忠实），3 条 <1：`Intel Mac onnxruntime`（0.62，技术细节越出 context）、
`记忆层选型`（0.80）、`MEMORY.md 索引`（0.83）。context_precision 分布广：6 条=0（drawer 无一切题）、
多条 0.4–0.8。

## 2. 解读（与文档层对比，意外发现）

| 层 | faithfulness | context_precision | context 性质 |
|---|---|---|---|
| 文档（.rst）| 0.971 | 0.533 | 结构化教程文本 |
| **记忆（drawer）** | **0.951** | **0.360** | 会话碎片（嘈杂/冗长）|

**反直觉**：原以为记忆 drawer 嘈杂 → faithfulness 会低。实测 **faithfulness 仍 0.951（逼近文档层）**——
**GLM 即使在嘈杂会话碎片上也不怎么幻觉**，它倾向"基于给定的 context 保守作答"（faithful 但可能答不到点）。
真正低的是 **context_precision 0.360**（< 文档 0.533）——会话碎片检索不如结构化 .rst 切题。

**结论**：记忆层的瓶颈和文档层一样在**检索精度**（context_precision），不在**生成幻觉**（faithfulness 已满）。
记忆 drawer 多样嘈杂 → 召回的 top-k 里"切题"比例低。改进方向：drawer 抽稀/压缩（mempalace compress）
或召回重排序，而非压幻觉。

## 3. 诚实边界

1. **LLM-judged（核心边界）**：GLM 生成 + GLM 判 = 同家族 self-preference。**相对参考值非绝对回归值**。
   与文档层同；绝对质量需第二家族 judge。
2. **Ragas 协议直接实现**（非 ragas 库，同 doc-ragas）。
3. **drawer 嘈杂**：palace 99.6% 是会话碎片（见 memory-baseline §2.3），context_precision 受此影响；
   换更干净 palace（如 compress 后）分数会变。
4. **小 N=15**：RECALL_GOLD 规模；扩标是 scale-up。
5. **faithfulness 高的隐含风险**：GLM 可能"忠实于一个答不到点的 context"（faithful 但 unhelpful）——
   faithfulness 不等于有用性。需结合召回质量一起看。

## 4. 价值定位（填 memory-baseline §6 最后一格）

| 维度 | 之前 | **现在** |
|---|---|---|
| 记忆答案质量 | ○○○○（未量化）| **●●○○**（faithfulness 0.951 / context_precision 0.360，LLM-judged）|

**总判断**：记忆答案质量层从"未量化"进入"部分量化"——**忠实度高（0.951）、检索切题率低（0.360）**。
与文档层同构结论：瓶颈在召回精度，不在生成幻觉。至此 value-benchmark / memory-benchmark 的所有
"未量化"格均已至少 ●●○○（检索 + 召回 + 路由 + 答案质量两层都有实测分）。

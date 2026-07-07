# 代码侧首基线发现 · cmm.search_code × graphify

> 任务 2.2「在 cmm 上跑出基线分数」产物。报告由 `python -m eval.run_code_baseline` 生成。
> 原始 JSON：`eval/reports/code-baseline-graphify.json`。

## 数字（n=21 query）

| 指标 | 值 |
|---|---|
| recall@1 / hit@1 | **0.476** |
| recall@3 / hit@3 | 0.667 |
| recall@5 / hit@5 | **0.762** |
| recall@10 / hit@10 | 0.81 |

lockfile：`cmm 0.8.1 · graphify 0.8.46 · temp=0 · 零 LLM judge`（gold 来自 cmm get_architecture 实测符号，非 LLM 生成）。

## 关键发现（评测的价值所在）

### 1. 概念查询（无词汇重叠）全军覆没 → 语义缺口属实
- `id construction` → gold `_make_id`：**top5 空**（cmm 返回 0 结果）
- `security` → gold `check_graph_file_size_cap`：top5 是 `detect_backend / to_json / _rebuild_code …`，全错
- 根因：`search_code` 是 grep + 图排序，纯概念词在目标符号代码里不出现 → 命中不了。design 决策 4 早预警；cmm 的 `semantic_query`（nomic-embed-code）**不在 MCP 工具集**里，MCP 侧无语义检索兜底。
- **触发（E4 精神）**：概念子集 recall@5=0，应评估补语义检索路径（CLI 调 `semantic_query`，或 agent 翻译 NL→关键词）。

### 2. 文档节点污染 → M6 风险的实证实例
- `transcribe audio` → gold `transcribe`：top5 = `[ingest, "graphify reference: transcribe video and audio" ×4]`。**4 个 markdown 文档节点排在真函数前**。
- 即 design M6（文档内嵌内容污染图）的真实表现：doc 节点与 code 函数混排、抢占靠前位。
- **触发**：给 doc 节点标 `provenance` 并在 code 检索时降权/过滤。

### 3. 符号变体混淆
- `load graph` → gold `load_graph`：top5 = `[write_callflow_html, _load_graph, _rebuild_code, _build_server, _load_global_graph]`，gold 在 rank 6–10（recall@10=1）。私有变体 `_load_graph` 抢先。

### 4. 词汇/精确匹配强
- 16/21 在 rank1 命中；含目标词的查询 recall@5 普遍 = 1.0。

## 方法学边界（诚实）

- **小-N 首基线**：21 条，非 RepoBench/SWE-Lancer 全量规模（HF RepoBench 需 token 401、且 completion/issue→file 范式与 cmm 符号检索不直接对口）。
- **gold 来源**：cmm `get_architecture` 实测符号（architecture-derived），**非 task 2.4 的 PR 反挖**。PR 反挖（真实 merged PR diff → gold）仍是更硬的 scale-up，待接目标仓库 git 历史。
- **单仓库**：仅 graphify；多仓库/跨语言留待 scale-up。
- **单检索接口**：仅 `search_code`；`search_graph`（BM25）/ `semantic_query` 对照留待后续。

## 触发的下一步

1. 概念查询 0% → 评估 cmm `semantic_query`（CLI）接入，或 agent NL→关键词翻译层
2. doc 节点污染 → provenance 标记 + code 检索降权
3. scale gold：PR 反挖（task 2.4）+ 多仓库
4. 对照基线：CoIR 向量（task 2.5）+ search_graph BM25

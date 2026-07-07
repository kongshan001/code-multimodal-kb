# 三路检索对比 · Godot core/（grep vs semantic vs BM25）

> 回应 add-evaluation-baseline「接 semantic_query 救概念盲区」。在 Godot core/（moderate 索引，
> 7890 函数向量 + LSH）上，对 5 条 grep 全盲的概念 query 跑三路检索。

## 结论先行

**BM25 是 NL 概念查询的最优主路；semantic_query 只在关键词=代码 token 时有效；grep 全盲。**
**design 决策4「semantic_query 主路」被实证修正为「BM25 主路 + semantic token-相似兜底 + grep 精确」。**

三路共同硬限：**代码里完全不出现的概念词**（如 `pathfinding`，AStar 代码用的是 `path`/`get_point_path`）→ 三路全败，必须靠 **agent NL→关键词翻译**（decision 4 的 agent 翻译层仍是必需）。

## 5 条概念盲区对比（gold 取自真实 Godot 符号）

| 概念 query | gold | grep `search_code` | semantic_query | **BM25 `search_graph query`** |
|---|---|---|---|---|
| string format | vformat | ❌ `_stringify` | ❌ path_to_file 等(0.94 但非 vformat) | ✅ **`String.format` r1**（比 vformat 更准——公开 API）|
| a star pathfinding | AStar | ❌ 空 | ❌ `["pathfinding"]` 分数~0.1 近无匹配；`["astar"]`→AStarGrid2D 家族(0.78) △ | ❌ `total:0`（"pathfinding" 不在代码里）|
| delete/free memory | memdelete | ❌ 空 | △ free/_allocate_rid(0.93) | ✅ **`Memory.free_static`/`DefaultAllocator.free`** |
| operating system | OS | ❌ 空 | ✅ `["os"]`→**OS 0.999** r1 | ✅ `OS.get_system_*`（OS 类方法群）|
| int to string | itos | ❌ compare_value 等 | △ `_to_int`/`as_int`(0.96，概念对) | △ `to_int`(反向 string→int，同文件 ustring.cpp) |

命中计：grep **0/5** ＜ semantic **~1-2/5**（仅当关键词=代码 token）＜ **BM25 ~3-4/5**。

## 关键洞察

1. **BM25 对 NL 多词查询干净有效**：分词后按代码 token 匹配，"string format"→`String.format`、"free memory"→`Memory.free_static`，且结果无 semantic 那种 `$id/$schema` 默认噪声前缀。
2. **semantic_query = 代码 token 相似，不是英文概念相似**：nomic-embed-code 嵌的是代码 token。`["os"]`→OS(0.999)、`["astar"]`→AStarGrid2D(0.78) 完美；但 `["operating","system"]`→floorf(0.04)、`["pathfinding"]`→0.1 全废。**它不会把英文概念桥接到不含该词的代码**。
3. **grep 是纯字面**：query 词不在 gold 符号代码里就 0 命中；大 C++ 上还把类埋在方法下（strict 失效，见 godot-findings）。
4. **pathfinding 是三路共同死穴**：AStar 代码不含 "pathfinding"，任何检索都救不了 → 必须靠 agent 把 "pathfinding" 翻译成 "astar"/"path" 再查。

## 修正后的检索架构（喂回 design 决策4）

```
NL 概念查询
   │
   ▼
agent 翻译层（NL→关键词，处理 pathfinding→astar 这类零词重合）   ← 不可省
   │
   ├─ 多词 NL ──────► BM25 search_graph query=    （主路，~3-4/5）
   ├─ 已知 token 相似 ► semantic_query=["token"]  （兜底，token 匹配时强）
   └─ 精确字面 ─────► grep search_code            （补精确/路径过滤）
```

## 方法学边界
- 概念 query 仅 5 条（盲区子集），非全量；BM25 命中按"概念正确符号"判（非严格 gold 名）——如 String.format vs vformat 算命中。
- 单仓库 core/ moderate 索引；semantic 用 LSH 近似（bands=16）。
- 未测：混合 query+semantic_query 同调、limit 调参、其他 cmm 检索接口。

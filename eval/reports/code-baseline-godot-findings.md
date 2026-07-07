# Godot core/ 基线发现 · cmm.search_code × 真实百万行 C++

> 任务 2.2「在真实目标仓库上跑基线」产物。Godot 4.7-stable `core/`（417 .cpp/.h →
> cmm `fast` index：13504 节点 / 38470 边 / 1094 类）。`python -m eval.run_code_baseline --target godot`。

## 数字（n=26 query，gold 取自 cmm 实测真实 Godot 符号，零 LLM）

| 指标 | graphify（参照） | **Godot core/** |
|---|---|---|
| strict recall@5（gold = 类名，node 短名精确匹配）| 0.762 | **0.0** |
| broad recall@5（gold 出现在 node\|qualified_name\|file，归一化）| 0.857 | **0.692** |
| broad recall@10 | 0.857 | 0.731 |

lockfile：`cmm 0.8.1 · Godot 4.7-stable core/ · fast 模式 · temp=0 · 零 LLM judge`。

## 两条方法学发现（评测本身被真实仓库倒逼出来的）

1. **粒度错配**：cmm search_code 在大 C++ 仓库返回**图中心性高的方法/文件节点**，把类型/类定义埋在自己的方法下。
   - `"vector2"` → 返回 `max, min, hash_compare`（**都是 Vector2 的方法**），不返回 `Vector2` 类节点 → strict recall 恒 0。
   - `"image"` → `crop_from_point, _get_color_at_ofs`（Image 方法）；`"http client"` → `io/http_client.h`（文件）。
   - → 必须用 broad（文件/类区级）指标才公平；strict 在大 C++ 上结构性失效。
2. **snake_case vs CamelCase**：`message_queue`(文件) ≠ `MessageQueue`(类)，下划线阻断子串匹配。broad 指标已加归一化（去非字母数字）修正，否则 broad@5 会从 0.692 被低估到 0.423。

## 真盲点（broad recall@5 仍 0 的）

全是**纯概念查询**（query 词在目标符号代码里不出现），grep 检索结构性失效：
- `string format`→`vformat`、`int to string`→`itos`、`delete object free memory`→`memdelete`、`a star pathfinding`→`AStar`、`operating system abstraction`→`OS`
- 与 graphify 的概念缺口发现一致，但在 Godot 上更刺眼（仓库大、干扰多）。

## 结论：cmm 在 Godot 上**部分有效，语义层是必需而非可选**

- **能落对代码区 ~69%**（broad@5）——cmm 的 grep+图排序对**含目标词的查询**有用，能定位到正确文件/方法群。
- **不能精确定位类型**（strict@5=0）——agent 拿到的是"相关方法群"而非类定义，需要自己聚合/上溯到类。
- **概念查询全盲**——必须靠 design 决策 4 的 `semantic_query`（cmm 自带 nomic-embed-code，但**不在 MCP 接口**）或 agent NL→关键词翻译层。

## 触发的下一步（喂回 KB 改进）

1. **接 cmm `semantic_query`（CLI）** —— 概念查询盲区的最高杠杆解；若接上，预期把 5 条概念盲点救回大部分。
2. **文件/类区级召回作为主指标** —— Godot 级 C++ 上 strict 失效，broad（+归一化）才是公平刻度；记入评测方法学。
3. **scale up index** —— core/ → 加 scene/、servers/、modules/，验证 cmm 在更大体量/全量的内存与耗时。
4. **PR 反挖 gold（task 2.4）** —— 用真实 Godot merged PR 的 diff 当 gold，比类名 gold 更贴近真实"定位"任务。

## 方法学边界

- gold = 类名级、architecture-derived（非 PR 反挖）；broad 指标补偿了粒度差，但仍不如函数级 PR gold 硬。
- 单仓库 core/ 分片（非全量 Godot）；fast 模式（无 semantic/similarity 边）。
- 单检索接口 search_code；`search_graph`(BM25) / `semantic_query` 对照留待后续。

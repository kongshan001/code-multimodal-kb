# agent-compare 结果 · target=godot-core · model=glm-5.1
> 4 题 × 1 runs × 4 臂。

## 谁赢
- **准确率最高**：`no-kb`（accuracy=0.75）
- **最省 token**：`kb`（mean_total_tokens=891.2）
- **最省钱**：`kb`（mean_cost_$=0.0006）
- **KB vs 无 KB token 压缩**：3.44×（>1 = KB 省）

## 指标怎么看（小白版）
| 指标 | 大白话 |
|---|---|
| `accuracy` | 答对率 = 答对的题 ÷ 总题数。0~1，越高越好 |
| `mean_total_tokens` | 平均每题烧多少 token（≈字数）。越少越省 |
| `mean_llm_calls` | 平均每题调几次大模型。越少越快越省 |
| `mean_tool_steps` | 平均每题用几次工具（cmm/grep/read） |
| `mean_wall_clock_s` | 平均每题跑多久（秒） |
| `mean_cost_$` | 平均每题花多少钱（≈ token × 单价） |
| `tool_diversity` | 平均用了几种不同工具（高了可能在乱试） |
| `truncated_rate` | 多少题没在步数内答完（卡住了）。0 最好 |
| `context_compression` | 有 KB 比无 KB 省几倍 token（>1=KB 省；仅 no-kb+kb 都跑时给） |

## 对比矩阵
| 臂 | accuracy | mean_total_tokens | mean_llm_calls | mean_tool_steps | mean_wall_clock_s | mean_cost_$ | tool_diversity | truncated_rate | n_episodes |
|---|---|---|---|---|---|---|---|---|---|
| `no-kb` | 0.75 | 3062.5 | 4.25 | 5 | 23.71 | 0.0022 | 1.5 | 0.25 | 4 |
| `kb` | 0.5 | 891.2 | 2 | 1 | 9.85 | 0.0006 | 1 | 0.0 | 4 |
| `kb+superpowers` | 0.75 | 1944 | 2.75 | 2 | 15.14 | 0.0014 | 1.25 | 0.0 | 4 |
| `kb+openspec` | 0.75 | 1984.5 | 2.5 | 1.5 | 14.43 | 0.0014 | 1 | 0.0 | 4 |

## 逐题得分对照

> 每题各臂的答对 / 答案 / 指标（4 题 × 4 臂）。看哪题谁答对、谁省 token、谁卡住。

### q01 · code_retrieval
**题**：string format  ·  **gold**：vformat

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✗ | (max_steps reached without final answer) | 5440 | 6 | 9 | 33.97 | ⚠卡住 |
| `kb` | ✗ | `String::format` — 定义在 `core/string/ustring.cpp` | 934 | 2 | 1 | 9.19 |  |
| `kb+superpowers` | ✗ | `String::format` — 定义在 `core/string/ustring.cpp` | 1671 | 2 | 1 | 10.95 |  |
| `kb+openspec` | ✗ | `String::format` — 定义在 `core/string/ustring.cpp` | 1501 | 2 | 1 | 13.92 |  |

### q02 · code_retrieval
**题**：int to string  ·  **gold**：itos

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | Godot core 中 int → string 的主要函数：  - **`itos(int  | 1296 | 3 | 3 | 15.13 |  |
| `kb` | ✓ | `itos()` — 定义在 `string/ustring.cpp`，将 `int` 转为 ` | 926 | 2 | 1 | 11.5 |  |
| `kb+superpowers` | ✓ | `itos`（定义于 `core/string/ustring.cpp`）——将 `int` 转 | 2655 | 3 | 2 | 11.56 |  |
| `kb+openspec` | ✓ | **`itos(int64_t p_val)`** — 定义于 `string/ustring. | 2475 | 3 | 2 | 12.39 |  |

### q03 · code_retrieval
**题**：delete object free memory  ·  **gold**：memdelete

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | In Godot core, deleting objects and freeing memo | 4554 | 6 | 7 | 37.15 |  |
| `kb` | ✗ | 相关符号：  - **`Memory::free_static`** — 释放静态分配的内存 ( | 976 | 2 | 1 | 8.63 |  |
| `kb+superpowers` | ✓ | 在 Godot core 中，删除对象/释放内存涉及以下关键符号：  ## 内存分配/释放宏与函 | 2370 | 4 | 4 | 26.6 |  |
| `kb+openspec` | ✓ | Godot 中删除对象并释放内存涉及以下关键符号：  / 操作 / 符号 / 位置 / /--- | 2374 | 3 | 2 | 18.21 |  |

### q04 · code_retrieval
**题**：a star pathfinding  ·  **gold**：AStar

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | Godot core 中 A* 寻路相关的类：  - **`AStar`** — 通用 3D A | 960 | 2 | 1 | 8.59 |  |
| `kb` | ✓ | A* 寻路相关核心符号：  - **`AStar3D`** — 3D A* 寻路类，位于 `ma | 729 | 2 | 1 | 10.09 |  |
| `kb+superpowers` | ✓ | Godot core 中的 A* 寻路实现：  - **`AStar3D`** — 3D A*  | 1080 | 2 | 1 | 11.46 |  |
| `kb+openspec` | ✓ | Godot core 中的 A* 寻路实现：  - **`AStar3D`** — 3D A*  | 1588 | 2 | 1 | 13.2 |  |

## 各臂速览
- `no-kb`: acc=0.75 · tokens=3062.5 · llm_calls=4.25 · steps=5 · t=23.71s · tools=1.5
- `kb`: acc=0.5 · tokens=891.2 · llm_calls=2 · steps=1 · t=9.85s · tools=1
- `kb+superpowers`: acc=0.75 · tokens=1944 · llm_calls=2.75 · steps=2 · t=15.14s · tools=1.25
- `kb+openspec`: acc=0.75 · tokens=1984.5 · llm_calls=2.5 · steps=1.5 · t=14.43s · tools=1

## 诚实边界（必须看）
- **accuracy 由 GLM 生成 + GLM 判分**（同家族 self-preference）→ 相对参考值，非绝对回归值。
- **skills 臂注入的是 bundled 精简 SOP 文本**（`eval/arms/skills_bundled/`），**非完整 Claude Code skill 运行时**（无触发机制/hook）。是 headless 可复现近似，不等于真实 skill 效果。
- **`cost_$` 依赖 MODEL_PRICES 单价**，单价未知则 0（占位）；当前价格为占位，勿当真实成本。
- 样本量小（4 题），结论显著性有限——看趋势勿绝对化。
- bug_fix 题仍用 symbol/file broad match 判分（非修复质量 LLM-judge）。

## 怎么看 skills 值不值
对比 `kb+superpowers` / `kb+openspec` vs `kb` 的 accuracy（skills 帮没帮）+ mean_total_tokens（skills 多花多少）。**bug_fix 题上差异最可能显现**（纯 code_retrieval 上 skills 显不出价值）。

详见 `summary.json`（臂×指标矩阵，程序消费用）、各臂 `arms/<arm>/`（config + aggregate + episodes）。

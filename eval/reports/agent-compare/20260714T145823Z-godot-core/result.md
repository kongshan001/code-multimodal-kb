# agent-compare 结果 · target=godot-core · model=glm-5.1
> 8 题 × 1 runs × 4 臂。

## 怎么读懂这份报告（规则，先看）

**4 个臂是什么**：
- `no-kb` = 只给 grep + 读文件（朴素搜索，无知识库）
- `kb` = 给 cmm 代码知识库（语义检索符号）
- `kb+superpowers` / `kb+openspec` = kb + 往 agent 指令里注入 superpowers/openspec 的工程纪律 SOP
  （注入的是**精简 SOP 文本**，不是真 skill 运行时——见末尾诚实边界）

**答对（✓）怎么判**：终答里含 gold 符号或文件名就算对（broad 子串匹配，零 LLM judge）。
**gold 是什么**：每题的标准答案——来自 codegraph 挖出的真实代码符号/文件，构造即正确（不是人拍脑袋写的）。

**某题被标截断（逐题表 `截断` 列 ⚠ / `truncated_rate` > 0）**：agent 跑满步数上限（非 skills 臂 **8 轮**、skills 臂 **12 轮**）没自然收敛，系统**强制要了一个最佳答案**（不让它空着）——所以那题的答案是它的**猜测**，不一定对。多半发生在 no-kb（grep 找不到、烧满步数）。上限是控成本护栏，防无限调工具。

**`thinking` / 思考过程**：GLM-5.1 经这个端点不返独立 thinking block，所以思考 = agent 的推理文本（assistant 回答），不是单独的隐藏思维链——别当成完整思考链。
**`cost_$`**：token × 单价；单价是**占位**（待确认 GLM 定价），勿当真实成本，看相对大小即可。
**`tool_diversity` 高**：可能 agent 在乱试不同工具（没方向），未必好事。

## 谁赢
- **准确率最高**：`no-kb`（accuracy=0.875）
- **最省 token**：`kb`（mean_total_tokens=1857.2）
- **最省钱**：`kb`（mean_cost_$=0.0013）
- **KB vs 无 KB token 压缩**：2.75×（>1 = KB 省）

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
| `no-kb` | 0.875 | 5103.5 | 6.75 | 7.25 | 36.4 | 0.0036 | 1.75 | 0.375 | 8 |
| `kb` | 0.875 | 1857.2 | 3 | 2 | 16.48 | 0.0013 | 1.12 | 0.125 | 8 |
| `kb+superpowers` | 0.875 | 2132.9 | 3.12 | 2.12 | 18.39 | 0.0015 | 1.25 | 0.0 | 8 |
| `kb+openspec` | 0.875 | 2136.2 | 2.75 | 1.75 | 15.53 | 0.0015 | 1.12 | 0.0 | 8 |

## 逐题得分对照

> 每题各臂的答对 / 答案 / 指标（8 题 × 4 臂）。看哪题谁答对、谁省 token、谁卡住。

### q01 · code_retrieval
**题**：string format  ·  **gold**：vformat

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✗ | `String::format` | 6739 | 9 | 9 | 43.37 | ⚠卡住 |
| `kb` | ✗ | `String::format` — 定义在 `core/string/ustring.cpp` | 934 | 2 | 1 | 7.78 |  |
| `kb+superpowers` | ✗ | `String::format` — 定义在 `core/string/ustring.cpp` | 1606 | 2 | 1 | 9.32 |  |
| `kb+openspec` | ✗ | `String::format` — 定义在 `core/string/ustring.cpp` | 1482 | 2 | 1 | 8.01 |  |

### q02 · code_retrieval
**题**：int to string  ·  **gold**：itos

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | `itos` | 7364 | 9 | 10 | 37.23 | ⚠卡住 |
| `kb` | ✓ | `itos()` — 定义在 `string/ustring.cpp`，将 `int` 转为 ` | 926 | 2 | 1 | 12.21 |  |
| `kb+superpowers` | ✓ | **`itos`** — `core/string/ustring.cpp`  将 `int`  | 1623 | 2 | 1 | 10.34 |  |
| `kb+openspec` | ✓ | `itos()` — 定义在 `core/string/ustring.cpp`，将 `int6 | 2476 | 3 | 2 | 12.59 |  |

### q03 · code_retrieval
**题**：delete object free memory  ·  **gold**：memdelete

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | 在 Godot core 中，删除对象/释放内存涉及以下关键符号（定义于 `core/os/me | 8183 | 7 | 8 | 47.93 |  |
| `kb` | ✓ | `memdelete`、`memdelete_allocator`、`memdelete_arr | 6944 | 9 | 8 | 32.97 | ⚠卡住 |
| `kb+superpowers` | ✓ | Godot 中删除对象并释放内存的核心函数：  - **`memdelete`** — 删除通过 | 1770 | 3 | 2 | 12.61 |  |
| `kb+openspec` | ✓ | Godot 中删除对象/释放内存的核心函数：  / 函数 / 用途 / /---/---/ /  | 1599 | 2 | 1 | 12.72 |  |

### q04 · code_retrieval
**题**：a star pathfinding  ·  **gold**：AStar

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | Godot core 中 A* 寻路相关的类：  - **`AStar`** — 通用 3D A | 966 | 2 | 1 | 10.31 |  |
| `kb` | ✓ | Godot core 中 A* 寻路相关的核心符号：  - **`AStar3D`** — 3D | 1064 | 2 | 1 | 10.75 |  |
| `kb+superpowers` | ✓ | Godot core 中 A* 寻路相关的核心类/符号：  - **`AStar3D`** —  | 2363 | 5 | 4 | 31.74 |  |
| `kb+openspec` | ✓ | Godot 的 A* 寻路实现位于 `core/math/a_star.cpp`，核心类和函数： | 1703 | 2 | 1 | 16.27 |  |

### q05 · code_retrieval
**题**：operating system abstraction  ·  **gold**：OS

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | Godot 的操作系统抽象层核心是：  - **`OS`** — 基类，定义在 `core/os | 6270 | 8 | 14 | 49.36 |  |
| `kb` | ✓ | Godot 的操作系统抽象层核心是：  - **`OS`** (`os/os.h`, `os/o | 1824 | 3 | 2 | 25.59 |  |
| `kb+superpowers` | ✓ | Godot 的操作系统抽象层核心是：  ## 核心类  - **`OS`** (`core/os | 5532 | 7 | 6 | 42.52 |  |
| `kb+openspec` | ✓ | Godot 的操作系统抽象层主要由以下符号构成：  - **`OS`** (`core/os/o | 2605 | 3 | 2 | 14.21 |  |

### q06 · code_retrieval
**题**：color  ·  **gold**：Color

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | `Color` 类型定义在：  - **`core/math/color.h`** — 类声明  | 1586 | 4 | 3 | 20.99 |  |
| `kb` | ✓ | `Color` 类定义在 **`core/math/color.h`** 中，实现在 **`co | 952 | 2 | 1 | 13.05 |  |
| `kb+superpowers` | ✓ | `Color` — 定义在 `core/math/color.h`，实现在 `core/math | 961 | 2 | 1 | 11.22 |  |
| `kb+openspec` | ✓ | `Color` — 定义于 `core/math/color.h`，实现在 `core/math | 1181 | 2 | 1 | 8.93 |  |

### q07 · code_retrieval
**题**：vector2  ·  **gold**：Vector2

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | `Vector2` 定义在 **`core/math/vector2.h`**，是一个 `str | 5041 | 6 | 5 | 41.25 |  |
| `kb` | ✓ | `Vector2` 定义在 **`core/math/vector2.h`**，实现在 **`c | 1161 | 2 | 1 | 18.57 |  |
| `kb+superpowers` | ✓ | `Vector2` 定义在 **`core/math/vector2.h`**，实现在 **`c | 1751 | 2 | 1 | 16.85 |  |
| `kb+openspec` | ✓ | `Vector2` 定义在 **`math/vector2.h`** / **`math/vec | 4377 | 6 | 5 | 36.58 |  |

### q08 · code_retrieval
**题**：vector3  ·  **gold**：Vector3

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | `Vector3`（定义于 `core/math/vector3.h`） | 4679 | 9 | 8 | 40.75 | ⚠卡住 |
| `kb` | ✓ | `Vector3` 定义在 **`core/math/vector3.h`**，实现在 **`c | 1053 | 2 | 1 | 10.93 |  |
| `kb+superpowers` | ✓ | `Vector3` — 定义在 `core/math/vector3.h`，实现在 `core/ | 1457 | 2 | 1 | 12.49 |  |
| `kb+openspec` | ✓ | `Vector3` 定义在 **`core/math/vector3.h`**（实现文件 `co | 1667 | 2 | 1 | 14.95 |  |

## 各臂速览
- `no-kb`: acc=0.875 · tokens=5103.5 · llm_calls=6.75 · steps=7.25 · t=36.4s · tools=1.75
- `kb`: acc=0.875 · tokens=1857.2 · llm_calls=3 · steps=2 · t=16.48s · tools=1.12
- `kb+superpowers`: acc=0.875 · tokens=2132.9 · llm_calls=3.12 · steps=2.12 · t=18.39s · tools=1.25
- `kb+openspec`: acc=0.875 · tokens=2136.2 · llm_calls=2.75 · steps=1.75 · t=15.53s · tools=1.12

## 诚实边界（必须看）
- **accuracy 由 GLM 生成 + GLM 判分**（同家族 self-preference）→ 相对参考值，非绝对回归值。
- **skills 臂注入的是 bundled 精简 SOP 文本**（`eval/arms/skills_bundled/`），**非完整 Claude Code skill 运行时**（无触发机制/hook）。是 headless 可复现近似，不等于真实 skill 效果。
- **`cost_$` 依赖 MODEL_PRICES 单价**，单价未知则 0（占位）；当前价格为占位，勿当真实成本。
- 样本量小（8 题），结论显著性有限——看趋势勿绝对化。
- bug_fix 题仍用 symbol/file broad match 判分（非修复质量 LLM-judge）。

## 怎么看 skills 值不值
对比 `kb+superpowers` / `kb+openspec` vs `kb` 的 accuracy（skills 帮没帮）+ mean_total_tokens（skills 多花多少）。**bug_fix 题上差异最可能显现**（纯 code_retrieval 上 skills 显不出价值）。

详见 `summary.json`（臂×指标矩阵，程序消费用）、各臂 `arms/<arm>/`（config + aggregate + episodes）。

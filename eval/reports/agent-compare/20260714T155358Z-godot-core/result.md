# agent-compare 结果 · target=godot-core · model=glm-5.1
> 4 题 × 1 runs × 4 臂。

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
- **准确率最高**：`no-kb`（accuracy=0.75）
- **最省 token**：`kb`（mean_total_tokens=2736.8）
- **最省钱**：`kb`（mean_cost_$=0.0019）
- **KB vs 无 KB token 压缩**：2.17×（>1 = KB 省）

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
| `no-kb` | 0.75 | 5937.5 | 7.75 | 8.75 | 53.4 | 0.0042 | 2 | 0.5 | 4 |
| `kb` | 0.75 | 2736.8 | 4 | 3 | 29.13 | 0.0019 | 1.25 | 0.0 | 4 |
| `kb+superpowers` | 0.75 | 7321.2 | 5.5 | 4.5 | 36.84 | 0.0051 | 1.25 | 0.25 | 4 |
| `kb+openspec` | 0.75 | 2777.5 | 3 | 2.25 | 28.15 | 0.0019 | 1.25 | 0.0 | 4 |

## 逐题得分对照

> 每题各臂的答对 / 答案 / 指标（4 题 × 4 臂）。看哪题谁答对、谁省 token、谁卡住。

### q01 · code_retrieval
**题**：string format  ·  **gold**：vformat

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✗ | Godot 中 `String` 的格式化相关方法/符号：  - **`String::form | 7523 | 8 | 13 | 43.0 |  |
| `kb` | ✗ | 核心符号是 **`String::format`**（定义于 `core/string/ustr | 5121 | 7 | 6 | 36.01 |  |
| `kb+superpowers` | ✗ | `String::format` — 定义在 `core/string/ustring.cpp` | 1608 | 2 | 1 | 9.83 |  |
| `kb+openspec` | ✗ | `String::format` — 定义在 `core/string/ustring.cpp` | 1557 | 2 | 1 | 8.5 |  |

### q02 · code_retrieval
**题**：int to string  ·  **gold**：itos

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | `itos` | 7599 | 9 | 9 | 33.01 | ⚠卡住 |
| `kb` | ✓ | `itos()` — 定义在 `string/ustring.cpp`，将 `int` 转为 ` | 926 | 2 | 1 | 7.89 |  |
| `kb+superpowers` | ✓ | Godot core 中 int → string 的主要方式：  - **`itos(int) | 4133 | 5 | 4 | 25.1 |  |
| `kb+openspec` | ✓ | **`itos`** — `String itos(int64_t p_val)`，定义在 `c | 1470 | 2 | 1 | 22.67 |  |

### q03 · code_retrieval
**题**：delete object free memory  ·  **gold**：memdelete

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | In Godot core (`core/os/memory.h`), deleting obj | 4003 | 5 | 5 | 26.71 |  |
| `kb` | ✓ | 在 Godot core 中，删除对象/释放内存涉及以下关键符号：  ### 内存释放（底层）  | 3866 | 5 | 4 | 30.67 |  |
| `kb+superpowers` | ✓ | `memdelete`、`Object::_predelete`、`Object::cancel | 21816 | 13 | 12 | 94.1 | ⚠卡住 |
| `kb+openspec` | ✓ | 在 Godot core 中，删除对象/释放内存涉及以下关键符号：  ## 内存释放（底层）   | 5328 | 5 | 5 | 54.26 |  |

### q04 · code_retrieval
**题**：a star pathfinding  ·  **gold**：AStar

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | `AStar`、`AStar2D`、`AStarGrid2D` | 4625 | 9 | 8 | 110.87 | ⚠卡住 |
| `kb` | ✓ | A* 寻路相关核心符号：  - **`AStar3D`** — 3D A* 寻路类，定义于 `m | 1034 | 2 | 1 | 41.95 |  |
| `kb+superpowers` | ✓ | Godot 的 A* 寻路实现在 `core/math/a_star.cpp`，核心类和函数：  | 1728 | 2 | 1 | 18.34 |  |
| `kb+openspec` | ✓ | Godot core 中 A* 寻路相关的核心符号：  / 符号 / 位置 / /---/--- | 2755 | 3 | 2 | 27.17 |  |

## 各臂速览
- `no-kb`: acc=0.75 · tokens=5937.5 · llm_calls=7.75 · steps=8.75 · t=53.4s · tools=2
- `kb`: acc=0.75 · tokens=2736.8 · llm_calls=4 · steps=3 · t=29.13s · tools=1.25
- `kb+superpowers`: acc=0.75 · tokens=7321.2 · llm_calls=5.5 · steps=4.5 · t=36.84s · tools=1.25
- `kb+openspec`: acc=0.75 · tokens=2777.5 · llm_calls=3 · steps=2.25 · t=28.15s · tools=1.25

## 诚实边界（必须看）
- **accuracy 由 GLM 生成 + GLM 判分**（同家族 self-preference）→ 相对参考值，非绝对回归值。
- **skills 臂注入的是 bundled 精简 SOP 文本**（`eval/arms/skills_bundled/`），**非完整 Claude Code skill 运行时**（无触发机制/hook）。是 headless 可复现近似，不等于真实 skill 效果。
- **`cost_$` 依赖 MODEL_PRICES 单价**，单价未知则 0（占位）；当前价格为占位，勿当真实成本。
- 样本量小（4 题），结论显著性有限——看趋势勿绝对化。
- bug_fix 题仍用 symbol/file broad match 判分（非修复质量 LLM-judge）。

## 怎么看 skills 值不值
对比 `kb+superpowers` / `kb+openspec` vs `kb` 的 accuracy（skills 帮没帮）+ mean_total_tokens（skills 多花多少）。**bug_fix 题上差异最可能显现**（纯 code_retrieval 上 skills 显不出价值）。

详见 `summary.json`（臂×指标矩阵，程序消费用）、各臂 `arms/<arm>/`（config + aggregate + episodes）。

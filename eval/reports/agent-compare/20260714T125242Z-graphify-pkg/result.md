# agent-compare 结果 · target=graphify-pkg · model=glm-5.1
> 2 题 × 1 runs × 4 臂。

## 谁赢
- **准确率最高**：`kb`（accuracy=1）
- **最省 token**：`kb`（mean_total_tokens=1025）
- **最省钱**：`kb`（mean_cost_$=0.0008）
- **KB vs 无 KB token 压缩**：2.68×（>1 = KB 省）

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
| `no-kb` | 0 | 2743 | 6 | 10.5 | 44.3 | 0.0019 | 1.5 | 1.0 | 2 |
| `kb` | 1 | 1025 | 2 | 1 | 15.21 | 0.0008 | 1 | 0.0 | 2 |
| `kb+superpowers` | 1 | 1498 | 2 | 1 | 11.54 | 0.001 | 1 | 0.0 | 2 |
| `kb+openspec` | 1 | 1523 | 2 | 1 | 12.14 | 0.0011 | 1 | 0.0 | 2 |

## 逐题得分对照

> 每题各臂的答对 / 答案 / 指标（2 题 × 4 臂）。看哪题谁答对、谁省 token、谁卡住。

### q01 · code_retrieval
**题**：id construction  ·  **gold**：_make_id

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✗ | (max_steps reached without final answer) | 2687 | 6 | 10 | 52.53 | ⚠卡住 |
| `kb` | ✓ | ID 构造相关的核心符号：  / 符号 / 所在文件 / /---/---/ / `make_i | 1076 | 2 | 1 | 18.25 |  |
| `kb+superpowers` | ✓ | ID 构造相关的符号：  / 符号 / 所在文件 / /---/---/ / `make_id` | 1674 | 2 | 1 | 15.19 |  |
| `kb+openspec` | ✓ | ID 构建相关的符号：  / 符号 / 所在文件 / /---/---/ / `make_id` | 1570 | 2 | 1 | 12.62 |  |

### q02 · code_retrieval
**题**：build graph from json  ·  **gold**：build_from_json

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✗ | (max_steps reached without final answer) | 2799 | 6 | 11 | 36.06 | ⚠卡住 |
| `kb` | ✓ | 核心函数是 **`build_from_json`**，位于 `graphify/build/b | 974 | 2 | 1 | 12.18 |  |
| `kb+superpowers` | ✓ | 核心函数是 **`build_from_json`**，位于 `graphify.build`  | 1322 | 2 | 1 | 7.88 |  |
| `kb+openspec` | ✓ | `build_from_json` — 位于 `graphify/build/build.py` | 1476 | 2 | 1 | 11.67 |  |

## 各臂速览
- `no-kb`: acc=0 · tokens=2743 · llm_calls=6 · steps=10.5 · t=44.3s · tools=1.5
- `kb`: acc=1 · tokens=1025 · llm_calls=2 · steps=1 · t=15.21s · tools=1
- `kb+superpowers`: acc=1 · tokens=1498 · llm_calls=2 · steps=1 · t=11.54s · tools=1
- `kb+openspec`: acc=1 · tokens=1523 · llm_calls=2 · steps=1 · t=12.14s · tools=1

## 诚实边界（必须看）
- **accuracy 由 GLM 生成 + GLM 判分**（同家族 self-preference）→ 相对参考值，非绝对回归值。
- **skills 臂注入的是 bundled 精简 SOP 文本**（`eval/arms/skills_bundled/`），**非完整 Claude Code skill 运行时**（无触发机制/hook）。是 headless 可复现近似，不等于真实 skill 效果。
- **`cost_$` 依赖 MODEL_PRICES 单价**，单价未知则 0（占位）；当前价格为占位，勿当真实成本。
- 样本量小（2 题），结论显著性有限——看趋势勿绝对化。
- bug_fix 题仍用 symbol/file broad match 判分（非修复质量 LLM-judge）。

## 怎么看 skills 值不值
对比 `kb+superpowers` / `kb+openspec` vs `kb` 的 accuracy（skills 帮没帮）+ mean_total_tokens（skills 多花多少）。**bug_fix 题上差异最可能显现**（纯 code_retrieval 上 skills 显不出价值）。

详见 `summary.json`（臂×指标矩阵，程序消费用）、各臂 `arms/<arm>/`（config + aggregate + episodes）。

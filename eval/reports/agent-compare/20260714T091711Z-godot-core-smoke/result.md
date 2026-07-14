# agent-compare 结果 · target=godot-core · model=mock（**SMOKE / mock**，非真实 LLM 跑）
> 3 题 × 1 runs × 4 臂。

## 谁赢
- **准确率最高**：`no-kb`（accuracy=0.667）
- **最省 token**：`no-kb`（mean_total_tokens=131）
- **最省钱**：`no-kb`（mean_cost_$=0.0001）
- **KB vs 无 KB token 压缩**：1.0×（>1 = KB 省）

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
| `no-kb` | 0.667 | 131 | 2 | 1 | 0.57 | 0.0001 | 1 | 0.0 | 3 |
| `kb` | 0.667 | 131 | 2 | 1 | 0.57 | 0.0001 | 1 | 0.0 | 3 |
| `kb+superpowers` | 0.667 | 141 | 3 | 2 | 0.87 | 0.0001 | 2 | 0.0 | 3 |
| `kb+openspec` | 0.667 | 141 | 3 | 2 | 0.87 | 0.0001 | 2 | 0.0 | 3 |

## 各臂速览
- `no-kb`: acc=0.667 · tokens=131 · llm_calls=2 · steps=1 · t=0.57s · tools=1
- `kb`: acc=0.667 · tokens=131 · llm_calls=2 · steps=1 · t=0.57s · tools=1
- `kb+superpowers`: acc=0.667 · tokens=141 · llm_calls=3 · steps=2 · t=0.87s · tools=2
- `kb+openspec`: acc=0.667 · tokens=141 · llm_calls=3 · steps=2 · t=0.87s · tools=2

## 诚实边界（必须看）
- **accuracy 由 GLM 生成 + GLM 判分**（同家族 self-preference）→ 相对参考值，非绝对回归值。
- **skills 臂注入的是 bundled 精简 SOP 文本**（`eval/arms/skills_bundled/`），**非完整 Claude Code skill 运行时**（无触发机制/hook）。是 headless 可复现近似，不等于真实 skill 效果。
- **`cost_$` 依赖 MODEL_PRICES 单价**，单价未知则 0（占位）；当前价格为占位，勿当真实成本。
- 样本量小（3 题），结论显著性有限——看趋势勿绝对化。
- bug_fix 题仍用 symbol/file broad match 判分（非修复质量 LLM-judge）。

## 怎么看 skills 值不值
对比 `kb+superpowers` / `kb+openspec` vs `kb` 的 accuracy（skills 帮没帮）+ mean_total_tokens（skills 多花多少）。**bug_fix 题上差异最可能显现**（纯 code_retrieval 上 skills 显不出价值）。

详见 `summary.json`（臂×指标矩阵，程序消费用）、各臂 `arms/<arm>/`（config + aggregate + episodes）。

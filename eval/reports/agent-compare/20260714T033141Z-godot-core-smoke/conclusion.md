# agent-compare 结论 · target=godot-core · model=mock（**SMOKE / mock**，非真实 LLM 跑）
> 4 题 × 1 runs × 4 臂。

## 谁赢
- **准确率最高**：`no-kb`（accuracy=0.5）
- **最省 token**：`no-kb`（mean_total_tokens=136.5）
- **最省钱**：`no-kb`（mean_cost_$=0.0001）
- **KB vs 无 KB token 压缩**：1.0×（>1 = KB 省）

## 诚实边界（必须看）
- **accuracy 由 GLM 生成 + GLM 判分**（同家族 self-preference）→ 相对参考值，非绝对回归值。
- **skills 臂注入的是 bundled 精简 SOP 文本**（`eval/arms/skills_bundled/`），**非完整 Claude Code skill 运行时**（无触发机制/hook）。是 headless 可复现近似，不等于真实 skill 效果。
- **`cost_$` 依赖 MODEL_PRICES 单价**，单价未知则 0（占位）；当前价格为占位，勿当真实成本。
- 样本量小（4 题），结论显著性有限——看趋势勿绝对化。
- bug_fix 题仍用 symbol/file broad match 判分（非修复质量 LLM-judge）。

## 各臂速览
- `no-kb`: acc=0.5 · tokens=136.5 · llm_calls=2 · steps=1 · t=0.6s · tools=1
- `kb`: acc=0.5 · tokens=136.5 · llm_calls=2 · steps=1 · t=0.6s · tools=1
- `kb+superpowers`: acc=0.5 · tokens=146.5 · llm_calls=3 · steps=2 · t=0.91s · tools=2
- `kb+openspec`: acc=0.5 · tokens=146.5 · llm_calls=3 · steps=2 · t=0.91s · tools=2

详见 `summary.json`（臂×指标矩阵）、`matrix.md`、各臂 `arms/<arm>/`。

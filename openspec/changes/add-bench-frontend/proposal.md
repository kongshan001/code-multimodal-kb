# Proposal: add-bench-frontend

## Why

bench CLI（`python -m eval.cli`）功能完整但**门槛在命令行**——要记子命令、读 JSON、手拼对比。
对非作者用户，"跑一次评测 / 看懂结果 / 对比两版"都得进终端。评测的价值（驱动改进）依赖**被人看见**，
CLI 形态限制了它的受众。一个轻量前端可视化层能把"出题→跑→看→比"变成点点点，显著降门槛。

## What

给 bench CLI 加一个**前端可视化层**（不是重写后端）：
- 后端不变：`eval.cli` 仍是单一事实源 + 归档 JSON 是统一 schema。
- 前端两层：
  - **Tier 1 读视图**（最低门槛）：静态 SPA，读 `eval/reports/archive/*.json` + `index.json`，浏览器打开即用，零后端。
  - **Tier 2 交互层**（可选）：薄 Flask/FastAPI 包一层 `eval.cli`（触发 run / goldgen / compare），UI 可点。

## Capabilities（受影响的 capability）

- 新 capability `bench-frontend`：评测结果的可视化消费 + 评测流程的 UI 触发。
- 复用 `evaluation` capability 的归档 schema（不重定义指标 / gold）。

## Impact

- **降门槛**：接入成本从"学 CLI"降到"开网页"。非作者用户、团队评审、演示场景都能直接看。
- **不破坏 CLI**：CLI 仍是后端 + CI/自动化通路；前端是消费层。
- **诚实**：前端不造数——所有显示来自归档 JSON（lockfile / 边界一并展示），保留 LLM-judged 等标注。

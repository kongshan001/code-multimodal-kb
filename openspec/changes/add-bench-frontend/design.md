# Design: add-bench-frontend

## 美学方向 · "Measurement Lab"（仪器/编辑混合）

避开通用 dashboard slop（紫色渐变白底 + Inter + 卡片网格）。项目本身是**评测体检台**，
视觉走"科学仪器 + 编辑数据新闻"——和现有 fireworks-tech-graph 流程图（style 6 Claude 官方风）
**同一品牌**：暖奶油底 `#f8f6f3`、有性格的字、超大指标数字做主角。

- **字体**：`Fraunces`（衬线展示，标题/ italic 强调）+ `JetBrains Mono`（数据/指标/元信息）+ `IBM Plex Sans`（正文）。不用 Inter/Roboto/system。
- **色板**：奶油 `#f8f6f3` 底 + 深墨 `#1a1814` 文 + 单一强调色**烟花橙 `#c75b39`**（hero 数字 / 异常 / codegraph 臂）。语义软色（teal/blue/beige）与流程图同源。
- **版式**：编辑式不对称、细规则线分栏、大留白；hero 指标用 40px mono 数字（recall/faithfulness IS the story）。
- **不做**：浮夸阴影/渐变、3 列等高 feature 卡、紫色 hero。

参考实现（已落）`docs/mockup/dashboard.html`——单文件 HTML + 内联 CSS，可浏览器直接开。

## 信息架构 · 6 个视图

| 视图 | 对应 CLI | 做什么 |
|---|---|---|
| **Dashboard**（首屏）| list-reports 聚合 | 4 个 hero 指标 + 价值定位 §7 网格（●●○○）+ A/B 四臂条形 + 最近 run 列表 |
| **Run console** | `bench run <subject>` | 选 subject + 参数 → 触发 → 实时进度 → 结果摘要（Tier2 需后端；Tier1 跳 CLI）|
| **Reports archive** | `list-reports` / `show <id>` | 时间线/表，按 subject 过滤，点进看 per_query + lockfile + 图 |
| **Compare** | `compare <id1> <id2>` | 两份报告 aggregate diff 表 + A/B 多臂横评条形 |
| **Gold lab** | `goldgen` / `-verify` / `-fold` | 扩题 4 阶段可视化：seed 输入 → 候选队列（带 verdict 徽标）→ 逐条 approve/edit → fold（Tier2 交互核心）|
| **Report detail** | `show <id>` | 单报告：aggregate + per_query 表 + lockfile + 边界标注（LLM-judged 等）|

## 技术栈 · 分层（降门槛优先）

| 层 | 栈 | 能做 | 门槛 |
|---|---|---|---|
| **Tier 1 读视图**（必做）| Vite + React（或 vanilla SPA）+ 手写 SVG 图 | 读 `archive/*.json` + `index.json` → Dashboard/Reports/Compare/Detail。纯静态，浏览器开 | **最低**（`open index.html` 或静态托管）|
| **Tier 2 交互**（可选）| + 薄 Flask/FastAPI（`POST /api/run`、`/api/goldgen`、`/api/compare` 子进程包 `eval.cli`，SSE 流式进度）| Run console + Gold lab 全交互（点按钮触发评测/goldgen）| 中（跑个 `flask run`）|

**图表**：手写 SVG 条形/点阵（mockup 已示，on-brand），重交互才上 visx/Recharts。
**不引**重型 UI 框架（MUI/AntD 之类）——与"仪器/编辑"美学冲突。

## 数据流（前端不造数）

```
Tier1（读）:  前端 ──fetch──▶ eval/reports/archive/*.json + index.json（统一 schema，已有）
Tier2（交互）: 前端 ──HTTP──▶ Flask wrapper ──subprocess──▶ python -m eval.cli ...
                                   └─ SSE 流 stdout 进度 ──▶ 前端
归档 JSON 仍是唯一事实源；前端只渲染 + 标注边界（lockfile / LLM-judged / self-preference 一并显示）。
```

## 关键页面设计要点

- **Dashboard hero**：4 个数字（代码 broad@5 / 记忆 hit@5 / A/B 省 token / 答案 faithfulness）——本项目最硬的结论一眼可见。
- **价值定位 §7 网格**：维度 × {检索/agent/答案质量} 的 ●●○○ 点阵 + 证据列——回答"哪层已量化"。
- **A/B 四臂条形**：准确度 + token 双列，codegraph 橙色突出（最准）。
- **Gold lab**：每条 candidate 一个卡，实证 verdict（✓/⚠）+ subagent verdict（✓/✗/✏）双徽标 + 一键 approve/edit——把两层验收 + 人审做成 UI。
- **边界标注**：每个 LLM-judged 分都带 `self-preference` 徽标（诚实，不藏）。

## 非目标

- 不评 agent 端到端回答质量（归 evaluation capability）。
- 不重算指标（只读归档）。
- 不做用户系统/多租户（本地/小团队工具）。
- Tier1 不触发 run（纯读；触发走 Tier2 或 CLI）。

## Open Questions

- Tier1 用 Vite+React 还是 vanilla 单文件？React 利于 Gold lab 交互；vanilla 利于"开箱即用"。倾向 React+Vite（Gold lab 体验更好），产物静态托管。
- Tier2 后端进不进本仓库？倾向进（`eval/server.py` 薄 Flask，复用 `eval.cli`）。

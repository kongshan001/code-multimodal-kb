## 1. Tier 1 读视图（静态 SPA · 必做）

- [ ] 1.1 脚手架：Vite + React + 路由，`docs/mockup/dashboard.html` 的 Measurement Lab 美学抽成 design tokens（cream 底 / Fraunces+JetBrains Mono / 烟花橙强调）→ 验证：开发服务器起，字体/色板与 mockup 一致
- [ ] 1.2 数据层：读 `eval/reports/archive/index.json` + 单份 `*.json`（fetch，统一 schema 已有）→ 验证：Dashboard 渲染真实归档（非写死）
- [ ] 1.3 Dashboard 页：4 hero 指标 + 价值定位 §7 网格 + A/B 四臂条形（手写 SVG）+ 最近 run 列表 → 验证：对当前 10 份归档渲染正确
- [ ] 1.4 Reports archive 页：时间线/表 + subject 过滤 + 点进 detail
- [ ] 1.5 Report detail 页：aggregate + per_query 表 + lockfile + LLM-judged 徽标（边界随分数显示）
- [ ] 1.6 Compare 页：两 id 的 aggregate diff 表 + A/B 多臂横评条形
- [ ] 1.7 静态构建 + 托管说明（`vite build` → 静态文件，open 即用 / GitHub Pages）

## 2. Tier 2 交互层（薄后端 · 可选）

- [ ] 2.1 `eval/server.py`：薄 Flask，`POST /api/run`、`/api/goldgen`、`/api/goldgen-verify`、`/api/goldgen-fold`、`/api/compare`，subprocess 包 `eval.cli`，SSE 流 stdout → 验证：curl 触发 run，stdout 流回
- [ ] 2.2 Run console 页：subject+参数表单 → 触发 → SSE 进度 → 结果摘要
- [ ] 2.3 Gold lab 页：seed 输入 → 候选队列（实证+subagent 双 verdict 徽标）→ 逐条 approve/edit → fold

## 3. 文档 + 收尾

- [ ] 3.1 README/runbook 加"前端"段（Tier1 怎么开 / Tier2 怎么起后端）
- [ ] 3.2 mockup 与实装一致（Dashboard 实装对照 docs/mockup/dashboard.html 不走样）
- [ ] 3.3 提交 + push（带 Co-Authored-By）

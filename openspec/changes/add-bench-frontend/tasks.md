## 0. Tier 2 后端骨架（接入段 + 评测交互都依赖）

- [ ] 0.1 `eval/server.py` 薄 Flask：`POST /api/setup`（包 setup.sh）、`/api/health`（依赖探测）、`/api/onboard/{index,docgraph,mine}`（包 cmm/codegraph/graphify/mempalace）、`/api/run`、`/api/goldgen*`、`/api/compare`，全 subprocess + SSE 流 stdout → 验证：curl 各端点能触发 + 流回

## 1. 接入段（Tier 2 · 环境 + 目标工程）

- [ ] 1.1 Setup 视图：依赖体检表（cmm/graphify/codegraph/mempalace/python/render/creds 逐项 ✓版本/✗缺，复用 setup.sh 探测）+ 一键装（subprocess setup.sh，SSE 日志）+ 健康检查（pytest 冒烟）+ 顶端就绪灯 → 验证：缺项能装、装完转绿
- [ ] 1.2 Project onboarding 5 步向导：连代码库→cmm+codegraph 索引（进度）→(可选 文档图，成本警示)→(可选 会话 mine，hook 警示)→gold（复用 Gold lab）→就绪（列可 bench 的 target）→ 验证：接一个新代码库走完 5 步能 bench run
- [ ] 1.3 向导状态持久化（localStorage 或后端），接了一半可续

## 2. Tier 1 读视图（静态 SPA · 评测段）

- [ ] 2.1 脚手架：Vite + React + 路由，`docs/mockup/dashboard.html` 的 Measurement Lab 美学抽成 design tokens（cream 底 / Fraunces+JetBrains Mono / 烟花橙强调）→ 验证：开发服务器起，字体/色板与 mockup 一致
- [ ] 2.2 数据层：读 `eval/reports/archive/index.json` + 单份 `*.json`（fetch，统一 schema 已有）→ 验证：Dashboard 渲染真实归档（非写死）
- [ ] 2.3 Dashboard 页：4 hero 指标 + 价值定位 §7 网格 + A/B 四臂条形（手写 SVG）+ 最近 run 列表 → 验证：对当前 10 份归档渲染正确
- [ ] 2.4 Reports archive 页：时间线/表 + subject 过滤 + 点进 detail
- [ ] 2.5 Report detail 页：aggregate + per_query 表 + lockfile + LLM-judged 徽标（边界随分数显示）
- [ ] 2.6 Compare 页：两 id 的 aggregate diff 表 + A/B 多臂横评条形
- [ ] 2.7 静态构建 + 托管说明（`vite build` → 静态文件，open 即用 / GitHub Pages）

## 3. Tier 2 评测交互（薄后端）

- [ ] 3.1 Run console 页：subject+参数表单 → `/api/run` → SSE 进度 → 结果摘要 + 自动归档刷新
- [ ] 3.2 Gold lab 页：seed 输入 → 候选队列（实证+subagent 双 verdict 徽标）→ 逐条 approve/edit → fold

## 4. 文档 + 收尾

- [ ] 4.1 README/runbook 加"前端"段（Tier1 怎么开 / Tier2 怎么起后端 / 接入向导怎么走）
- [ ] 4.2 mockup 与实装一致（Dashboard 实装对照 docs/mockup/dashboard.html 不走样）
- [ ] 4.3 提交 + push（带 Co-Authored-By）

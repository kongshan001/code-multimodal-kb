## 0. Tier 2 后端骨架（接入段 + 评测交互都依赖）

- [x] 0.1 `eval/server.py` 薄后端（**stdlib http.server，零依赖**）：GET / (SPA) + /web/* 静态 + /api/reports + /api/report/<id> + /api/health（依赖探测）+ POST /api/run / /api/goldgen / /api/onboard（subprocess 包 eval.cli/setup.sh）→ 验证：curl 各端点通（10 份归档 / health ready / SPA 200）✓

## 1. 接入段（Tier 2）

- [x] 1.1 Setup 视图：依赖体检表（读 /api/health，cmm/graphify/codegraph/mempalace/python/render/creds ✓版本/✗缺）+ 健康门禁 + 依赖坑提示 → 验证：live 渲染真实 health ✓
- [x] 1.2 Project onboarding 5 步向导 UI：连代码库→索引(codegraph init)/文档图(graphify build,成本警示)/会话(mine,hook警示)/gold→就绪，每步 POST /api/onboard 实跑 → 验证：live 渲染 + 端点通 ✓
- [x] 1.3 向导状态持久化（localStorage）— Playwright 验证：输路径 → 离开页面 → 折回，自动回填 ✓

## 2. Tier 1 读视图（静态 SPA · 评测段）✓

- [x] 2.1 脚手架：vanilla JS SPA（web/index.html + app.css + app.js），Measurement Lab design tokens（奶油底 / Fraunces+JetBrains Mono / 烟花橙）抽自 mockup → 验证：服务起、字体/色板与 mockup 一致 ✓
- [x] 2.2 数据层：fetch /api/reports（index.json）+ /api/report/<id> → 验证：Dashboard 渲染真实归档（非写死）✓
- [x] 2.3 Dashboard 页：4 hero 指标（代码 0.846/记忆 0.933/A/B 12.71×/答案 0.971）+ 最近 run 列表 → 验证：live 读真实归档 ✓
- [x] 2.4 Reports archive 页：全量归档表 + 点行进 detail ✓
- [x] 2.5 Report detail 页：aggregate + per_query + lockfile + LLM-judged 徽标 ✓
- [x] 2.6 Compare 页：两 id aggregate diff 表 ✓
- [x] 2.7 启动：`python -m eval.cli web`（bench web 子命令）→ localhost:8765 ✓（静态托管 = 直接 open web/index.html 或起 server）

## 3. Tier 2 评测交互（薄后端）

- [x] 3.1 Run console 页 UI：subject/target/method 选 → POST /api/run → 显示 stdout → 验证 ✓
- [x] 3.2 Gold lab 页 UI：seed+target → ①挖+拟题(POST /api/goldgen) → ②实证验收(/api/goldgen-verify) → ③看候选人审(GET /api/pending) → ④fold(POST /api/goldgen-fold) → 验证：live 渲染 + 端点全通 ✓

## 4. 文档 + 收尾

- [x] 4.1 README/runbook 加"前端"段（bench web 起服务）
- [x] 4.2 mockup 与实装一致（Dashboard 实装对照 docs/mockup/dashboard.html，live 截屏 docs/mockup/live-dashboard.png）✓
- [x] 4.3 提交 + push ✓

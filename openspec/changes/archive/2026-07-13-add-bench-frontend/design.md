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

## 信息架构 · 8 个视图

接入门户分两段：**①接入（环境+目标工程）→ ②评测（跑+看+比）**。新人从①走完到②。

| 段 | 视图 | 对应 CLI / 脚本 | 做什么 | 层 |
|---|---|---|---|---|
| 接入 | **Setup · 环境依赖** | `setup.sh`（python/tools/render/creds）| 4 工具 + Python 依赖 + 渲染器 + 凭据：逐项状态（✓装/版本 · ✗缺）+ 一键装 + 健康检查 | Tier2 |
| 接入 | **Project · 目标工程接入** | cmm/codegraph index + graphify build + mempalace mine + goldgen | 向导：连代码库→索引→(文档图)→(会话 mine)→生成 gold→就绪 | Tier2 |
| 评测 | **Dashboard**（首屏）| list-reports 聚合 | 4 hero 指标 + 价值定位 §7 网格 + A/B 四臂条形 + 最近 run | Tier1 |
| 评测 | **Run console** | `bench run <subject>` | 选 subject+参数→触发→SSE 进度→结果摘要 | Tier2 |
| 评测 | **Reports archive** | `list-reports` / `show` | 时间线/表 + subject 过滤 + 点进 detail | Tier1 |
| 评测 | **Compare** | `compare <id1> <id2>` | aggregate diff 表 + A/B 多臂横评条形 | Tier1 |
| 评测 | **Gold lab** | `goldgen` / `-verify` / `-fold` | 扩题 4 阶段：seed→候选（双 verdict 徽标）→approve/edit→fold | Tier2 |
| 评测 | **Report detail** | `show <id>` | aggregate + per_query + lockfile + 边界标注 | Tier1 |

## 接入段 · 两视图设计

### Setup · 环境依赖（向导式）
- **依赖体检表**：cmm / graphify / codegraph / mempalace / Python(python+anthropic) / 渲染器 / LLM 凭据——每行 `✓ 装了 v…` 或 `✗ 缺`，含版本探测（复用 setup.sh 的探测逻辑）。
- **一键装**：缺的项逐个或"全装"——后端 `subprocess setup.sh <step>`，SSE 流安装日志。
- **健康检查**：跑 `pytest eval/tests/ -q`（零依赖应全绿）+ 各工具冒烟（cmm list_projects / graphify --version）→ 顶端绿灯"环境就绪"才放行进评测段。
- 诚实：依赖坑（numpy<2 / mempalace py3.11 / ragas 库冲突）在项内折叠提示，不藏。

### Project · 目标工程接入（5 步向导）
1. **连代码库**：填路径 → `cmm index <path>` + `codegraph init <path>`（进度条，静态零 LLM）。
2. **（可选）连文档**：填文档目录 → `graphify` 建图（⚠️ 标 LLM 成本预估，确认才跑）。
3. **（可选）连会话**：填 `~/.claude/projects/<proj>` → `mempalace mine --mode convos`（带"别配 auto-save hook"警示，链 D.4 事故）。
4. **生成 gold**：goldgen（seed 输入 → 两层验收 → 人审 → fold）——复用 Gold lab 视图。
5. **就绪**：显示"可 bench run 的 target 列表"→ 一键进 Run console 跑自己的系统。
- 每步可单独跳过/重跑；向导状态持久化（接了一半下次接着来）。



## 技术栈 · 分层（降门槛优先）

| 层 | 栈 | 能做 | 门槛 |
|---|---|---|---|
| **Tier 1 读视图**（必做）| Vite + React（或 vanilla SPA）+ 手写 SVG 图 | 读 `archive/*.json` + `index.json` → Dashboard/Reports/Compare/Detail。纯静态，浏览器开 | **最低**（`open index.html` 或静态托管）|
| **Tier 2 交互**（可选）| + 薄 Flask/FastAPI（`POST /api/run`、`/api/goldgen`、`/api/compare` 子进程包 `eval.cli`，SSE 流式进度）| Run console + Gold lab 全交互（点按钮触发评测/goldgen）| 中（跑个 `flask run`）|

**图表**：手写 SVG 条形/点阵（mockup 已示，on-brand），重交互才上 visx/Recharts。
**不引**重型 UI 框架（MUI/AntD 之类）——与"仪器/编辑"美学冲突。

## 数据流（前端不造数；接入段执行命令）

```
Tier1（读）:    前端 ──fetch──▶ eval/reports/archive/*.json + index.json（统一 schema）
Tier2（评测）:  前端 ──HTTP──▶ Flask wrapper ──subprocess──▶ python -m eval.cli ...
                                 └─ SSE 流 stdout 进度 ──▶ 前端
Tier2（接入）:  前端 ──HTTP──▶ Flask wrapper ──subprocess──▶ setup.sh / cmm index / codegraph init
                                                         / graphify build / mempalace mine / goldgen
                                 └─ 探测状态（which/version）+ SSE 流执行日志 ──▶ 前端
```
归档 JSON 仍是评测唯一事实源；接入段执行 setup.sh / 索引 / mine（不改评测契约）。
LLM-judged 分等边界仍随分数显示（诚实不藏）。

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

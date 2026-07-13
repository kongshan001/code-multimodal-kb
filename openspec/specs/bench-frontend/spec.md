# bench-frontend Specification

## Purpose

benchmark 的可视化层（Measurement Lab）：把 CLI 的每一句对应到一个浏览器页面——读归档报告（Dashboard / Reports / Detail / Compare）、依赖体检与一键装、目标工程接入向导、交互式跑评测与扩题编辑器。零额外依赖（stdlib http.server + vanilla JS SPA），只读视图不依赖后端，交互视图经薄后端 subprocess 调 `eval.cli`。

## Requirements
### Requirement: Environment dependency management

当系统提供 Tier 2 后端时，前端 SHALL 显示依赖体检（cmm/graphify/codegraph/mempalace/Python/渲染器/LLM 凭据，逐项 ✓版本/✗缺）并支持一键安装（subprocess 调 `setup.sh`）+ 健康检查（pytest 冒烟 + 各工具版本探测）；环境未就绪时 SHALL 提示、不阻断只读评测视图。

#### Scenario: 依赖体检 + 一键装

- **WHEN** 用户进 Setup 视图
- **THEN** 看到逐项依赖状态；点"装缺的"→ 后端 SHALL 跑 `setup.sh <step>`，SSE 流日志，装完刷新状态

#### Scenario: 健康门禁

- **WHEN** 关键依赖缺失
- **THEN** 顶端 SHALL 标"环境未就绪"，但只读评测视图（Tier1）仍可用

### Requirement: Target project onboarding wizard

当系统提供 Tier 2 后端时，前端 SHALL 提供 5 步向导把用户的目标工程接入可 bench 状态：连代码库→索引（cmm+codegraph）→(可选 文档图 graphify)→(可选 会话 mempalace mine)→生成 gold（复用 Gold lab）→就绪；每步 SHALL 显示进度、可跳过/重跑，向导状态持久化。

#### Scenario: 索引目标代码库

- **WHEN** 用户填代码库路径并确认
- **THEN** 后端 SHALL 跑 `cmm index` + `codegraph init`（静态零 LLM，进度条）；完成进入下一步

#### Scenario: 文档图成本警示

- **WHEN** 向导到可选的文档图步骤（graphify，花 LLM）
- **THEN** SHALL 先显示成本预估，用户确认才执行

#### Scenario: auto-save hook 警示

- **WHEN** 向导到会话 mine 步骤
- **THEN** SHALL 提示"勿配非 idempotent 的 auto-save hook"（链 deployment-runbook §D.4 事故），引导手动 `mempalace sweep`

### Requirement: Benchmark visualization layer (read-only)

系统 SHALL 提供一个静态前端，读取 `eval/reports/archive/*.json` + `index.json`（统一 schema），把 bench CLI 的归档结果可视化（Dashboard / Reports archive / Compare / Report detail），使非 CLI 用户能浏览评测结果，无需运行命令。

#### Scenario: 浏览器打开即看 Dashboard

- **WHEN** 用户在浏览器打开前端（静态托管或本地 file/简单 HTTP）
- **THEN** 看到 hero 指标（最近一次各 subject 主分数）+ 价值定位 §7 网格 + 最近 run 列表，全部来自归档 JSON

#### Scenario: 边界随分数一起显示

- **WHEN** 展示任一 LLM-judged 指标（faithfulness 等）
- **THEN** 该分数旁 SHALL 标注 `LLM-judged / self-preference` 徽标（前端不藏诚实边界）

### Requirement: Compare view

系统 SHALL 可视化 `bench compare` 的两份报告 aggregate diff，并在 A/B 多臂场景显示各臂准确度/token/步数对照条形。

#### Scenario: 两臂对比

- **WHEN** 用户选两份归档报告
- **THEN** 显示 metric × {left, right, delta} 表 +（若是 A/B 报告）多臂条形横评

### Requirement: Interactive run/goldgen (Tier 2, optional)

当系统提供 Tier 2 薄后端（Flask/FastAPI 包装 `eval.cli`）时，它 SHALL 使前端能触发 `bench run` / `goldgen` / `goldgen-verify` / `goldgen-fold` 并流式显示进度；Gold lab SHALL 把扩题两层验收 + 人审做成 UI。Tier 2 为可选（不提供时降级为 Tier 1 只读 + CLI 触发）。

#### Scenario: UI 触发评测

- **WHEN** 用户在 Run console 选 subject + 参数并点"跑"（Tier 2 后端已提供）
- **THEN** 后端 SHALL 子进程调 `python -m eval.cli run <subject> ...`，SSE 流 stdout 进度，完成后归档并刷新 Dashboard

#### Scenario: Gold lab 两层验收可视化

- **WHEN** goldgen 产出候选（Tier 2）
- **THEN** 前端 SHALL 每条 candidate 显示实证 verdict + subagent verdict 双徽标，用户逐条 approve/edit，确认后触发 fold


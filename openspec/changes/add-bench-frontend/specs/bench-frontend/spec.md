## ADDED Requirements

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

系统 MAY 提供薄后端（Flask/FastAPI）包装 `eval.cli`，使前端能触发 `bench run` / `goldgen` / `goldgen-verify` / `goldgen-fold` 并流式显示进度；Gold lab 把扩题两层验收 + 人审做成 UI。

#### Scenario: UI 触发评测

- **WHEN** 用户在 Run console 选 subject + 参数并点"跑"
- **THEN** 后端 SHALL 子进程调 `python -m eval.cli run <subject> ...`，SSE 流 stdout 进度，完成后归档并刷新 Dashboard

#### Scenario: Gold lab 两层验收可视化

- **WHEN** goldgen 产出候选
- **THEN** 前端 SHALL 每条 candidate 显示实证 verdict + subagent verdict 双徽标，用户逐条 approve/edit，确认后触发 fold

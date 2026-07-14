# benchmark-runner Specification

## Purpose

统一 benchmark 运行器：一个 `bench` CLI（子命令式）替代散装 `run_*` 脚本，每次评测自动归档（不覆盖）+ 结构化报告 schema + 可复现 lockfile + pytest 三层测试 + gold 回归门禁。使评测可脚本化、可管道、跨设备/跨时间可比，并为前端（bench-frontend）预留统一入口。
## Requirements
### Requirement: Unified benchmark CLI

系统 SHALL 提供统一 `bench` CLI（子命令式），替代散装 `python -m eval.run_*`，支持 `run code|doc|cross|quality`、`list-reports`、`show <id>`、`compare <id1> <id2>`；子命令可脚本化、可管道，使前端（后续 change）可复用同一入口。

#### Scenario: 子命令跑评测并归档

- **WHEN** 执行 `bench run code --target godot --method bm25`
- **THEN** 评测执行、结果以结构化 JSON 归档至 `eval/reports/archive/`、stdout 打印归档路径与 aggregate 摘要

#### Scenario: 列出历史报告

- **WHEN** 执行 `bench list-reports`
- **THEN** 输出 `archive/index.json` 中所有报告的 id / ts / subject / variant / aggregate 摘要

#### Scenario: 查看与对比报告

- **WHEN** 执行 `bench show <id>` 或 `bench compare <id1> <id2>`
- **THEN** 分别输出单份报告详情、或两份报告的 aggregate 差异

### Requirement: Report archival and provenance

系统 SHALL 在每次评测运行后自动将报告归档至 `eval/reports/archive/<ts>-<subject>-<variant>.json`，不覆盖既有文件，并更新 `archive/index.json` 清单，使每次报告生成均有留底、可追溯。

#### Scenario: 重跑不覆盖

- **WHEN** 对同一 subject + variant 连续运行两次评测
- **THEN** 生成两个不同 ts 的归档文件，`index.json` 含两条记录，既有文件不被覆盖

#### Scenario: 归档含 lockfile 与摘要

- **WHEN** 报告归档
- **THEN** 归档 JSON 含 lockfile（temp / 模型 / 工具版本）与 aggregate 摘要；`index.json` 条目含同样的 lockfile 摘要，支撑横向对比与可复现性核查

### Requirement: Structured report schema

系统 SHALL 产出统一结构的报告 JSON（`subject / target / n / aggregate / per_query / lockfile / archive_meta`），使报告可被程序化消费，为前端预留。

#### Scenario: 报告 schema 跨 subject 一致

- **WHEN** 任一 subject（code / doc / cross / quality）运行并归档
- **THEN** 归档 JSON 含统一顶层字段；`aggregate` 与 `per_query` 按 subject 语义填充，但顶层结构相同

### Requirement: Benchmark documentation

系统 SHALL 提供完整 benchmark 使用文档（runbook），覆盖安装、运行、读报告、复现、归档查询，使新成员能独立复现一次评测。

#### Scenario: 新人照文档复现

- **WHEN** 新成员照 `docs/benchmark-runbook.md` 操作
- **THEN** 能独立跑一次代码侧评测、定位归档报告、解释 aggregate 指标含义

### Requirement: Test fixation

系统 SHALL 用 pytest 固化三层测试——纯函数指标、端到端 smoke（mock subject，零外部依赖）、留底机制（归档不覆盖 + index 更新）——并加 gold 集回归门禁防漂移。

#### Scenario: 端到端 smoke 零外部依赖

- **WHEN** 在无 cmm / graphify / Godot 的环境跑 `pytest eval/tests/`
- **THEN** 端到端 smoke 用 mock subject 通过，断言 aggregate 落在预期区间且归档文件生成

#### Scenario: 留底机制测试

- **WHEN** 测试中连续跑两次同一评测
- **THEN** 断言产生两个归档文件、`index.json` 新增两条、既有文件不覆盖

#### Scenario: gold 回归门禁

- **WHEN** `gold_*.py` 的 GOLD 集被改动
- **THEN** 快照测试检测到长度 / 首条变化并失败，防止 gold 意外漂移

### Requirement: Frontend readiness boundary

系统 SHALL 保持核心逻辑为可导入纯函数 + 报告为结构化 JSON，为前端预留；但 SHALL NOT 在本变更引入前端 UI 或 HTTP API。

#### Scenario: 前端可消费归档

- **WHEN** 前端（后续 change）读取 `archive/index.json` 与归档 JSON
- **THEN** 结构化字段可直接消费，无需解析 stdout 文本

#### Scenario: 本变更不引入 HTTP

- **WHEN** 本变更实施完成
- **THEN** 不新增任何 HTTP 服务 / 端点（前端 UI / API 为后续 change）

### Requirement: agent-compare run subcommand

统一 bench CLI SHALL 提供 `bench run agent-compare --target <id>` 子命令：对该 target 的题目（code_retrieval + bug_fix）跑多臂（no-kb / kb / kb+superpowers / kb+openspec）agent episode，捕获 trace + 指标，产出目录化对比报告（`eval/reports/agent-compare/<ts>-<target>/`，含 conclusion/summary/matrix/arms）。子命令 SHALL 支持 `--arms`（默认 4 臂全跑，可指定子集）、`--runs`（每题重复次数，控成本）、`--subset`（只跑前 N 题 pilot）、`--smoke`（无凭据 mock 模式）。每次跑 SHALL 入库结论类、gitignore 会话/思考类。

#### Scenario: 跑 4 臂出目录报告

- **WHEN** 执行 `bench run agent-compare --target <id>`
- **THEN** SHALL 跑 4 臂 agent episode，在 `eval/reports/agent-compare/<ts>-<id>/` 下产出 conclusion.md + summary.json + matrix.md + arms/<arm>/{config,aggregate,episodes}

#### Scenario: smoke 模式无凭据跑通

- **WHEN** 执行 `bench run agent-compare --target <id> --smoke` 且无 LLM 凭据
- **THEN** SHALL 用 mock LLM 跑通流水线，产出结构完整的目录报告，不报错


## ADDED Requirements

### Requirement: agent-compare run subcommand

统一 bench CLI SHALL 提供 `bench run agent-compare --target <id>` 子命令：对该 target 的题目（code_retrieval + bug_fix）跑多臂（no-kb / kb / kb+superpowers / kb+openspec）agent episode，捕获 trace + 指标，产出目录化对比报告（`eval/reports/agent-compare/<ts>-<target>/`，含 conclusion/summary/matrix/arms）。子命令 SHALL 支持 `--arms`（默认 4 臂全跑，可指定子集）、`--runs`（每题重复次数，控成本）、`--subset`（只跑前 N 题 pilot）、`--smoke`（无凭据 mock 模式）。每次跑 SHALL 入库结论类、gitignore 会话/思考类。

#### Scenario: 跑 4 臂出目录报告

- **WHEN** 执行 `bench run agent-compare --target <id>`
- **THEN** SHALL 跑 4 臂 agent episode，在 `eval/reports/agent-compare/<ts>-<id>/` 下产出 conclusion.md + summary.json + matrix.md + arms/<arm>/{config,aggregate,episodes}

#### Scenario: smoke 模式无凭据跑通

- **WHEN** 执行 `bench run agent-compare --target <id> --smoke` 且无 LLM 凭据
- **THEN** SHALL 用 mock LLM 跑通流水线，产出结构完整的目录报告，不报错

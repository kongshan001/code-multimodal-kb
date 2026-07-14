## Why

现有 `ab-agent` benchmark 只测"有 KB vs 无 KB"在**代码检索**（find symbol）上的准确率/token——回答不了用户的核心问题：**软件开发 skills（superpowers / openspec）到底给 agent 带来多少价值？** 而且只输出单 JSON，看不到 agent 的**执行过程与思考**。本变更把 agent 对比扩成 4 臂（KB × skills）、加 token/调用次数/耗时/成本/准确率多维指标、并产出**目录化报告**（结论 + 每臂执行过程 + 会话 + 思考），让"skills 值不值"有据可查。

## What Changes

- **4 臂 agent 对比**：`no-kb` / `kb` / `kb+superpowers` / `kb+openspec`。臂 = 工具集 + skills 注入；skills 臂把精简 SOP 文本 prepend 进 system prompt。
- **ab_agent.run_episode 改造**：捕 `llm_calls` / `wall_clock_s` / `cost_$` / 完整 `session` 消息流 / `thinking`（模型无关：有 thinking block 抽 block，无则 fallback reasoning 文本）；去 SYS_PROMPT 的 Godot 硬编码（改目标感知）；skills 臂 `max_steps` 放宽到 10。
- **新增 `bug_fix` 题型**：query=bug 复现，gold={symbols,files}，复用 broad match 判分。给 skills 臂发挥空间（纯检索上 skills 无价值）——每目标 curate 5-8 道。
- **目录化对比报告**（新写器 `eval/agent_compare_report.py`）：`conclusion.md` / `summary.json`（臂×指标矩阵）/ `matrix.md` / `arms/<arm>/{config.md, aggregate.json, episodes/qNN/{episode.json, session.jsonl, thinking.md}}`。结论类入库，`session.jsonl`+`thinking.md` 本地 gitignore（防膨胀）。
- **指标集**：accuracy / input·output·total_tokens / llm_calls / tool_steps / wall_clock_s / cost_$ / context_compression / tool_diversity。
- **bench CLI**：加 `bench run agent-compare --target <id>` 子命令。
- **`bench-author-problems` skill**（`.claude/skills/`）：顶上编排"给目标工程 → goldgen 设计 code_retrieval 题 → 手动 curate bug_fix 题 → AI 审（实证 + 独立 subagent 语义审）→ 人工 approve 入库 → 4 臂对比跑 → 目录报告"。
- **BREAKING**：`ab_tools.ARMS` 从 `dict[str, list[str]]` 升级为 `dict[str, {tools, skills}]`（旧臂名 `baseline`/`kb`/`doc`/`codegraph` 的调用方需适配；保留兼容映射或迁移）。

## Capabilities

### New Capabilities

- `benchmark-agent-compare`: 多臂 agent 对比 benchmark——4 臂（KB × skills）配置、episode trace 捕获（session/thinking/llm_calls/wall_clock/cost）、目录化对比报告（结论+执行过程+会话+思考）、多维指标矩阵、诚实边界标注、无凭据 mock 降级。

### Modified Capabilities

- `benchmark-targets`: 新增 `bug_fix` problem type（gold={symbols,files}，扩展题库 schema 到 6 型），为 agent-compare 提供 skills-可发挥的任务。
- `benchmark-runner`: bench CLI 加 `run agent-compare` 子命令（多臂对比 + 目录报告）。

## Impact

- **改**：`eval/ab_agent.py`（run_episode 6 项改造 + 去 Godot）、`eval/ab_tools.py`（ARMS 升级 {tools,skills} + skill 内容加载）、`eval/run_ab_agent.py`（适配新臂 + 新指标 + 调报告写器）、`eval/targets.py`（bug_fix type schema 校验）、`eval/cli.py`（agent-compare 子命令）、`eval/server.py`（若前端触发）。
- **新增**：`eval/arms/skills_bundled/{superpowers,openspec}.md`（精简 SOP）、`eval/agent_compare_report.py`（目录写器）、`eval/reports/agent-compare/`（报告目录，gitignore session/thinking）。
- **依赖**：零新增（复用 anthropic SDK + stdlib）。本机无 anthropic → mock 降级跑通写器/流水线。
- **skill**：`.claude/skills/bench-author-problems/SKILL.md`。
- **文档**：`docs/benchmark-runbook.md`（agent-compare 段）、`docs/frontend-guide.md`（若前端展示）。
- **诚实边界**：bundled skill 是精简 SOP 文本（非完整 skill 运行时触发机制）；accuracy 由 GLM 判分（同家族 self-preference）；`cost_$` 依赖 GLM 单价（未知则 null）。

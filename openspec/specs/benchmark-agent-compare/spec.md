# benchmark-agent-compare Specification

## Purpose

多臂 agent 对比 benchmark：把"有/无 KB"和"有/无 软件开发 skills（superpowers/openspec）"对 agent 任务表现的影响量化成可对比的指标矩阵（准确率 / token / LLM 调用次数 / 耗时 / 成本 / 工具多样性），并产出含结论 + 每臂执行过程 + 会话流 + 思考过程的目录化报告，使"KB 与 skills 的工程价值"有据可查、可审计。
## Requirements
### Requirement: Multi-arm agent comparison

系统 SHALL 支持多臂 agent 对比，臂 = 工具集 + skills 注入的组合。SHALL 至少提供 4 臂：`no-kb`（grep+read，无 KB 无 skill）/ `kb`（cmm+read，有 KB 无 skill）/ `kb+superpowers`（cmm+read + superpowers SOP）/ `kb+openspec`（cmm+read + openspec SOP）。臂定义 SHALL 以 `{tools: [...], skills: [...]}` 结构声明（不再仅是工具名列表）。skills 臂 SHALL 把对应 skill 的精简 SOP 文本 prepend 进该臂 agent 的 system prompt；SOP 文本 SHALL 从仓库内 bundle（`eval/arms/skills_bundled/`）读取，不依赖宿主 `~/.claude/skills`。skills 臂的 `max_steps` SHALL 放宽到 10（SOP 更费步），非 skills 臂保持 6。

#### Scenario: 4 臂配置可声明

- **WHEN** 查阅臂注册表
- **THEN** SHALL 见 4 臂 `no-kb` / `kb` / `kb+superpowers` / `kb+openspec`，每臂含 `tools` 与 `skills` 字段

#### Scenario: skills 臂注入 SOP

- **WHEN** 跑 `kb+superpowers` 臂的 episode
- **THEN** 该臂 agent 的 system prompt SHALL 含 superpowers SOP 文本（来自仓库 bundle），且 max_steps=10

### Requirement: Agent episode trace capture

每个 episode SHALL 捕获完整执行 trace：`llm_calls`（LLM 调用轮数，显式）、`tool_steps`（工具调用次数）、`input_tokens`/`output_tokens`/`total_tokens`、`wall_clock_s`（端到端耗时）、`cost_$`（token×单价，单价未知则 null）、`session`（逐轮消息流：role + 序列化的 text/tool_use/tool_result 内容）、`thinking`（模型无关：有 thinking block 抽 block，无则 fallback 该轮 assistant reasoning 文本）、`truncated`（max_steps/max_turns 耗尽未自然收敛）。`session` 中的 tool_result 内容 SHALL 截断至限长（防膨胀）。

**运行时无关**：上述 trace 契约 SHALL 与底层 agent 运行时实现无关——无论 episode 由手写 ReAct loop（直连 `anthropic` SDK 最小调用）还是 `claude_agent_sdk`（`claude` CLI 封装）驱动，同一 episode 产出的 trace 字段名、类型、语义 SHALL 逐一对齐。底层运行时的替换（如本次 SDK 迁移）SHALL NOT 改变可观测契约，使迁移成为纯实现重构、不破坏与历史报告的可比性。

#### Scenario: 捕获 llm_calls 与 tool_steps 分开

- **WHEN** 一个 episode 跑了 3 轮 LLM、共触发 5 次工具
- **THEN** 输出 SHALL 含 `llm_calls=3`、`tool_steps=5`（二者独立）

#### Scenario: thinking 模型无关捕获

- **WHEN** 模型返回 thinking block
- **THEN** SHALL 抽进 `thinking`
- **WHEN ELSE**（无 thinking block）THEN SHALL 用该轮 assistant text 作 fallback，`thinking` 非空

#### Scenario: cost 未知降级

- **WHEN** MODEL_PRICES 无当前模型单价
- **THEN** `cost_$` SHALL 为 null（不报错），并在报告标注

#### Scenario: trace 契约运行时无关（迁移等价）

- **WHEN** 同一（固定 seed / mock）episode 分别由手写 loop 与 `claude_agent_sdk` 驱动
- **THEN** 二者产出的 trace dict SHALL 含相同 key 集合，且 `truncated` / `tool_steps` 语义一致；token 与 wall_clock 允许随运行时浮动，但字段 SHALL 存在且类型不变

### Requirement: Directory-structured comparison report

系统 SHALL 把多臂对比结果写成目录结构：`<report-root>/result.md`（人读：结论 + 指标小白说明 + 对比矩阵 + 逐题得分对照 + 诚实边界，全合一）+ `summary.json`（臂×指标矩阵，程序消费用）+ `arms/<arm>/config.md`（该臂工具+skill 透明可审计）+ `arms/<arm>/aggregate.json`（该臂指标聚合）+ `arms/<arm>/episodes/qNN/episode.json`（单题：query+gold+answer+correct+逐步 tool+指标）+ 同目录 `session.jsonl`（完整消息流）+ `thinking.md`（思考）。`result.md` / `summary.json` / `arms/<arm>/{config.md,aggregate.json,episodes/qNN/episode.json}` SHALL 入库；`session.jsonl` 与 `thinking.md` SHALL 经 gitignore 不入库。系统 SHALL NOT 自动 git commit 报告。结论、矩阵、逐题对照 SHALL 合并进单个 `result.md`（不再拆 conclusion.md / matrix.md / questions.md）。

#### Scenario: 结论类入库、会话类本地

- **WHEN** 一次 agent-compare 跑完
- **THEN** `result.md`/`summary.json`/`arms/<arm>/aggregate.json`/`arms/<arm>/episodes/*/episode.json` SHALL 入库；同 episode 的 `session.jsonl`+`thinking.md` SHALL 被 .gitignore 忽略

#### Scenario: result 人读（含逐题对照）

- **WHEN** 打开 result.md
- **THEN** SHALL 见哪臂赢、by 哪个指标、各指标的大白话说明、对比矩阵、逐题得分对照（每题 qNN 一段含 臂×{答对/答案/tokens/llm_calls/耗时/截断} 表）、诚实边界标注（LLM-judged / self-preference / bundled-SOP-not-runtime）

### Requirement: Comparison metrics matrix

每臂 SHALL 产出完整指标集：`accuracy` / `input_tokens` / `output_tokens` / `total_tokens` / `llm_calls` / `tool_steps` / `wall_clock_s` / `cost_$` / `context_compression`（有 KB vs 无 KB 的注入 token 比）/ `tool_diversity`（distinct 工具数）。`summary.json` SHALL 是臂×指标的对比矩阵；`result.md` SHALL 含该矩阵的人读版 + 每个指标的小白说明。

#### Scenario: summary 是臂×指标矩阵

- **WHEN** 跑完 4 臂
- **THEN** `summary.json` SHALL 含每臂的全指标行，字段集一致，可程序化对比

### Requirement: Honest comparison boundaries

`result.md` 与每臂 `config.md` SHALL 明确标注：（a）skills 臂注入的是**精简 SOP 文本**，非完整 Claude Code skill 运行时触发机制——是 headless 可复现近似，非真实 skill 效果；（b）`accuracy` 由 GLM 生成 + GLM 判分（同家族 self-preference），是相对参考值非绝对回归值；（c）`cost_$` 依赖模型单价，可能为 null；（d）样本量（题数×runs）影响显著性，小样本结论须标注。

#### Scenario: 结论不藏诚实边界

- **WHEN** 展示任一指标结论
- **THEN** result.md SHALL 在该结论旁标注适用边界（至少 LLM-judged / SOP-not-runtime 之一）

### Requirement: Low-credential degradation

系统 SHALL 在无 LLM 凭据（无 anthropic SDK 或无 GLM key）时以 mock LLM 跑通报告写器与对比流水线（smoke），产出结构完整（含 4 臂目录、summary 矩阵、conclusion）的示例报告——使本机无凭据也能验证流水线正确性。真 episode SHALL 待凭据就绪后跑。

#### Scenario: 无凭据 mock 跑通写器

- **WHEN** 无 AB_API_KEY 且无 ~/.cc-connect/config.toml，跑 agent-compare 的 smoke 模式
- **THEN** SHALL 用 mock LLM 产出 4 臂完整目录报告（结构正确），不因缺凭据报错


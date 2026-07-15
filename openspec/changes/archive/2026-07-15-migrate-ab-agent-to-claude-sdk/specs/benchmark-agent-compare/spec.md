## MODIFIED Requirements

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

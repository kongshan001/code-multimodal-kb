## Context

`eval/ab_agent.py` 的 `run_episode` 是 benchmark 唯一直接打 LLM 协议的代码：手写 ReAct loop + 429/5xx 退避（`_create_with_retry`）+ tool_use 循环 + max_steps 耗尽 force-answer 兜底 + 模型无关序列化（`_serialize_turn`），约 80 行，全部依赖 `anthropic.Anthropic.messages.create` 的最小调用形态。BigModel 的 anthropic 兼容端点偏离真 Anthropic 的每一处（thinking block / stop_reason / tool_use 边界 / usage 字段）都靠这些手写 fallback 兜，格式脆弱性与维护成本集中于此。

`claude_agent_sdk`（Python）是 `claude` CLI 的官方薄封装——spawn `claude` 子进程经 stdio 通信，loop / 重试 / tool_use 往返 / 序列化全在 SDK 内。spike（2026-07-15）已实锤完整 CLI 打 BigModel 端点返回 `PONG`，tool_use 端点已支持。本设计把 ab_agent 从"手写 loop + 最小 SDK 调用"迁到"SDK query() 消费消息流"，**trace 契约逐字段不变**（见 specs delta）。

约束：对外 `run_episode` 同步签名不动（`run_compare`/`run` 是同步循环）；凭据优先级（env > bench.local.yaml > config.toml）不动；4 臂语义 + target 注入不动；判分 / 报告写器 / `bench` CLI 不动。

## Goals / Non-Goals

**Goals:**
- 删除手写 agent loop（`_create_with_retry` / 循环体 / force-answer / `_serialize_turn`），把 LLM 协议敏感度转移给官方 SDK。
- trace 字段 100% 向后兼容——迁移前后同一 episode 的 trace dict key 集合 / 类型 / 语义对齐。
- 工具层零语义改动：executor + `set_active` target 注入原样保留，仅注册方式从 schema-dict 改 `@tool`。
- `run_episode` 对外同步签名不变，调用点零改。

**Non-Goals:**
- 不改判分（`_judge`/`_judge_retrieval`）、报告目录 / 写器、`bench` CLI、goldgen、smoke `_mock_episode`。
- 不动 `eval/llm.py` 的 judge 路径（OpenAI 兼容，走 urllib，独立）。
- 不把整条调用栈改 async（仅 `run_episode` 内部 `anyio.run` 包）。
- 不改臂定义 / target 配置 schema。

## Decisions

### D1. 凭据与端点：经 `ClaudeAgentOptions.env` 透传，不写 `~/.claude/settings.json`
SDK spawn `claude` 子进程，自定义端点经 `env={"ANTHROPIC_BASE_URL": ..., "ANTHROPIC_API_KEY": ...}` + `model=...` 注入子进程（spike 已用 `ANTHROPIC_API_KEY` + `ANTHROPIC_BASE_URL` 跑通 PONG；与现有 `make_client` 的 `anthropic.Anthropic(api_key=)` 同走 `x-api-key`）。
- **弃用方案**：写 `~/.claude/settings.json` 的 provider——拒绝：机器全局、污染用户 CLI 配置、bench 凭据不该落宿主全局。
- `load_creds` 优先级链保留；`make_client` 删除（不再构造 `anthropic.Anthropic`）。

### D2. 自定义工具：`@tool` + in-process MCP，保留 executor 与 `set_active`
每个 ab_tool（`grep_code`/`cmm_search`/`read_file`/`codegraph_search`/`graphify_query`）包成 `@tool`，`create_sdk_mcp_server("bench", tools=[...])` 挂进 `mcp_servers`。工具名 `grep_code` → `mcp__bench__grep_code`（仅 `ARMS` 数据里的引用名改）。executor 函数体不动 → `set_active` 注入的 `_active` 仍生效（工具在**进程内**执行，`_active` 是模块级 dict）。
- **弃用方案**：映射到 CLI 内建 `Grep`/`Read` + 外部 MCP server 提供 cmm——拒绝：丢失 target 注入隔离（CLI 内建工具不知当前 target）、要重实现工具语义、破坏臂公平性控制（read_cap / tool_result_cap 截断）。

### D3. sync 包 async：`run_episode` 内部 `anyio.run`，对外签名不变
`query()` 是 async 迭代器；`run_episode` 内部 `anyio.run(_run_episode_async, ...)` 包裹，对外仍是 `def run_episode(...) -> dict`。`run_compare`/`run` 是同步循环，零改。
- **弃用方案**：整栈 async——拒绝：级联改 `run_compare`/`run`/`bench` CLI，无收益。

### D4. force-answer / truncated 保真：max_turns 耗尽后追加一次 `tools=[]` query
SDK 的 `max_turns` 到顶后停止；为保现有契约（非空答案 + `truncated=True`），耗尽时追加一次 `allowed_tools=[]`（或无 mcp_servers）的 `query()` 强制作答，复刻现有 force-answer 语义。
- **弃用方案**：依赖 SDK 自带的"末轮给文本"——拒绝：可能返空 / partial，破坏"答案非空"契约。

### D5. trace 字段映射（消息流 → 现 trace dict）

| trace 字段 | 来源（SDK 消息流） |
|---|---|
| `llm_calls` | AssistantMessage 计数（或 ResultMessage.num_turns） |
| `tool_steps` | ToolUseBlock 计数 |
| `tool_calls` / `tool_texts` | 逐 ToolUseBlock 的 name / exec 结果 |
| `input_tokens` / `output_tokens` / `total_tokens` | 累计各轮 AssistantMessage.usage；无则 ResultMessage.usage |
| `session` | 逐轮序列化：AssistantMessage(text/tool_use blocks) + tool_result（截断至 `tool_result_cap`） |
| `thinking` | thinking block；无则 fallback 该轮 text（模型无关） |
| `cost_$` | ResultMessage.total_cost_usd；无/0 则 token×`config.prices` fallback（保 cost 未知降级） |
| `truncated` | 是否走了 D4 force-answer |
| `wall_clock_s` | `run_episode` 入口 → 出口（含子进程启动，见 D6） |

### D6. 子进程开销与 wall_clock：保留端到端计时，不做剔除
每个 episode spawn 一个 `claude` 子进程，启动开销（~数百 ms）会进 `wall_clock_s`。但**所有臂都付同一恒定开销**，臂间相对比较不受影响；仅绝对 wall_clock 略增。
- 决定：`wall_clock_s` 保持端到端（诚实、且是用户感知的实际耗时），不引入 `llm_wall_clock` 拆分（避免无谓复杂度，违 KISS）。
- 若后续需要纯 LLM 计时，单列变更。

## Risks / Trade-offs

- **[CLI 自带 system prompt 改变 agent 行为 / accuracy 基线]** → `claude` CLI 注入比 `BASE_SYS_PROMPT` 大得多的默认 system prompt + 工具描述；即使 `system_prompt=` 覆盖，CLI 可能 prepend 自身指令，使 agent 答题行为偏离历史 run，accuracy 数字跨版本不可比。→ **缓解**：实现期 spike 验证 `system_prompt=` 是否**完全替换** CLI 默认（非 prepend）；若 prepend，需 `setting_sources`/`--append-system-prompt` 关闭默认，或接受"迁移后重立基线"。这是最大未定项，见 Open Questions。
- **[BigModel 端点对 CLI 重负载请求的兼容]** → CLI 请求体比最小 SDK 调用重（多特性），可能撞上端点未实现的字段。→ 缓解：spike 已通；消息流解析保留 getattr 防御；实现期用真 episode 端到端跑 `godot-core` subset 验。
- **[async / 事件流抽取比承诺费事]** → token/session 从消息流抽，非简单 `.usage`。→ 缓解：D5 映射表 + 单测（录一份 fixture 消息流，断言抽出的 trace 字段）。
- **[`anthropic` 移除是 BREAKING]** → 迁移后 ab_agent 不再 import；env 需重装。→ 缓解：改 `eval/requirements.txt` + `setup-bench.bat` 注明；移除前全仓 grep 确认无其他引用。
- **[子进程 spawn 开销 / 并发]** → `run_compare` 串行跑多题×多臂×runs，每 episode spawn 一次子进程，总耗时上升。→ 缓解：benchmark 本就串行（公平 / 限流），开销可接受；不改并发模型。

## Migration Plan

1. `pip install claude-agent-sdk anyio` 到 bench env；`eval/requirements.txt` 加这两项。
2. spike 验证 D1（env 透传）+ Open Question 1（system_prompt 覆盖语义）——决定是否需关 CLI 默认 prompt。
3. 改 `ab_tools.py`：executor 包 `@tool`，建 in-process MCP server；`ARMS` 工具名改 `mcp__bench__*`。
4. 改 `ab_agent.py`：`run_episode` 重写为 `anyio.run(_async)` + 消息流消费 + D5 映射 + D4 force-answer；删 `_create_with_retry`/`_serialize_turn`/`make_client`。
5. `godot-core` subset 端到端跑 4 臂，比对迁移前后 trace 字段 + accuracy 是否合理（D6/Open Q1 结论决定"合理"阈值）。
6. `eval/requirements.txt` 移除 `anthropic`（grep 确认无引用后）。
7. **回滚**：变更全在 `eval/ab_agent.py` + `ab_tools.py` + `requirements.txt`；git revert 单 commit 即回手写 loop（trace 契约不变 → 历史报告仍可比）。

## Open Questions

1. **`ClaudeAgentOptions(system_prompt=...)` 是完全替换 CLI 默认 system prompt，还是 prepend？** 决定 agent 行为是否偏离历史 baseline、accuracy 跨版本可比性。实现期 spike 验证；若 prepend 且无法关闭 → 接受"迁移后重立基线"并在 result.md 标注。
2. **`anthropic` SDK 迁移后是否全仓无其他 import？** 决定能否从 requirements 移除（grep 验证）。
3. **SDK 消息流是否稳定暴露每轮 usage（还是只在 ResultMessage 汇总）？** 影响 `llm_calls`/逐轮 token 粒度；若仅汇总，`session` 逐轮仍可序列化但逐轮 token 粒度降级（total 仍准）。

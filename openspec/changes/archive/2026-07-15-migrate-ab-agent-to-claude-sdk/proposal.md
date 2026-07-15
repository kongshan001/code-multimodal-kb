## Why

`eval/ab_agent.py` 手写了一套约 80 行 ReAct agent loop（`_create_with_retry` 退避 + `run_episode` 的 tool_use 循环 + max_steps 耗尽 force-answer 兜底 + `_serialize_turn` 模型无关序列化），直接依赖 `anthropic.Anthropic.messages.create` 的**最小调用**形态。这是 benchmark 唯一对 LLM 协议细节敏感的代码——BigModel 的 anthropic 兼容端点偏离真 Anthropic 的每一处（thinking block / stop_reason / tool_use 边界）都要靠手写 fallback 兜，维护负担与格式脆弱性都集中在此。

改用 `claude_agent_sdk`（`claude` CLI 的官方封装）后，loop / 重试 / tool_use 往返 / 序列化全交 SDK，ab_agent 只剩"组装 prompt + 工具 + 取 trace"——把对协议格式的敏感度从 benchmark 自有代码转移到官方 SDK。

**已验证可行性（spike，2026-07-15）**：完整 `claude` CLI（v2.1.195，非最小 SDK 调用）打 BigModel 端点 `https://open.bigmodel.cn/api/anthropic` 返回 `PONG`；端点已支持 tool_use（现有 ab_agent 在用）；自定义 base_url/key 经 `ClaudeAgentOptions(env={ANTHROPIC_BASE_URL, ANTHROPIC_API_KEY}, model=...)` 透传给子进程；工具层经 `@tool` + `create_sdk_mcp_server` in-process MCP 可原样移植。

## What Changes

- **①（核心）`run_episode` 手写 loop → `claude_agent_sdk.query()`**：删除 `_create_with_retry` / `run_episode` 循环体 / force-answer 兜底 / `_serialize_turn`，改为消费 `query()` 的 async 消息流。`max_steps` → `ClaudeAgentOptions.max_turns`；force-answer 兜底用"末轮 `max_turns` 耗尽后追加一次 `tools=[]` 的 `query()`"复刻（保 `truncated` 语义）。
- **②（核心）工具注册 schema-dict → `@tool` + in-process MCP**：`ab_tools.py` 的 `_X_DEF` schema dict + `register_tool` 改为 `@tool` 装饰器包同款 executor，`create_sdk_mcp_server("bench", tools=[...])` 挂进 `ClaudeAgentOptions.mcp_servers`；臂工具名 `grep_code` → `mcp__bench__grep_code`（仅 `ARMS` 数据里的工具名引用改）。**executor（`grep_code`/`cmm_search`/`read_file`/`codegraph_search`/`graphify_query`）与 `set_active` 的 target 注入零改**——工具在进程内执行，`_active` 仍生效。
- **③ sync → async 包裹**：`run_episode` 内部用 `anyio.run` 包 async `query()`，**对外签名保持同步**——`run_ab_agent.py` 的 `run_compare` / `run` 调用点零改。
- **④ trace 字段从消息流抽取，向后兼容**：`llm_calls`←`ResultMessage` num_turns / AssistantMessage 计数；`input_tokens`/`output_tokens`←累计各轮 usage；`session`←逐轮序列化的 text/tool_use/tool_result；`thinking`←thinking block（无则 fallback 该轮 text）；`cost_$`←`ResultMessage.total_cost_usd`（无则 token×单价 fallback）。**现有 trace dict 的全部 key 保留**，判分 / 聚合 / 报告写器零改。
- **⑤ 依赖**：`eval/requirements.txt` 加 `claude-agent-sdk`、`anyio`。`anthropic` 迁移后 ab_agent 不再 import——若全仓确认无其他引用则移除（**潜在 BREAKING**：env 需 `pip install -r eval/requirements.txt` 重装）。
- **不改**：判分（`_judge`/`_judge_retrieval`）、报告目录结构与写器、`bench` CLI、4 臂语义（tools+skills）、target 注入、goldgen、smoke `_mock_episode`。

## Capabilities

### New Capabilities

（无——本变更是 agent 运行时的实现迁移，不引入新能力。）

### Modified Capabilities

- `benchmark-agent-compare`:
  - 强化 `Agent episode trace capture`：trace 契约（`llm_calls`/`tool_steps`/`input_tokens`/`output_tokens`/`total_tokens`/`wall_clock_s`/`cost_$`/`session`/`thinking`/`truncated`）SHALL 与底层 agent 运行时无关——无论手写 ReAct loop 还是 `claude_agent_sdk`，同一 episode 产出的 trace 字段 SHALL 逐一对齐。本迁移为**纯实现重构**，不改变可观测契约；新增一条 regression-guard scenario 锁定迁移前后的 trace 等价性。

## Impact

- **代码**：`eval/ab_agent.py`（loop 重写为主，~80 行 → ~40 行）、`eval/ab_tools.py`（注册方式改 `@tool`，executor 不动）、`eval/run_ab_agent.py`（调用点零改，仅 import 必要时调整）、`eval/config.py`（`make_client` 相关字段保留，base_url/model 仍经 env 透传）。
- **依赖**：`eval/requirements.txt` +`claude-agent-sdk` +`anyio`；`anthropic` 待确认移除。
- **运行时**：每个 episode 多 spawn 一个 `claude` 子进程（SDK 封装本质）；`wall_clock_s` 可能因子进程启动开销略增——**design 须评估是否将该开销从 LLM 计时中剔除**，避免污染"效率"指标。
- **凭据**：`load_creds` 优先级（env > bench.local.yaml > config.toml）不变；`make_client` 删除（SDK 经 env 透传 base_url/key，不再构造 `anthropic.Anthropic`）。
- **回归风险**：trace 字段等价性（迁移前后 mock/固定 episode 对齐）、tool_use 往返正确性、force-answer/truncated 语义保真、async 包裹不阻塞调用方、子进程开销不污染效率指标。

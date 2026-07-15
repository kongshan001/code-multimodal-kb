# Tasks

## 1. 依赖与前置 spike

- [ ] 1.1 `eval/requirements.txt` 加 `claude-agent-sdk`、`anyio`；bench env `pip install -r eval/requirements.txt` → verify: `python -c "import claude_agent_sdk, anyio"` 成功
- [ ] 1.2 spike 验证 D1：用 `~/.cc-connect/config.toml` 的 key/base_url，`ClaudeAgentOptions(env={ANTHROPIC_BASE_URL, ANTHROPIC_API_KEY}, model=glm-5.1)` 跑一次 `query("只回复 PONG")` → verify: 返回含 PONG
- [ ] 1.3 spike 验证 Open Q1（最大未定项）：`system_prompt="只许用符号名作答"` 是否**完全替换** CLI 默认 prompt（检查 AssistantMessage 是否含 CLI 自带指令痕迹 / 是否 prepend）→ verify: 记录结论（替换 vs prepend）回填 design Open Q1；若 prepend 且无法关 → 决定接受"迁移后重立 accuracy 基线"并在 result.md 标注

## 2. 工具层迁移（ab_tools.py → @tool）

- [ ] 2.1 5 个 executor（`grep_code`/`cmm_search`/`read_file`/`codegraph_search`/`graphify_query`）各包 `@tool`，`input_schema` 用 dict 形式对齐现有 `_X_DEF`；executor 函数体不动 → verify: `@tool` 装饰对象可被 `create_sdk_mcp_server` 接受
- [ ] 2.2 建 `create_sdk_mcp_server("bench", tools=<臂工具子集>)` 工厂（按臂选工具）；`set_active` 与 `_active` 不动 → verify: monkeypatch `_active` 后 tool exec 仍读注入路径
- [ ] 2.3 `ARMS` 工具名引用 `grep_code` → `mcp__bench__grep_code`（5 个全改）；`arm_schemas`/`arm_config` 适配新命名 → verify: `arm_schemas("no-kb")` 返回新名工具
- [ ] 2.4 单测 `eval/tests/test_ab_tools.py`：in-process MCP server 注册后 tool 列表 == 臂声明工具 → verify: pytest 过

## 3. agent loop 重写（ab_agent.py）

- [ ] 3.1 删 `_create_with_retry`/`_serialize_turn`/`make_client`；`run_episode` 改 `anyio.run(_run_episode_async, ...)` 包裹，**对外同步签名不变** → verify: `run_episode(...)` 仍同步返 dict
- [ ] 3.2 `_run_episode_async`：组 `ClaudeAgentOptions(system_prompt=_system_prompt(arm,target), mcp_servers={"bench": server}, allowed_tools=[...], max_turns=max_steps, env={base_url,key}, model=mdl)`，消费 `query()` 消息流 → verify: 跑通一次真 episode
- [ ] 3.3 D5 trace 映射：从消息流抽 `llm_calls`/`tool_steps`/`tool_calls`/`tool_texts`/`input_tokens`/`output_tokens`/`session`/`thinking`/`cost_$`/`truncated`，填入与现 dict **完全同 key** 的结构 → verify: 返回 dict 的 key 集合 == 迁移前
- [ ] 3.4 D4 force-answer：max_turns 耗尽（无自然 end_turn）时追加一次 `allowed_tools=[]` 的 query，`truncated=True`，答案非空 fallback → verify: 构造必超步 prompt，断言 truncated=True 且 answer 非空
- [ ] 3.5 `load_creds` 保留优先级链（env > bench.local.yaml > config.toml），返 (api_key, base_url, model) 供 env 透传 → verify: 三来源分支单测仍过

## 4. 回归与端到端

- [ ] 4.1 单测：录一份 SDK 消息流 fixture，断言 `_run_episode_async` 抽出的 trace（key 集合 + tool_steps + truncated 语义）→ verify: pytest 过
- [ ] 4.2 specs regression scenario：新 trace dict.keys() ⊇ `{answer, input_tokens, output_tokens, total_tokens, steps, llm_calls, tool_calls, tool_steps, tool_texts, truncated, wall_clock_s, cost_$, session, thinking}` → verify: 断言通过
- [ ] 4.3 端到端：`bench run ab-agent --target godot-core --subset 2`（或 `run_compare` 4 臂 subset）真跑 → verify: 出报告、4 臂 trace 字段齐全、accuracy 合理（结合 1.3 结论判基线）
- [ ] 4.4 `eval/tests/test_ab_agent.py` / `test_agent_compare.py` 跑通（必要时适配 mock）→ verify: pytest 全绿

## 5. 清理与提交

- [ ] 5.1 全仓 grep `import anthropic` / `anthropic.` 确认迁移后无其他活引用 → verify: 仅历史 git 记录、无活引用
- [ ] 5.2 若 5.1 确认无引用：`eval/requirements.txt` 移除 `anthropic`；`setup-bench.bat`/setup 文档注明 SDK 依赖 → verify: 重装 env 后 smoke 仍过
- [ ] 5.3 提交 git（main + push，带 Co-Authored-By）；归档前 `openspec validate migrate-ab-agent-to-claude-sdk` → verify: validate 通过

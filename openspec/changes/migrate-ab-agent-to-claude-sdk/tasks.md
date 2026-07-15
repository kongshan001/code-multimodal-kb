# Tasks

## 1. 依赖与前置 spike

- [x] 1.1 `eval/requirements.txt` 加 `claude-agent-sdk`、`anyio`；bench env `pip install -r eval/requirements.txt`（**注意**：本机 python CA 有坑，pip 须加 `--trusted-host pypi.org --trusted-host files.pythonhosted.org`）→ ✅ 装进 anaconda bench env（python 3.12.7），`import claude_agent_sdk, anyio, anthropic` 全通
- [x] 1.2 spike 验证 D1（env 透传）→ ✅ spike1 P1-P4 全通
- [x] 1.3 spike 验证 Open Q1（go/no-go gate）→ ✅ **GO**：system_prompt 覆盖身份；最小配置剥 token 税 22-40k→392-632；tool_use 通

## 2. 工具层迁移（ab_tools.py → @tool）

- [x] 2.1 5 个 executor 包 `@tool`（input_schema 复用 `_X_DEF`，已验 @tool 吃完整 JSON schema）；executor 函数体不动 → ✅
- [x] 2.2 `arm_mcp_server(arm, sink)` 工厂（按臂选工具子集，sink 捕结果）；`set_active`/`_active` 不动 → ✅
- [x] 2.3 `arm_allowed_tools(arm)` 派生 `mcp__bench__<bare>`；**ARMS 仍存 bare 名**（比字面改 ARMS 更干净，前缀在 allowed_tools 派生）→ ✅
- [x] 2.4 单测 `test_ab_tools.py` 加 MCP 层 case（build + sink 捕获）→ ✅ 79/79 过

## 3. agent loop 重写（ab_agent.py）

- [x] 3.1 删 `_create_with_retry`/`_serialize_turn`；`run_episode` 改 `anyio.run` 包同步；**`make_client` 保留**（cli/run_doc_quality_ragas/run_memory_quality 仍直连 anthropic 用）→ ✅
- [x] 3.2 `_run_episode_async` 最小配置（D7：`tools=[]`+`setting_sources=[]`）+ `@tool` sink 捕结果 → ✅ 真跑 input_tokens 958/1755（< 5000）
- [x] 3.3 trace 映射：消息流按**类名**判型（TextBlock/ToolUseBlock/ThinkingBlock，无 .type 属性）+ 剥 `mcp__bench__` 前缀；滤 SystemMessage/HookEvent 噪声；cache_read 单列 → ✅
- [x] 3.4 D4 force-answer：max_turns 耗尽 SDK 抛异常 → `_consume` try/except 接住，answer 空→追加无工具 query 强制作答，`truncated=True` → ✅ 真跑验证（VMap 题 truncated 不崩、答案非空）
- [x] 3.5 `load_creds` 优先级链保留（env > bench.local.yaml > config.toml）→ ✅

## 4. 回归与端到端

- [x] 4.1 单测 mock 消息流（fake AssistantMessage/ResultMessage/TextBlock/ToolUseBlock）断言 trace 抽取 → ✅
- [x] 4.2 specs regression：trace dict.keys() ⊇ 全契约字段 → ✅ 断言进 test_ab_agent
- [x] 4.3 端到端 `bench run agent-compare --arms no-kb,kb --subset 1`：真跑出报告、trace 字段齐全 → ✅
- [x] 4.4 `test_ab_agent.py`/`test_agent_compare.py` 适配 mock 跑通 → ✅ 79/79 全绿
- [x] 4.5 token 税回归门 input_tokens<5000 → ✅ 真跑 958/963/1755 全过
- [x] 4.6 **顺手修既有 bug**：`agent_compare_report._clean_episode` 空 body 致 episode.json 落 null（body 误漂进 `_episode_md` return 后成死代码）。修 + 加 regression 断言（episode.json 非空 + trace 字段全）。**非本迁移引入**，但堵在 trace 契约落盘路径上，必须修。

## 5. 清理与提交

- [x] 5.1 grep `anthropic` 活引用：仅 `ab_agent.py`(make_client)；make_client 仍被 cli/run_doc_quality_ragas/run_memory_quality/test_memory_quality 用 → **anthropic 必须留**
- [x] ~~5.2 移除 `anthropic`~~ **取消**：5.1 证明 make_client 仍有 4 个消费者直连 anthropic，依赖保留
- [ ] 5.3 提交 git（main + push，带 Co-Authored-By）；归档前 `openspec validate` → 进行中

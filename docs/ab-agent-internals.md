# ab_agent 内部机制（agent loop / 提示词 / 轮次 / token 计算）

> 供外部人员评审 `eval/ab_agent.py` 的 agent loop 合理性。源码为准（本文引用行号对应 `eval/ab_agent.py`
> + `eval/ab_tools.py` 当前版本）。写于 2026-07-18。
>
> 一句话：`ab_agent` 给一道题跑一个 **带工具的 agent**（不是单次问答），测它能不能用 grep/cmm/读文件
> 找到 gold 符号。有两个等价 engine（`sdk` 默认 / `raw` 对照），同策略、同 trace 契约。

---

## 0. 为什么要"多轮"（不是问一次答一次）

普通聊天：发问题 → 模型凭记忆答 → 1 次 API 调用。

本 benchmark 的 agent **带工具、看不到代码库**：模型得先调工具查，拿到结果再决定答不答。每调一次工具 =
模型被调一次。所以一道题内部是**循环**：

```
轮1：发题 → 模型「我搜一下」→ 调 cmm_search
        （工具返回结果）
轮2：发题+结果 → 模型「找到了，答 Color」→ 结束
```

`llm_calls`（轮次）数的就是**这道题内部模型被调了多少次**，不是"问了几道题"。正常 1-5 次；卡死的题
可能滚到上限（默认 30，no-kb 臂 12）还没答出。`max_turns` 是**防死循环的安全阀**（`bench.yaml` 分臂可配）。

---

## 1. 两 engine 架构

| | `sdk`（默认） | `raw`（A/B 对照） |
|---|---|---|
| loop 实现 | `claude_agent_sdk.query()`（封装 `claude` CLI 子进程） | 手写 ReAct loop，裸 `anthropic.messages.create` |
| 多轮消息 | **SDK 内部管理**（我不碰 messages） | **我手搓 messages 列表** |
| 工具形态 | `@tool` + in-process MCP server | JSON schema dict + `exec_tool` |
| thinking | SDK 默认开（`ThinkingBlock`） | 不请求（无） |
| prompt caching | 有（`cache_read_input_tokens` 累计） | 无（`cache_read` 恒 0） |
| temperature / max_tokens | SDK 默认 | 显式 `temperature=0.0, max_tokens=1024` |
| 凭据 | 经 `env={ANTHROPIC_BASE_URL, ANTHROPIC_API_KEY}` 透传给 CLI 子进程 | `anthropic.Anthropic(api_key, base_url)` 直连 |
| 收敛策略 | **相同**：backstop（默认 30，**no-kb 臂 12** 控空转成本，分臂可配）、无 force-answer、run-until-answer | 同左 |
| trace 契约 | 逐字段对齐（raw 的 `cache_read_tokens` 恒 0） | 同 |

入口 `run_episode(question, arm, target, model, max_steps, engine="sdk")`（:311）按 `engine` 分发。

---

## 2. 提示词怎么拼（`_system_prompt`，:30-43）

模型每轮的 **system 消息**由 `_system_prompt(arm, target)` 拼，三段：

```python
parts = [BASE_SYS_PROMPT]                              # ① 基底纪律（:23-27，固定）
if target: parts.append(f"（目标代码库：{lang}。{notes}）")   # ② 目标上下文（target.json）
for s in arm_skills(arm): parts.append(skill SOP)     # ③ skill SOP（仅 skills 臂）
```

- **① BASE_SYS_PROMPT**（固定）：「你是代码定位助手…用**符号名**作答…**收敛纪律：查到即答，不要反复查**」。
- **② 目标上下文**：`target.json` 的 `language` + `notes`，如「（目标代码库：C++。Godot 4.7 core/, 13504 节点…）」。
- **③ skill SOP**（`ab_tools.arm_skills(arm)`）：**仅 `kb+superpowers` / `kb+openspec`** 追加。把
  `eval/arms/skills_bundled/{superpowers,openspec}.md` 整篇原文塞进去（前缀「# 注入的工程纪律」）。

→ 各臂 system prompt 体积不同（这是 `cache_read` 差异的根源）：

| 臂 | system_prompt 构成 | 约大小 |
|---|---|---|
| `no-kb` / `kb` | ① + ② | ~150 token |
| `kb+superpowers` | ① + ② + superpowers.md(27行) | ~+500 token |
| `kb+openspec` | ① + ② + openspec.md(22行) | ~+400 token |

> **题目（user 消息）从不修改**——原样发。`session` 里第一条 `{"role":"user","content":question}` 是给我
> 本地日志用的；真正发模型的是 `query(prompt=question)`（sdk）或 `messages=[{user:question}]`（raw）。

---

## 3. 问题怎么发——sdk engine（`_run_episode_async`，:150）

```python
options = ClaudeAgentOptions(
    model=mdl, env=env, system_prompt=sys_prompt,
    tools=[], setting_sources=[],                 # D7：剥 CLI 默认工具定义（否则 token 税 22-40k）
    permission_mode="bypassPermissions",          # headless 无交互，自动批准工具调用
    mcp_servers={"bench": ab_tools.arm_mcp_server(arm, tool_sink)},
    allowed_tools=ab_tools.arm_allowed_tools(arm),
    max_turns=max_steps, include_hook_events=False,
)
async for msg in query(prompt=question, options=options): ...   # :121
```

`query()` 启动 `claude` CLI 子进程，**真正拼 HTTP 请求的是 SDK/CLI**。我传的三样落到请求里：

| 传入 | 请求位置 | 内容 |
|---|---|---|
| `prompt=question` | 第一条 **user** 消息 | 题目原文 |
| `system_prompt=sys_prompt` | **system** 消息 | §2 拼的三段 |
| `mcp_servers` + `allowed_tools` | **tools** 定义 | 该臂工具的 name/description/input_schema |

模型回 `tool_use` → SDK 调我的 `@tool` wrapper（`ab_tools.mcp_tool`）→ 跑 `exec_fn` → 结果塞回 →
SDK 再调模型。**多轮往返全在 SDK 内部，我不维护 messages。**

> D7 为什么 `tools=[] + setting_sources=[]`：CLI 默认会注入 Bash/Read/Grep 等内置工具定义 + 用户
> settings，使每次 input 膨胀到 22-40k token（实测）。关掉后降到几百 token，保 token 指标不失真。
> 代价：agent 只能用我给的 bench 工具（这正是隔离测量想要的）。

---

## 4. 问题怎么发——raw engine（`run_episode_raw`，:245）

raw 是**我手搓 ReAct loop**，直连 `anthropic.messages.create`：

```python
client = make_client()                                   # anthropic.Anthropic(api_key, base_url)
tools = ab_tools.arm_schemas(arm)                        # JSON schema dict 列表
messages = [{"role": "user", "content": question}]       # 我自己维护这个 list
for _ in range(max_steps):                               # :266 —— 循环上限 = max_steps
    resp = _create_with_retry(client, mdl, sys_prompt, messages, tools)
    #  ↑ client.messages.create(model, max_tokens=1024, system=sys_prompt,
    #                           messages=messages, tools=tools, temperature=0.0)
    messages.append({"role": "assistant", "content": resp.content})
    if resp.stop_reason == "tool_use":
        results = []
        for block in resp.content:
            if block.type == "tool_use":
                result = ab_tools.exec_tool(block.name, dict(block.input))   # 我直接调工具
                results.append({"type": "tool_result", "tool_use_id": block.id, "content": result})
        messages.append({"role": "user", "content": results})                # 结果塞回 messages
    else:                                # end_turn → 自然作答
        answer = turn_text; break
else:                                    # range 跑满没 break → 卡死
    truncated = True; answer = last_text or "(未在限定步数内自然作答)"
```

**和 sdk 的本质差**：
- `messages` 列表**我亲自 append**（assistant 响应 + tool_result），每轮把**全量历史**重发给模型。
- `system=sys_prompt` 每次调用都传（anthropic API 的 system 不在 messages 里，单独参数）。
- 工具结果**全量**进 messages（`tool_result_cap` 只截我本地 session 日志，:287；**喂给模型的不截**）。
- `temperature=0.0`、`max_tokens=1024` 显式；**不请求 thinking**（无 `thinking` 参数）→ 无 ThinkingBlock。
- 不设 `cache_control` → **无 prompt caching**，`cache_read` 恒 0。
- 收敛/截断策略与 sdk **完全一致**（backstop 30、无 force-answer、run-until-answer）。

---

## 5. 轮次（`llm_calls`）怎么算

### sdk engine（`_consume`，:111-147）

```python
async for msg in query(...):
    if type(msg).__name__ == "AssistantMessage":        # 一次模型响应
        blocks, text, think, tnames = _extract_assistant(msg)
        if text.strip() or tnames:                      # 有文本/工具调用才 +1（跳纯 ThinkingBlock 消息）
            llm_calls += 1
        tool_calls.extend(tnames)
```

**定义：`llm_calls` = "产出过文本或工具调用"的 `AssistantMessage` 个数。**（纯思考消息不计。）

- 一个 `AssistantMessage` 可含**多个 `tool_use` block**（模型并行调多工具）→ 算 **1 个 llm_call**，
  但 `tool_calls` 收多个 → `tool_steps = len(tool_calls)` 可 > `llm_calls`。
- 上限：`max_turns`（默认 30，**no-kb 臂 12**）是 **SDK 的循环硬上限**（不是我数的）。到顶 SDK 停——某些版本抛
  `Reached maximum number of turns`（被 :145 `except` 接住），某些版本发带 usage 的空 ResultMessage。

### raw engine（`run_episode_raw`，:266-292）

```python
for _ in range(max_steps):
    resp = _create_with_retry(...)   # 每次 = 1 次 messages.create
    llm_calls += 1                   # 每次迭代都 +1
```

**定义：`llm_calls` = `messages.create` 调用次数 = 循环迭代数。**（raw 不请求 thinking，每次迭代必产出
text 或 tool_use，所以无"空轮"要过滤。）

### 两者可比性

口径接近（都 ≈ "模型为这道题被有效调用的次数"），但有细微差：
- sdk 可能少计纯 thinking 消息；raw 无 thinking，每次都计。
- sdk 的 "turn" 与 raw 的 "iteration" 在并行工具调用时口径略不同。
- 实测：两 engine 在同一题上 `llm_calls` 通常相差 ≤1（见 `analysis.md §7` A/B，97.4% 题判分一致）。

---

## 6. token 怎么算

### sdk engine（`_consume` ResultMessage 分支，:134-144）

```python
elif t == "ResultMessage":
    u = msg.usage                                  # ★ 整个 episode 跨所有轮的「累计」值
    in_tok    += u["input_tokens"]                 # 新读（未命中缓存）
    out_tok   += u["output_tokens"]
    cache_read+= u["cache_read_input_tokens"]      # 缓存重读
    cost = msg.total_cost_usd                      # SDK 按 cache 折价算的成本
    if msg.result.strip(): answer = msg.result
```

`ResultMessage` 在 episode 结束时发**一次**，`usage` 是**全 episode 累计**（不是单轮）。然后（:190）：

```python
total = in_tok + out_tok + cache_read              # 真实处理量（含缓存重读）
```

成本（:198）：优先 `total_cost_usd`（cache 折价，准），缺失才退回 `_cost(in,out)`（全价、不含 cache）。

> **`cache_read` 是什么**：每轮模型要重读 [system_prompt + 之前全部 tool_result] 这个稳定前缀；命中
> prompt 缓存的部分走 `cache_read_input_tokens`（计价 ~0.1×）。旧版 `total = in+out` 漏算它 → 缓存多的
> 臂（prompt 大的 skills 臂）**虚省**。现版含 cache_read，反映模型真实处理量。

### raw engine（`run_episode_raw`，:268-269 + :298）

```python
for _ in range(max_steps):
    resp = _create_with_retry(...)
    in_tok += resp.usage.input_tokens              # 每次 create 的 usage，逐次累加
    out_tok+= resp.usage.output_tokens
...
total = in_tok + out_tok                           # 无 cache_read（raw 无 caching）
```

**定义：`total = Σ 每次调用的 (input+output)`，无缓存成分。**（raw 不设 cache_control，每次把全量
messages 重发，input 随历史增长。）

### 两者 token 数能直接比吗？

不能简单比绝对值——口径不同：
- sdk `total` 含 `cache_read`（缓存重读），raw 不含。同一条题 sdk 的 `total` 通常比 raw **高**（因为
  把缓存重读也算进去），但**实际花费** sdk 更低（cache 折价）。所以看 `cost_$`（都优先用 cache 折价的
  `total_cost_usd`）比看 `total_tokens` 公平。
- raw 每轮重发全量历史（无缓存折扣），stuck 题 token 同样雪崩，只是没有 `cache_read` 这一项。

---

## 7. 卡死案例串讲（DSL 题：`llm_calls=33 · tokens=153463 · 截断`）

1. 题发出去，模型调工具（grep/read）找 `dsl_path`。
2. 没找到 → 换词再 grep / 读别的文件 → 又没找到 → ……（每轮 1 个工具，串行）。
3. 每轮 tool_result 进历史；下一轮模型重读**全部累积历史** → 输入 token 滚雪球。
4. 撞 `max_turns=30`（实测到 33，因 SDK 一轮可含多 block / 口径差）→ SDK 发空 ResultMessage（带累计
   usage=153463）→ `answer` 空 → `truncated=True`，答案留「(未在限定步数内自然作答)」。
5. 153463 = 33 轮的 (input+output+cache_read) **累加**，cache_read 占大头（system_prompt + 胖历史每轮缓存重读）。

正常题（1-3 轮收敛）这个数 ~1000-2000。**卡死题的成本 = 正常题的 ~100 倍**，被 backstop 30 兜住（没无限）。

---

## 8. 合理性评估要点（给外部审）

**测量上严谨的地方：**
- `temperature=0`（raw 显式；sdk 默认偏低），尽力可复现。
- 两 engine 同策略对照（`--engine sdk|raw`），可交叉验证 loop 实现没引入偏差。
- token 含 `cache_read`（真实处理量）、cost 用 cache 折价（真实花费），两个口径都给。
- trace 字段全（answer/tokens/llm_calls/tool_calls/tool_texts/session/thinking/truncated/cache_read），可审计。
- 判分零 LLM judge（gold 符号 broad 子串），避免 judge 自身噪声。

**已知边界 / 局限（评审应知悉）：**
- **SDK engine 不可控项**：thinking 默认开、caching 默认开、temperature/max_tokens 走 SDK 默认——这些
  我不直接控，是 `claude` CLI 行为。raw engine 显式控（temp=0、无 thinking、无 caching），可作为对照。
- **`llm_calls` 两 engine 口径微差**（纯 thinking 消息 / 并行工具），差 ≤1，不影响结论但非字字相等。
- **stuck 题成本爆炸**：backstop（默认 30；**no-kb 臂已降到 12 控成本**）兜住上限，但单题仍可烧几万 token
  （雪球）。进一步控成本可继续调小分臂 backstop（注意 read_file 深位 gold 是独立议题，别用截断结果的方式）。
- **skill 注入是文本近似**：skills 臂注入的是精简 SOP 文本，**不是真 superpowers/openspec 运行时**
  （无触发/hook）。
- **n=1 方差大**：API 非完全确定（即便 temp=0），同题两次跑准确率会洗牌；要稳结论需多 run 取均值。
- **题集偏简单**：多数 code_retrieval 是模型本就会的 → KB/skills 加分 marginal；要测出价值需加难。
- **glm-5.1 经此端点**：thinking/caching 行为是 BigModel anthropic 兼容端点的实现，非原生 Anthropic。

---

## 附：关键源码索引

| 关注点 | 位置 |
|---|---|
| 入口 / engine 分发 | `ab_agent.run_episode` (:311) |
| sdk loop | `_run_episode_async` (:150) + `_consume` (:111) |
| raw loop | `run_episode_raw` (:245) + `_create_with_retry` (:209) |
| system_prompt 拼装 | `_system_prompt` (:30) + `BASE_SYS_PROMPT` (:23) |
| 消息块解析 | `_extract_assistant` (:54, sdk) / `_serialize_turn` (:228, raw) |
| 工具注册 / skills 注入 | `ab_tools.ARMS` / `arm_skills` / `load_skill_content` |
| 工具 → MCP（sdk） | `ab_tools.mcp_tool` / `arm_mcp_server` / `arm_allowed_tools` |
| 配置（backstop/价格/截断） | `bench.yaml` → `eval/config.py` |

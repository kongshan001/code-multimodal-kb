"""Stage 1 agent A/B harness：claude_agent_sdk 驱动 agent loop 测 agent 答对率 + token。

**工具与臂在 `eval/ab_tools.py` 注册表**（接新 KB 工具只改注册表，本文件不动）。
本文件只管：组装 SDK options / 消费消息流抽 trace / run-until-answer backstop / 凭据 / 收敛纪律。
loop / 重试 / tool_use 往返 / 序列化全交 claude_agent_sdk（claude CLI 封装）。

两臂差异 = 发现工具（baseline=词面 grep / kb=语义 cmm / doc=文档 graphify），都给 read_file 保公平。
LLM：经 ClaudeAgentOptions.env 透传 base_url+key 打 BigModel anthropic 兼容端点（glm-5.x）。
判分（gold ∈ 终答）在 run_ab_agent.py。凭据从 env / bench.local.yaml / config.toml 读，不入库。

迁移自手写 ReAct loop（openspec change migrate-ab-agent-to-claude-sdk）；trace 字段逐字段不变。
"""
from __future__ import annotations

import os
import time

import anyio

from eval import ab_tools, config

# 目标感知的基底 system prompt（去 Godot 硬编码；目标信息由 _system_prompt 注入）
BASE_SYS_PROMPT = (
    "你是代码定位助手。用户问代码库的问题，你用提供的工具查找，然后用**符号名**作答。"
    "答案简短：直接给类/函数/方法名（如 `Color`、`ResourceLoader`），不要长解释。\n"
    "**收敛纪律**：一旦工具返回了相关符号就立刻用符号名作答，不要反复查。查到即答。"
)


def _system_prompt(arm: str, target: dict | None = None) -> str:
    """基底 prompt + 目标信息 + 注入的 skill SOP 文本。"""
    parts = [BASE_SYS_PROMPT]
    if target:
        lang = target.get("language", "")
        notes = target.get("notes", "")
        ctx = f"（目标代码库：{lang or '未知'}。{notes}）" if (lang or notes) else ""
        if ctx:
            parts.append("\n" + ctx)
    for s in ab_tools.arm_skills(arm):
        content = ab_tools.load_skill_content(s)
        if content:
            parts.append(f"\n\n# 注入的工程纪律（skill: {s}）\n{content}")
    return "".join(parts)


def _cost(model: str, in_tok: int, out_tok: int):
    """token×单价 → $。单价未知返 None（不报错）。"""
    p = config.llm()["prices"].get(model)
    if not p:
        return None
    return round((in_tok * p["in"] + out_tok * p["out"]) / 1e6, 4)


def _extract_assistant(msg) -> tuple[list, str, str, list[str]]:
    """把 AssistantMessage.content 序列化成 JSON-friendly blocks + 抽 text + thinking + tool_use 名。
    返 (blocks, text, thinking, tool_names)。thinking：有 thinking block 用之，无则 fallback 该轮 text。
    注：SDK 的 block 是 TextBlock/ToolUseBlock/ThinkingBlock 类对象，**无 .type 属性**——按类名判型。"""
    blocks, texts, thinks, tnames = [], [], [], []
    for b in getattr(msg, "content", []) or []:
        cn = type(b).__name__
        if cn == "TextBlock":
            tx = getattr(b, "text", "")
            blocks.append({"type": "text", "text": tx})
            texts.append(tx)
        elif cn == "ToolUseBlock":
            name = getattr(b, "name", "")
            bare = name[len("mcp__bench__"):] if name.startswith("mcp__bench__") else name
            blocks.append({"type": "tool_use", "name": bare, "input": dict(getattr(b, "input", {}) or {})})
            tnames.append(bare)
        elif cn == "ThinkingBlock":
            th = getattr(b, "thinking", "")
            blocks.append({"type": "thinking", "text": th})
            thinks.append(th)
    text = "".join(texts)
    think = "".join(thinks) if thinks else text   # 模型无关 fallback
    return blocks, text, think, tnames


# ── 凭据 ──────────────────────────────────────────────────────────────────

def load_creds() -> tuple[str, str, str]:
    """返 (api_key, base_url, model)。
    api_key 优先级：env AB_API_KEY > bench.local.yaml > config.toml。
    base_url + model **永远从 config（bench.yaml）读**——env 只提供 key，不覆盖 URL/model。
    （与迁移前同语义；现用于透传给 ClaudeAgentOptions.env。）"""
    _cfg = config.llm()
    if os.environ.get("AB_API_KEY"):
        return (os.environ["AB_API_KEY"], _cfg["base_url"], _cfg["model"])
    if _cfg.get("api_key"):   # bench.local.yaml → llm.api_key
        return (_cfg["api_key"], _cfg["base_url"], _cfg["model"])
    try:
        import tomllib
        with open(os.path.expanduser("~/.cc-connect/config.toml"), "rb") as f:
            data = tomllib.load(f)
        prov = data["projects"][0]["agent"]["providers"][0]
        return prov["api_key"], _cfg["base_url"], _cfg["model"]
    except Exception as e:
        raise RuntimeError(f"找不到 LLM 凭据（设 AB_API_KEY 或配 ~/.cc-connect/config.toml）: {e}")


def make_client():
    """直连 anthropic 客户端（供 run_memory_quality / run_doc_quality_ragas / cli 等自管 LLM 调用用）。
    注：ab_agent 的 run_episode 已改走 claude_agent_sdk，不再用本客户端；保留给其它直连消费者。"""
    import anthropic  # 延迟导入
    key, base_url, _ = load_creds()
    return anthropic.Anthropic(api_key=key, base_url=base_url)


# ── agent loop（claude_agent_sdk）─────────────────────────────────────────

async def _consume(query_fn, prompt, options, session, thinking, sink=None):
    """消费 query() 消息流，只认 AssistantMessage/ResultMessage（滤 SystemMessage/HookEventMessage 噪声）。
    累计 tokens / llm_calls / tool_calls；返 (answer, last_text, in_tok, out_tok, cache_read, cost, llm_calls, tool_calls)。
    max_turns 耗尽时 SDK 抛 'Reached maximum number of turns'——catch 之，返已累计的（answer 留空 → 触发 force-answer）。
    注：此情形下 ResultMessage 未到，该 query 的 token 计为 0（force-query 的 token 仍计入）。"""
    in_tok = out_tok = cache_read = llm_calls = 0
    last_text = answer = ""
    cost = None
    tool_calls: list[str] = []
    try:
        async for msg in query_fn(prompt=prompt, options=options):
            t = type(msg).__name__
            if t == "AssistantMessage":
                blocks, text, think, tnames = _extract_assistant(msg)
                if text.strip() or tnames:   # 有 text/tool_use 才算一轮（不数纯 ThinkingBlock 消息）
                    llm_calls += 1
                if blocks:
                    session.append({"role": "assistant", "content": blocks})
                if think:
                    thinking.append(think)
                if text.strip():
                    last_text = text
                tool_calls.extend(tnames)
            elif t == "ResultMessage":
                u = getattr(msg, "usage", None) or {}
                in_tok += int(u.get("input_tokens") or 0)
                out_tok += int(u.get("output_tokens") or 0)
                cache_read += int(u.get("cache_read_input_tokens") or 0)
                c = getattr(msg, "total_cost_usd", None)
                if c:
                    cost = c
                r = getattr(msg, "result", "") or ""
                if r.strip():
                    answer = r
    except Exception:
        pass   # max_turns 耗尽等 → answer 留空，run_episode 标 truncated（不 inject 猜测）
    return answer, last_text, in_tok, out_tok, cache_read, cost, llm_calls, tool_calls


async def _run_episode_async(question: str, arm: str, target: dict | None,
                             mdl: str, max_steps: int | None) -> dict:
    from claude_agent_sdk import query, ClaudeAgentOptions

    sys_prompt = _system_prompt(arm, target)
    ab_tools.set_active(target)   # 臂 executor 读当前 target 的 cmm/codegraph/doc 路径
    if max_steps is None:
        max_steps = config.agent()["skill_max_steps"] if ab_tools.arm_skills(arm) else config.agent()["max_steps"]

    key, base_url, _ = load_creds()
    env = {"ANTHROPIC_BASE_URL": base_url, "ANTHROPIC_API_KEY": key}
    tool_sink: list = []   # 捕 (name, result)——run_episode 用来填 tool_texts

    # D7 硬约束：tools=[] + setting_sources=[] 剥掉 CLI 默认工具定义（否则 token 税 22-40k）
    options = ClaudeAgentOptions(
        model=mdl, env=env, system_prompt=sys_prompt,
        tools=[], setting_sources=[],
        mcp_servers={"bench": ab_tools.arm_mcp_server(arm, tool_sink)},
        allowed_tools=ab_tools.arm_allowed_tools(arm),
        max_turns=max_steps, include_hook_events=False,
    )

    session: list[dict] = [{"role": "user", "content": question}]
    thinking: list[str] = []
    answer, last_text, in_tok, out_tok, cache_read, cost, llm_calls, tool_calls = await _consume(
        query, question, options, session, thinking)

    # run-until-answer：不 inject 猜测。跑满 backstop 仍未自然作答 → 真卡住，诚实标 truncated。
    truncated = not bool(answer.strip())
    if truncated:
        answer = (last_text or "(未在限定步数内自然作答)").strip()

    # tool_results 进 session（从 sink，截断；review 用）
    cap = config.agent()["tool_result_cap"]
    for name, result in tool_sink:
        session.append({"role": "user", "content": [{"type": "tool_result",
                          "tool_use_id": None, "content": str(result)[:cap]}]})

    total = in_tok + out_tok
    return {
        "answer": answer.strip(), "input_tokens": in_tok, "output_tokens": out_tok,
        "total_tokens": total,
        "steps": llm_calls, "llm_calls": llm_calls,   # steps = 别名（向后兼容）
        "tool_calls": tool_calls, "tool_steps": len(tool_calls),
        "tool_texts": [t for _, t in tool_sink],
        "truncated": truncated, "wall_clock_s": 0,    # run_episode 同步包裹填
        "cost_$": cost if cost is not None else _cost(mdl, in_tok, out_tok),
        "session": session, "thinking": thinking,
        "cache_read_tokens": cache_read,
    }


def run_episode(question: str, arm: str, target: dict | None = None,
                model: str = "", max_steps: int | None = None) -> dict:
    """跑一次 agent episode（同步；内部 anyio.run 包 async query）。arm 决定工具集 + skills 注入。
    返回 trace（字段与迁移前逐一对齐，见 openspec specs delta）。"""
    _, _, mdl = load_creds() if not model else (None, None, model)
    t0 = time.time()
    trace = anyio.run(_run_episode_async, question, arm, target, mdl, max_steps)
    trace["wall_clock_s"] = round(time.time() - t0, 2)
    return trace

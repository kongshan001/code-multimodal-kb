"""Stage 1 agent A/B harness（task 6.3 实施）：可控 ReAct loop 测 agent 答对率 + token。

**工具与臂在 `eval/ab_tools.py` 注册表**（接新 KB 工具只改注册表，本文件不动）。
本文件只管：agent loop / token 累计 / 429 退避 / 凭据 / 收敛纪律。

两臂差异 = 发现工具（baseline=词面 grep / kb=语义 cmm / doc=文档 graphify），都给 read_file 保公平。
LLM：BigModel anthropic 兼容端点（glm-5.x），tool_use + usage 计 token。
判分（gold ∈ 终答）在 run_ab_agent.py。凭据从 env 或 ~/.cc-connect/config.toml 读，不入库。
"""
from __future__ import annotations

import os
import time
from typing import Any

from eval import ab_tools

MAX_STEPS = 6            # 非 skills 臂最多轮（控成本）；skills 臂放宽到 SKILL_MAX_STEPS
SKILL_MAX_STEPS = 10     # skills 臂 SOP 更费步
DEFAULT_BASE_URL = "https://open.bigmodel.cn/api/anthropic"
DEFAULT_MODEL = "glm-5.1"

# 目标感知的基底 system prompt（去 Godot 硬编码；目标信息由 _system_prompt 注入）
BASE_SYS_PROMPT = (
    "你是代码定位助手。用户问代码库的问题，你用提供的工具查找，然后用**符号名**作答。"
    "答案简短：直接给类/函数/方法名（如 `Color`、`ResourceLoader`），不要长解释。\n"
    "**收敛纪律**：一旦工具返回了相关符号就立刻用符号名作答，不要反复查。查到即答。"
)

# 模型单价 $/Mtoken（OQ2：占位，待查 BigModel 实际定价；未知模型 → cost None）
MODEL_PRICES = {
    "glm-5.1": {"in": 0.70, "out": 0.70},
    "glm-5.2": {"in": 0.70, "out": 0.70},
}

TOOL_RESULT_CAP = 2000   # tool_result 序列化截断（防 session.jsonl 膨胀）


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
    p = MODEL_PRICES.get(model)
    if not p:
        return None
    return round((in_tok * p["in"] + out_tok * p["out"]) / 1e6, 4)


def _serialize_turn(resp) -> tuple[list, str, str]:
    """把一轮 resp.content 序列化成 JSON-friendly blocks + 抽 text + thinking（模型无关）。

    返 (blocks, turn_text, turn_thinking)。thinking：有 thinking block 用之，无则 fallback 该轮 text。
    """
    blocks, texts, thinks = [], [], []
    for b in resp.content:
        t = getattr(b, "type", "")
        if t == "text":
            tx = getattr(b, "text", "")
            blocks.append({"type": "text", "text": tx})
            texts.append(tx)
        elif t == "tool_use":
            blocks.append({"type": "tool_use", "name": b.name, "input": dict(b.input)})
        elif t == "thinking":
            th = getattr(b, "thinking", "") or getattr(b, "text", "")
            blocks.append({"type": "thinking", "text": th})
            thinks.append(th)
    turn_text = "".join(texts)
    turn_thinking = "".join(thinks) if thinks else turn_text  # 模型无关 fallback
    return blocks, turn_text, turn_thinking


def _exec_tool(name: str, inputs: dict) -> str:
    """薄封装→注册表（保留为模块级，便于测试 monkeypatch）。"""
    return ab_tools.exec_tool(name, inputs)


# ── 凭据 ──────────────────────────────────────────────────────────────────

def load_creds() -> tuple[str, str, str]:
    """返 (api_key, base_url, model)。env 优先，否则读 ~/.cc-connect/config.toml。"""
    if os.environ.get("AB_API_KEY"):
        return (os.environ["AB_API_KEY"],
                os.environ.get("AB_BASE_URL", DEFAULT_BASE_URL),
                os.environ.get("AB_MODEL", DEFAULT_MODEL))
    try:
        import tomllib
        with open(os.path.expanduser("~/.cc-connect/config.toml"), "rb") as f:
            data = tomllib.load(f)
        prov = data["projects"][0]["agent"]["providers"][0]
        return prov["api_key"], prov.get("base_url", DEFAULT_BASE_URL), prov.get("model", DEFAULT_MODEL)
    except Exception as e:
        raise RuntimeError(f"找不到 LLM 凭据（设 AB_API_KEY 或配 ~/.cc-connect/config.toml）: {e}")


def make_client():
    import anthropic  # 延迟导入（smoke/mock 不需要）
    key, base_url, _ = load_creds()
    return anthropic.Anthropic(api_key=key, base_url=base_url)


# ── agent loop ────────────────────────────────────────────────────────────

def _create_with_retry(client, model, system, messages, tools, retries=4) -> Any:
    """带 429/529/503 退避重试。"""
    import anthropic  # 延迟导入：smoke/mock 模式无需装 anthropic（spec 无凭据降级）
    last = None
    for i in range(retries + 1):
        try:
            return client.messages.create(
                model=model, max_tokens=1024, system=system,
                messages=messages, tools=tools, temperature=0.0,
            )
        except anthropic.RateLimitError as e:
            last = e
        except anthropic.APIStatusError as e:
            last = e
            if e.status_code not in (429, 500, 502, 503, 529):
                raise
        if i < retries:
            time.sleep(2 ** i)  # 1,2,4,8s
    raise RuntimeError(f"LLM 调用重试 {retries} 次仍失败: {last}")


def run_episode(client, question: str, arm: str, target: dict | None = None,
                model: str = "", max_steps: int | None = None) -> dict:
    """跑一次 agent episode。arm 决定工具集 + skills 注入（见 ab_tools.ARMS）。

    返回 trace：{answer, input/output/total_tokens, steps(=llm_calls 别名), llm_calls,
    tool_calls[], tool_steps, tool_texts[], truncated, wall_clock_s, cost_$, session[], thinking[]}。
    session = 逐轮序列化消息流（thinking = 模型无关：有 thinking block 用之，无则 fallback text）。
    """
    _, _, mdl = load_creds() if not model else (None, None, model)
    sys_prompt = _system_prompt(arm, target)
    if max_steps is None:
        max_steps = SKILL_MAX_STEPS if ab_tools.arm_skills(arm) else MAX_STEPS
    tools = ab_tools.arm_schemas(arm)
    messages: list[dict] = [{"role": "user", "content": question}]
    in_tok = out_tok = llm_calls = 0
    tool_calls: list[str] = []
    tool_texts: list[str] = []
    session: list[dict] = [{"role": "user", "content": question}]
    thinking: list[str] = []
    last_text = ""
    answer = ""
    truncated = False
    t0 = time.time()

    for _ in range(max_steps):
        resp = _create_with_retry(client, mdl, sys_prompt, messages, tools)
        in_tok += getattr(resp.usage, "input_tokens", 0)
        out_tok += getattr(resp.usage, "output_tokens", 0)
        llm_calls += 1

        turn_blocks, turn_text, turn_thinking = _serialize_turn(resp)
        session.append({"role": "assistant", "content": turn_blocks})
        thinking.append(turn_thinking)
        if turn_text.strip():
            last_text = turn_text
        messages.append({"role": "assistant", "content": resp.content})

        if resp.stop_reason == "tool_use":
            results, serialized_results = [], []
            for block in resp.content:
                if getattr(block, "type", "") == "tool_use":
                    result = _exec_tool(block.name, dict(block.input))
                    result_s = str(result)
                    tool_calls.append(block.name)
                    tool_texts.append(result_s)
                    results.append({"type": "tool_result", "tool_use_id": block.id, "content": result})
                    serialized_results.append({"type": "tool_result", "tool_use_id": block.id,
                                               "content": result_s[:TOOL_RESULT_CAP]})
            messages.append({"role": "user", "content": results})
            session.append({"role": "user", "content": serialized_results})
        else:  # end_turn → 取本轮 text 作答
            answer = turn_text
            break
    else:
        truncated = True
        answer = last_text or "(max_steps reached without final answer)"

    wall = round(time.time() - t0, 2)
    return {
        "answer": answer.strip(), "input_tokens": in_tok, "output_tokens": out_tok,
        "total_tokens": in_tok + out_tok,
        "steps": llm_calls, "llm_calls": llm_calls,   # steps = 别名（向后兼容）
        "tool_calls": tool_calls, "tool_steps": len(tool_calls), "tool_texts": tool_texts,
        "truncated": truncated, "wall_clock_s": wall,
        "cost_$": _cost(mdl, in_tok, out_tok),
        "session": session, "thinking": thinking,
    }

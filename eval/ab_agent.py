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

import anthropic

from eval import ab_tools

MAX_STEPS = 6            # agent 最多轮（控成本）
DEFAULT_BASE_URL = "https://open.bigmodel.cn/api/anthropic"
DEFAULT_MODEL = "glm-5.1"

SYS_PROMPT = (
    "你是代码定位助手。用户问 Godot 引擎 core/ 代码库的问题，你用提供的工具查找，"
    "然后用**符号名**作答。答案要简短：直接给类/函数/方法名（如 `Color`、`ResourceLoader`），"
    "不要长解释。\n"
    "**收敛纪律**：最多调 2 次工具，一旦工具返回了相关符号就**立刻**用符号名作答，不要反复查、"
    "不要读多个文件。查到即答。"
)


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


def make_client() -> anthropic.Anthropic:
    key, base_url, _ = load_creds()
    return anthropic.Anthropic(api_key=key, base_url=base_url)


# ── agent loop ────────────────────────────────────────────────────────────

def _create_with_retry(client, model, system, messages, tools, retries=4) -> Any:
    """带 429/529/503 退避重试。"""
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


def run_episode(client, question: str, arm: str, model: str = "",
                max_steps: int = MAX_STEPS) -> dict:
    """跑一次 agent episode。arm 决定工具集（见 ab_tools.ARMS）。
    返回 {answer, input_tokens, output_tokens, steps, tool_calls, tool_texts, truncated}。"""
    _, _, mdl = load_creds() if not model else (None, None, model)
    tools = ab_tools.arm_schemas(arm)
    messages: list[dict] = [{"role": "user", "content": question}]
    in_tok = out_tok = steps = 0
    tool_calls: list[str] = []
    tool_texts: list[str] = []
    last_text = ""
    answer = ""
    truncated = False

    for _ in range(max_steps):
        resp = _create_with_retry(client, mdl, SYS_PROMPT, messages, tools)
        in_tok += getattr(resp.usage, "input_tokens", 0)
        out_tok += getattr(resp.usage, "output_tokens", 0)
        steps += 1
        messages.append({"role": "assistant", "content": resp.content})

        turn_text = "".join(b.text for b in resp.content if getattr(b, "type", "") == "text")
        if turn_text.strip():
            last_text = turn_text

        if resp.stop_reason == "tool_use":
            results = []
            for block in resp.content:
                if getattr(block, "type", "") == "tool_use":
                    result = _exec_tool(block.name, dict(block.input))
                    tool_calls.append(block.name)
                    tool_texts.append(str(result))
                    results.append({"type": "tool_result", "tool_use_id": block.id, "content": result})
            messages.append({"role": "user", "content": results})
        else:  # end_turn → 取本轮 text 作答
            answer = turn_text
            break
    else:
        truncated = True
        answer = last_text or "(max_steps reached without final answer)"

    return {
        "answer": answer.strip(), "input_tokens": in_tok, "output_tokens": out_tok,
        "steps": steps, "tool_calls": tool_calls, "tool_texts": tool_texts,
        "truncated": truncated,
    }

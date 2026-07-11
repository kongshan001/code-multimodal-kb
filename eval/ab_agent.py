"""Stage 1 agent A/B harness（task 6.3 实施）：可控 ReAct loop 测 agent 答对率 + token。

两臂（差异 = 发现工具：词面 grep vs 语义 KB，都给 read_file 保公平）：
  baseline = {grep_code, read_file}
  kb       = {cmm_search, read_file}
LLM：BigModel anthropic 兼容端点（glm-5.x），tool_use + usage 计 token。
判分：gold 符号 ∈ 终答（broad 子串，零 LLM judge）——在 run_ab_agent 里做。

凭据：env AB_API_KEY/AB_BASE_URL/AB_MODEL，否则读 ~/.cc-connect/config.toml 首个 provider。
**不写死、不入库**（repo 推 GitHub 会泄漏 key）。
"""
from __future__ import annotations

import os
import subprocess
import time
from typing import Any

import anthropic

from eval.subjects import cmm_bm25, norm_item

GODOT_CORE = "/Users/ks_128/Documents/godot-src/core"
CMM_PROJECT = "Users-ks_128-Documents-godot-src-core"
READ_CAP = 2000          # read_file 每次返回上限 chars（控 token）
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

# ── 工具执行 ──────────────────────────────────────────────────────────────

def tool_grep_code(pattern: str) -> str:
    """grep -rli <pattern>（大小写不敏感），返 top-20 文件路径。"""
    try:
        out = subprocess.run(
            ["grep", "-rli", pattern, GODOT_CORE, "--include=*.h", "--include=*.cpp", "--include=*.hpp"],
            capture_output=True, text=True, timeout=30,
        ).stdout.strip()
        files = [ln for ln in out.splitlines() if ln][:20]
        return f"matched {len(files)} files:\n" + "\n".join(files) if files else "(no matches)"
    except Exception as e:
        return f"(grep error: {e})"


def tool_read_file(path: str) -> str:
    """读文件前 READ_CAP chars。"""
    try:
        return open(path, errors="ignore").read(READ_CAP)
    except Exception as e:
        return f"(read error: {e})"


def tool_cmm_search(query: str) -> str:
    """cmm bm25 top-5 检索，返 name/qualified_name/file。"""
    try:
        raw = [r for r in cmm_bm25(CMM_PROJECT, query, 5) if isinstance(r, dict)]
        items = [norm_item(r) for r in raw]
        lines = [f"- {it['node']}  ({it['qualified_name']})  {it['file']}" for it in items]
        return "\n".join(lines) if lines else "(no results)"
    except Exception as e:
        return f"(cmm error: {e})"


DOC_GRAPH = "/Users/ks_128/Documents/godot-docs-subset/graphify-out/graph.json"


def tool_graphify_query(question: str) -> str:
    """graphify BFS 查 Godot 文档图（17 篇 vector/math 子集，72 节点），返文档节点。
    注意：文档图仅覆盖 vector/math 主题，其它题（crypto/http 等）无文档可查。"""
    try:
        out = subprocess.run(
            ["graphify", "query", question, "--graph", DOC_GRAPH, "--budget", "800"],
            capture_output=True, text=True, timeout=30,
        ).stdout
        nodes = [ln for ln in out.splitlines() if ln.startswith("NODE ")]
        edges = [ln for ln in out.splitlines() if ln.startswith("EDGE ")][:4]
        return "\n".join(nodes[:10] + edges) if nodes else "(no doc nodes — 文档图未覆盖该主题)"
    except Exception as e:
        return f"(graphify error: {e})"


_TOOL_EXEC = {"grep_code": tool_grep_code, "read_file": tool_read_file,
              "cmm_search": tool_cmm_search, "graphify_query": tool_graphify_query}

# ── 工具 schema（按臂组合）──────────────────────────────────────────────

_READ_DEF = {
    "name": "read_file", "description": "读取 Godot core/ 下某文件的前若干字符",
    "input_schema": {"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]},
}
_GREP_DEF = {
    "name": "grep_code", "description": "在 Godot core/ 源码里 grep 一个模式，返回匹配文件路径列表",
    "input_schema": {"type": "object", "properties": {"pattern": {"type": "string"}}, "required": ["pattern"]},
}
_CMM_DEF = {
    "name": "cmm_search", "description": "用代码知识库（cmm）语义检索 Godot core/，返回相关符号/函数/类",
    "input_schema": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]},
}
_GRAPHIFY_DEF = {
    "name": "graphify_query", "description": "查 Godot 文档知识图（vector/math 文档子集），返回相关文档节点/概念（文档→代码定位的语义起点）",
    "input_schema": {"type": "object", "properties": {"question": {"type": "string"}}, "required": ["question"]},
}

ARM_TOOLS = {
    "baseline": [_GREP_DEF, _READ_DEF],
    "kb": [_CMM_DEF, _READ_DEF],
    "doc": [_GRAPHIFY_DEF, _READ_DEF],
}


def _exec_tool(name: str, inputs: dict) -> str:
    fn = _TOOL_EXEC.get(name)
    return fn(**inputs) if fn else f"(unknown tool: {name})"


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
    """跑一次 agent episode。返回 {answer, input_tokens, output_tokens, steps, tool_calls,
    tool_texts, truncated}。tool_texts 收集所有工具返回（供 retrieval-aware 判分）。"""
    _, _, mdl = load_creds() if not model else (None, None, model)
    tools = ARM_TOOLS[arm]
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

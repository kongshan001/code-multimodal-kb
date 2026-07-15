"""A/B 工具注册表（task 6.x）：把 agent 工具集中成注册表，臂（arm）变数据。

**设计**：工具 = executor（包 CLI/API）+ schema。注册进 TOOL_REGISTRY。
臂 = 一组工具名（ARMS dict，数据）。run_episode 按臂名 → 工具名 → (exec,schema) 解析。

**接新 KB 工具**（换/加代码 KB、文档 KB 等）：
  1. 写一个 executor 函数（包它的 CLI/API，~5 行）
  2. 写一个 schema dict（name/description/input_schema）
  3. register_tool(name, exec, schema)         ← 注册 1 行
  4. 在 ARMS 里挂臂：ARMS["newarm"] = ["newtool", "read_file"]   ← 数据，不改 loop
然后 `bench run ab-agent --arms newarm` 直接出对照。
**agent loop / 判分 / 归档 / CLI / token 计数 全不改。**

注：executor 必须是代码（无法纯配置——它调外部 CLI/API）；本注册表让"哪些工具组成哪个臂"
完全数据化，新工具接入成本从"改 3 处"降到"写 1 个 executor + 注册 + 挂臂"。
换代码库：换 target（run_episode 经 set_active 把当前 target 的 cmm/codegraph/doc 路径
注入 _active，executor 读 _active，不再硬编码）。
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from eval._subproc import run_text
from eval.subjects import cmm_bm25, norm_item
from eval.targets import load_target
from eval import config

# ── 被测目标：运行时由 run_episode 经 set_active 注入（不再硬编码 godot-core）───
# 历史 bug：模块级 load_target("godot-core") 导致 cmm/grep/codegraph 臂永远查 godot-core，
# 跟 agent-compare 实际跑的 target 无关。现改为 _active + set_active，由 runner 注入。
_active = {"codegraph_root": "", "cmm_project": "", "doc_graph": ""}


def set_active(target_cfg: dict | None) -> None:
    """runner 在跑 episode 前注入当前 target 的路径（cmm_project / codegraph_root / doc_graph）。
    臂 executor 读 _active，不再硬编码具体 target。target_cfg=None → 清空（仅 mock/测试用）。"""
    if not target_cfg:
        _active.update({"codegraph_root": "", "cmm_project": "", "doc_graph": ""})
        return
    code = target_cfg.get("code", {}) or {}
    doc = target_cfg.get("doc", {}) or {}
    _active["codegraph_root"] = code.get("codegraph_root", "")
    _active["cmm_project"] = code.get("cmm_project", "")
    _active["doc_graph"] = doc.get("graph", "")


@dataclass
class ToolSpec:
    exec_fn: Callable[..., str]
    schema: dict


# ── 工具 executor（每个包一个被测工具的 CLI/API）────────────────────────
def grep_code(pattern: str) -> str:
    """朴素 grep -rli（baseline 臂）：返 top-20 文件路径。grep 当前 target 的 codegraph_root。"""
    root = _active["codegraph_root"]
    try:
        out = run_text(
            ["grep", "-rli", pattern, root, "--include=*.h", "--include=*.cpp", "--include=*.hpp"],
            timeout=30,
        ).stdout.strip()
        files = [ln for ln in out.splitlines() if ln][:20]
        return f"matched {len(files)} files:\n" + "\n".join(files) if files else "(no matches)"
    except Exception as e:
        return f"(grep error: {e})"


def read_file(path: str) -> str:
    """读文件前 READ_CAP chars（两臂共有，保公平）。"""
    try:
        return open(path, errors="ignore").read(config.agent()["read_cap"])
    except Exception as e:
        return f"(read error: {e})"


def cmm_search(query: str) -> str:
    """cmm bm25 top-5（kb 臂）：查当前 target 的 cmm_project，返符号 name/qualified_name/file。"""
    try:
        raw = [r for r in cmm_bm25(_active["cmm_project"], query, 5) if isinstance(r, dict)]
        items = [norm_item(r) for r in raw]
        lines = [f"- {it['node']}  ({it['qualified_name']})  {it['file']}" for it in items]
        return "\n".join(lines) if lines else "(no results)"
    except Exception as e:
        return f"(cmm error: {e})"


def graphify_query(question: str) -> str:
    """graphify BFS 查文档图（doc 臂）：查当前 target 的 doc_graph。"""
    try:
        out = run_text(
            ["graphify", "query", question, "--graph", _active["doc_graph"], "--budget", "800"],
            timeout=30,
        ).stdout
        nodes = [ln for ln in out.splitlines() if ln.startswith("NODE ")]
        edges = [ln for ln in out.splitlines() if ln.startswith("EDGE ")][:4]
        return "\n".join(nodes[:10] + edges) if nodes else "(no doc nodes — 文档图未覆盖该主题)"
    except Exception as e:
        return f"(graphify error: {e})"


def codegraph_search(query: str) -> str:
    """codegraph 符号检索（codegraph 臂）：查当前 target 的 codegraph_root。需先 codegraph init。"""
    try:
        out = run_text(
            ["codegraph", "query", query, "--path", _active["codegraph_root"], "--limit", "5", "--json"],
            timeout=30,
        ).stdout
        data = json.loads(out) if out.strip() else []
        items = data if isinstance(data, list) else (data.get("results") or data.get("symbols") or [])
        lines = []
        for it in (items or [])[:5]:
            n = it.get("node", it) if isinstance(it, dict) else {}   # 结果项可能包在 "node" 里
            name = n.get("name") or n.get("qualifiedName") or "?"
            kind = n.get("kind", "")
            loc = n.get("filePath") or n.get("file") or n.get("file_path") or ""
            lines.append(f"- {name}  [{kind}]  {loc}")
        return "\n".join(lines) if lines else "(no codegraph results)"
    except Exception as e:
        return f"(codegraph error: {e})"


# ── 工具 schema（Anthropic tool_use 格式）───────────────────────────────
_READ_DEF = {"name": "read_file", "description": "读取 Godot core/ 下某文件的前若干字符",
             "input_schema": {"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}}
_GREP_DEF = {"name": "grep_code", "description": "在 Godot core/ 源码里 grep 一个模式，返回匹配文件路径列表",
             "input_schema": {"type": "object", "properties": {"pattern": {"type": "string"}}, "required": ["pattern"]}}
_CMM_DEF = {"name": "cmm_search", "description": "用代码知识库（cmm）语义检索 Godot core/，返回相关符号/函数/类",
            "input_schema": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}}
_GRAPHIFY_DEF = {"name": "graphify_query", "description": "查 Godot 文档知识图（vector/math 文档子集），返回相关文档节点/概念",
                 "input_schema": {"type": "object", "properties": {"question": {"type": "string"}}, "required": ["question"]}}
_CODEGRAPH_DEF = {"name": "codegraph_search", "description": "用 codegraph 知识图检索 Godot core/ 符号（函数/类/方法），返回符号名+类型+文件",
                  "input_schema": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}}


# ── 注册表 ───────────────────────────────────────────────────────────────
TOOL_REGISTRY: dict[str, ToolSpec] = {}


def register_tool(name: str, exec_fn: Callable[..., str], schema: dict) -> None:
    """注册一个工具（executor + schema）。新工具调用此函数即可。"""
    TOOL_REGISTRY[name] = ToolSpec(exec_fn=exec_fn, schema=schema)


# 注册内置工具
register_tool("grep_code", grep_code, _GREP_DEF)
register_tool("read_file", read_file, _READ_DEF)
register_tool("cmm_search", cmm_search, _CMM_DEF)
register_tool("graphify_query", graphify_query, _GRAPHIFY_DEF)
register_tool("codegraph_search", codegraph_search, _CODEGRAPH_DEF)


# ── 臂（数据：工具集 + skills 注入）──────────────────────────────────────
# agent-compare 4 臂 = {KB on/off} × {skills}；旧臂名保留兼容（ab-agent 旧入口）
ARMS: dict[str, dict] = {
    # 新 4 臂（add-bench-agent-compare）
    "no-kb":          {"tools": ["grep_code", "read_file"], "skills": []},
    "kb":             {"tools": ["cmm_search", "read_file"], "skills": []},
    "kb+superpowers": {"tools": ["cmm_search", "read_file"], "skills": ["superpowers"]},
    "kb+openspec":    {"tools": ["cmm_search", "read_file"], "skills": ["openspec"]},
    # 旧臂名兼容（保原工具行为，无 skills 注入）
    "baseline":  {"tools": ["grep_code", "read_file"], "skills": []},
    "doc":       {"tools": ["graphify_query", "read_file"], "skills": []},
    "codegraph": {"tools": ["codegraph_search", "read_file"], "skills": []},
}

_SKILLS_DIR = Path(__file__).resolve().parent / "arms" / "skills_bundled"


def arm_schemas(arm: str) -> list[dict]:
    """臂名 → 该臂的工具 schema 列表（喂给 LLM tool_use）。"""
    return [TOOL_REGISTRY[n].schema for n in ARMS[arm]["tools"]]


def arm_skills(arm: str) -> list[str]:
    """臂名 → 注入的 skill 名列表。"""
    return ARMS[arm].get("skills", [])


def load_skill_content(name: str) -> str:
    """读 bundled skill 精简 SOP 文本（eval/arms/skills_bundled/<name>.md）。无则空串。"""
    f = _SKILLS_DIR / f"{name}.md"
    return f.read_text(encoding="utf-8") if f.is_file() else ""


def arm_config(arm: str) -> dict:
    """臂名 → 完整配置（工具 + skills + 各 skill 的 SOP 文本），供报告 config.md 用。"""
    skills = arm_skills(arm)
    return {
        "tools": ARMS[arm]["tools"],
        "skills": skills,
        "skill_contents": {s: load_skill_content(s) for s in skills},
    }


def exec_tool(name: str, inputs: dict) -> str:
    """按工具名执行（run_episode 调）。"""
    return TOOL_REGISTRY[name].exec_fn(**inputs)


def arm_names() -> list[str]:
    return list(ARMS)


# ── SDK MCP 层（openspec migrate-ab-agent-to-claude-sdk）─────────────────
# 注册表（TOOL_REGISTRY）仍是唯一真相；本层把它的 (exec_fn, schema) 包成
# claude_agent_sdk 的 in-process MCP tool，供 query() 用。executor 与 set_active 零改
#（工具在进程内执行，_active 仍生效）。bare 工具名经 mcp__bench__ 前缀暴露给模型。


def mcp_tool(name: str, sink: list | None = None):
    """从注册表项造一个 claude_agent_sdk @tool 对象（async，返 MCP content 形状）。
    sink 非空时，每次调用把 (name, result) append 进 sink——run_episode 用来捕 tool_texts
    （tool_calls 另从消息流的 tool_use block 取，二者在真跑时等长）。"""
    from claude_agent_sdk import tool as _tool
    spec = TOOL_REGISTRY[name]
    exec_fn, schema = spec.exec_fn, spec.schema

    async def _wrapper(args):
        result = str(exec_fn(**args))
        if sink is not None:
            sink.append((name, result))
        return {"content": [{"type": "text", "text": result}]}

    _wrapper.__name__ = f"{name}_tool"
    # @tool 接受完整 JSON schema dict（已验），直接复用 _X_DEF["input_schema"]
    return _tool(name, schema["description"], schema["input_schema"])(_wrapper)


def arm_mcp_server(arm: str, sink: list | None = None):
    """臂 → in-process MCP server 配置（dict，喂 ClaudeAgentOptions.mcp_servers）。
    只含该臂声明工具（保臂隔离）。sink 透传给每个 tool 捕结果。"""
    from claude_agent_sdk import create_sdk_mcp_server
    tools = [mcp_tool(n, sink) for n in ARMS[arm]["tools"]]
    return create_sdk_mcp_server("bench", tools=tools)


def arm_allowed_tools(arm: str) -> list[str]:
    """臂 → allowed_tools 名（mcp__bench__<bare>）。ARMS 仍存 bare 名，前缀在此派生。"""
    return [f"mcp__bench__{n}" for n in ARMS[arm]["tools"]]

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
换代码库：改下面的 GODOT_CORE / CMM_PROJECT / DOC_GRAPH 常量。
"""
from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass
from typing import Callable

from eval.subjects import cmm_bm25, norm_item

# ── 代码库 / 索引目标（换代码库改这里）──────────────────────────────────
GODOT_CORE = "/Users/ks_128/Documents/godot-src/core"
CMM_PROJECT = "Users-ks-128-Documents-godot-src-core"
DOC_GRAPH = "/Users/ks_128/Documents/godot-docs-subset/graphify-out/graph.json"
READ_CAP = 2000


@dataclass
class ToolSpec:
    exec_fn: Callable[..., str]
    schema: dict


# ── 工具 executor（每个包一个被测工具的 CLI/API）────────────────────────
def grep_code(pattern: str) -> str:
    """朴素 grep -rli（baseline 臂）：返 top-20 文件路径。"""
    try:
        out = subprocess.run(
            ["grep", "-rli", pattern, GODOT_CORE, "--include=*.h", "--include=*.cpp", "--include=*.hpp"],
            capture_output=True, text=True, timeout=30,
        ).stdout.strip()
        files = [ln for ln in out.splitlines() if ln][:20]
        return f"matched {len(files)} files:\n" + "\n".join(files) if files else "(no matches)"
    except Exception as e:
        return f"(grep error: {e})"


def read_file(path: str) -> str:
    """读文件前 READ_CAP chars（两臂共有，保公平）。"""
    try:
        return open(path, errors="ignore").read(READ_CAP)
    except Exception as e:
        return f"(read error: {e})"


def cmm_search(query: str) -> str:
    """cmm bm25 top-5（kb 臂）：返符号 name/qualified_name/file。"""
    try:
        raw = [r for r in cmm_bm25(CMM_PROJECT, query, 5) if isinstance(r, dict)]
        items = [norm_item(r) for r in raw]
        lines = [f"- {it['node']}  ({it['qualified_name']})  {it['file']}" for it in items]
        return "\n".join(lines) if lines else "(no results)"
    except Exception as e:
        return f"(cmm error: {e})"


def graphify_query(question: str) -> str:
    """graphify BFS 查文档图（doc 臂）：返文档概念节点（仅 vector/math 子集覆盖的主题）。"""
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


def codegraph_search(query: str) -> str:
    """codegraph 符号检索（codegraph 臂）：返 name/kind/file。
    需先在 GODOT_CORE 跑 `codegraph init` 建索引。JSON 输出。"""
    try:
        out = subprocess.run(
            ["codegraph", "query", query, "--path", GODOT_CORE, "--limit", "5", "--json"],
            capture_output=True, text=True, timeout=30,
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


# ── 臂（数据：哪些工具组成哪个臂）────────────────────────────────────────
ARMS: dict[str, list[str]] = {
    "baseline": ["grep_code", "read_file"],
    "kb": ["cmm_search", "read_file"],
    "doc": ["graphify_query", "read_file"],
    "codegraph": ["codegraph_search", "read_file"],
}


def arm_schemas(arm: str) -> list[dict]:
    """臂名 → 该臂的工具 schema 列表（喂给 LLM tool_use）。"""
    return [TOOL_REGISTRY[n].schema for n in ARMS[arm]]


def exec_tool(name: str, inputs: dict) -> str:
    """按工具名执行（run_episode 调）。"""
    return TOOL_REGISTRY[name].exec_fn(**inputs)


def arm_names() -> list[str]:
    return list(ARMS)

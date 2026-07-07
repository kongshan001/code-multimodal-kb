"""Subject 适配器：调用被测工具。task 1.1 目标 = cmm round-trip。

harness 是独立 pytest 进程，不走 agent MCP，改走 cmm CLI（与 deployment-runbook 一致）。
三路检索：grep(search_code) / BM25(search_graph query) / semantic(search_graph semantic_query)。
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
from typing import Any

CMM_BIN = (
    os.environ.get("CMM_BIN")
    or shutil.which("codebase-memory-mcp")
    or os.path.expanduser("~/.local/bin/codebase-memory-mcp")
)


def _cli(tool: str, args: dict) -> Any:
    proc = subprocess.run(
        [CMM_BIN, "cli", tool, json.dumps(args)],
        capture_output=True, text=True, timeout=120,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"cmm cli {tool} 失败 (rc={proc.returncode}): {proc.stderr.strip()}")
    out = proc.stdout.strip()
    i = out.find("{")  # 防御：stdout 混入 log 时跳到首个 JSON 对象
    return json.loads(out[i:]) if i >= 0 else json.loads(out)


def cmm_available() -> bool:
    try:
        cmm_list_projects()
        return True
    except Exception:
        return False


def cmm_list_projects() -> list[dict]:
    return _cli("list_projects", {}).get("projects", [])


# ── 三路检索 ──

def cmm_search(project: str, pattern: str, limit: int = 10) -> list[dict]:
    """grep + 图排序（search_code）。结果项：node / file。"""
    res = _cli("search_code", {"project": project, "pattern": pattern, "limit": limit})
    return res.get("results", res) if isinstance(res, dict) else res


def cmm_bm25(project: str, query: str, limit: int = 10) -> list[dict]:
    """BM25 NL 检索（search_graph query=）。结果项：name / file_path。"""
    res = _cli("search_graph", {"project": project, "query": query, "limit": limit})
    return res.get("results", []) if isinstance(res, dict) else res


def cmm_semantic(project: str, keywords: list[str], limit: int = 10) -> list[dict]:
    """语义向量检索（search_graph semantic_query=，需 moderate/full 索引）。
    返回 semantic_results（cosine 排序）。结果项：name / file_path / score。"""
    res = _cli("search_graph", {"project": project, "semantic_query": list(keywords), "limit": limit})
    if not isinstance(res, dict):
        return res
    return res.get("semantic_results", [])  # 注：res["results"] 是 $id/$schema 默认噪声，不用


def norm_item(r: dict) -> dict:
    """归一化不同接口的结果项：node|name → node；file|file_path → file。"""
    return {
        "node": r.get("node") or r.get("name", ""),
        "qualified_name": r.get("qualified_name", ""),
        "file": r.get("file") or r.get("file_path", ""),
    }


def cmm_call_chain(project: str, function_name: str) -> dict:
    """调用链（task 2.3 Call-Chain Edge Recall 的结果来源）。"""
    return _cli("trace_path", {"project": project, "function_name": function_name})

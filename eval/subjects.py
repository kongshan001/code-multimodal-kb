"""Subject 适配器：调用被测工具。task 1.1 目标 = cmm round-trip。

harness 是独立 pytest 进程，不走 agent MCP，改走 cmm CLI（与 deployment-runbook 一致）。
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


def cmm_search(project: str, pattern: str, limit: int = 10) -> list[dict]:
    """符号检索（task 2.2 NL→符号定位的主接口）。"""
    res = _cli("search_code", {"project": project, "pattern": pattern, "limit": limit})
    return res.get("results", res) if isinstance(res, dict) else res


def cmm_call_chain(project: str, function_name: str) -> dict:
    """调用链（task 2.3 Call-Chain Edge Recall 的结果来源）。"""
    return _cli("trace_path", {"project": project, "function_name": function_name})

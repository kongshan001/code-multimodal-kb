"""MemPalace 适配器（task 4.2）：调 mempalace CLI search，解析文本输出。

harness 是独立进程，不走 agent MCP，改走 mempalace CLI（与 cmm adapter 模式一致，
见 subjects.py）。mempalace search 无 --json，输出人类可读表格 → 这里 regex 解析，
解析器单测（test_mempalace_parser）用录样锁格式，mempalace 改输出会先在测试暴露。
"""
from __future__ import annotations

import os
import re
import shutil
import subprocess
from typing import Any

MEMPALACE_BIN = (
    os.environ.get("MEMPALACE_BIN")
    or shutil.which("mempalace")
    or os.path.expanduser("~/.local/bin/mempalace")
)

# 结果块头：  [1] wing_api / technical
_HEADER = re.compile(r"^\s*\[(\d+)\]\s+(\S+)\s*/\s*(\S+)\s*$", re.MULTILINE)
_SOURCE = re.compile(r"Source:\s*(.+?)\s*$", re.MULTILINE)
_MATCH = re.compile(r"cosine_sim=([-\d.]+)\s+bm25=([-\d.]+)")


def parse_search_output(text: str) -> list[dict]:
    """把 mempalace search 的文本输出解析成结构化结果列表。

    每项：{rank, wing, room, source_file, cosine_sim, bm25_score, text}。
    无结果（无 [N] 头）→ []。
    """
    if not text:
        return []
    headers = list(_HEADER.finditer(text))
    if not headers:
        return []
    out = []
    for i, h in enumerate(headers):
        block = text[h.end():headers[i + 1].start()] if i + 1 < len(headers) else text[h.end():]
        sm = _SOURCE.search(block)
        mm = _MATCH.search(block)
        # 文本片段：Source/Match 行之后的非空行，去前导缩进
        snippet_lines = []
        for ln in block.splitlines():
            stripped = ln.strip()
            if not stripped:
                continue
            if stripped.startswith("Source:") or stripped.startswith("Match:"):
                continue
            snippet_lines.append(stripped)
        out.append({
            "rank": int(h.group(1)),
            "wing": h.group(2),
            "room": h.group(3),
            "source_file": (sm.group(1).strip() if sm else ""),
            "cosine_sim": (float(mm.group(1)) if mm else 0.0),
            "bm25_score": (float(mm.group(2)) if mm else 0.0),
            "text": " ".join(snippet_lines)[:200],
        })
    return out


def _run(query: str, results: int, wing: str | None, room: str | None) -> str:
    cmd = [MEMPALACE_BIN, "search", query, "--results", str(results)]
    if wing:
        cmd += ["--wing", wing]
    if room:
        cmd += ["--room", room]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    if proc.returncode != 0:
        raise RuntimeError(f"mempalace search 失败 (rc={proc.returncode}): {proc.stderr.strip()[:200]}")
    return proc.stdout


def mempalace_search(query: str, limit: int = 10, wing: str | None = None,
                     room: str | None = None) -> list[dict]:
    """调 mempalace search → 解析 → 返回结构化结果项列表。"""
    return parse_search_output(_run(query, limit, wing, room))


def mempalace_available() -> bool:
    try:
        subprocess.run([MEMPALACE_BIN, "--version"], capture_output=True, text=True, timeout=15)
        return True
    except Exception:
        return False


def norm_source(it: dict) -> str:
    """归一化结果项的 source_file（取 basename，去路径）。"""
    sf = it.get("source_file", "") or ""
    return os.path.basename(sf) or sf

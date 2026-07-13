"""子进程 UTF-8 helper：跨平台强制 UTF-8 解码 stdout/stderr。

Windows 中文系统默认用 cp936(GBK) 解码子进程输出；工具输出里的非 ASCII 字节（中文
memory drawer / 代码符号路径 / emoji ✓⚠）会触发 UnicodeDecodeError → reader 线程崩
→ .stdout=None → 后续 .strip()/.splitlines() AttributeError。统一 UTF-8 + errors=replace。

全仓 subprocess.run(capture_output=True, text=True, ...) 一律走 run_text，集中编码处理。
"""
from __future__ import annotations

import subprocess


def run_text(cmd: list[str], timeout: float = 120, cwd: str | None = None) -> subprocess.CompletedProcess:
    """跑 cmd，capture stdout/stderr，强制 UTF-8 解码。返 CompletedProcess。"""
    return subprocess.run(
        cmd, capture_output=True, text=True,
        encoding="utf-8", errors="replace", timeout=timeout, cwd=cwd,
    )

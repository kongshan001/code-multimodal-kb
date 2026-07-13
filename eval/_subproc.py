"""子进程 helper：跨平台 UTF-8 解码 + Windows 可执行文件解析。

两个 Windows 坑（中文 Windows 尤甚）：
  1. cp936(GBK) 解码非 ASCII 字节（中文 memory drawer / 符号路径 / emoji）→ reader 线程
     崩 → .stdout=None → 后续 .strip() AttributeError。
  2. npm/uv 装的 CLI（codegraph/openspec/graphify/mempalace）是无扩展名 POSIX shell
     脚本 + .cmd 包装器并存；CreateProcess 跑不了无扩展名那个，shutil.which 还可能
     把它返回。需优先找同目录的 .cmd/.bat/.exe 包装器。

全仓 subprocess 一律走 run_text，集中处理。
"""
from __future__ import annotations

import os
import shutil
import subprocess

# Windows 上 CreateProcess 能直接跑的扩展名（按优先序）。无扩展名的 POSIX 脚本不算。
_WIN_EXTS = (".cmd", ".CMD", ".bat", ".BAT", ".exe", ".EXE")


def _resolve_exe(name: str) -> str:
    """把 CLI 名解析成 CreateProcess 能直接跑的可执行路径。

    Unix：shutil.which 透传（已有扩展名 / 在 PATH 里）。
    Windows：shutil.which 可能返回无扩展名的 POSIX 脚本 → 优先返回同目录的 .cmd/.bat/.exe
    包装器；都没有就退回原名（让 subprocess 报原错，便于诊断）。
    """
    resolved = shutil.which(name)
    if not resolved:
        return name
    if os.name == "nt" and not os.path.splitext(resolved)[1]:
        for ext in _WIN_EXTS:
            alt = resolved + ext
            if os.path.isfile(alt):
                return alt
    return resolved


def run_text(cmd: list[str], timeout: float = 120, cwd: str | None = None) -> subprocess.CompletedProcess:
    """跑 cmd，capture stdout/stderr，强制 UTF-8 解码 + Windows exe 解析。返 CompletedProcess。"""
    return subprocess.run(
        [_resolve_exe(cmd[0]), *cmd[1:]], capture_output=True, text=True,
        encoding="utf-8", errors="replace", timeout=timeout, cwd=cwd,
    )

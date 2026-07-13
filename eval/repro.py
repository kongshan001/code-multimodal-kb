"""可复现 lockfile（task 1.2）：把锁定的 temp/模型/工具版本盖到评测报告。

graphify/Mem0 抽取非确定（LLM 生成），跨设备/跨时间可比必须先锁这三项；
代码侧结构指标天然确定，不受此约束，但版本号仍记录便于追溯。
"""
from __future__ import annotations

from dataclasses import asdict, dataclass

from eval._subproc import run_text


@dataclass
class Lockfile:
    temperature: float = 0.0
    llm_model: str = ""        # 用到 LLM 的 subject（文档侧/记忆侧）才填
    cmm_version: str = ""
    graphify_version: str = ""
    mem0_version: str = ""     # 遗留：Mem0 路线已弃用，保留字段兼容旧报告
    mempalace_version: str = ""  # 记忆侧 subject（task 4.2）

    def to_dict(self) -> dict:
        return asdict(self)


def _version(bin_cmd: list[str]) -> str:
    try:
        out = run_text(bin_cmd, timeout=10)
        if out.returncode == 0:
            return out.stdout.strip().split()[-1] or "unknown"
    except Exception:
        pass
    return "unknown"


def detect_lockfile() -> Lockfile:
    """探测本机已装工具版本。未装的记 unknown。"""
    import shutil
    cmm = shutil.which("codebase-memory-mcp") or ""
    graphify = shutil.which("graphify") or ""
    mempalace = shutil.which("mempalace") or ""
    return Lockfile(
        cmm_version=_version([cmm, "--version"]) if cmm else "not-installed",
        graphify_version=_version([graphify, "--version"]) if graphify else "not-installed",
        mempalace_version=_version([mempalace, "--version"]) if mempalace else "not-installed",
    )


def stamp(report: dict, lock: Lockfile) -> dict:
    """把 lockfile 盖进评测报告（满足 spec：报告附锁定项清单）。"""
    report = dict(report)
    report["lockfile"] = lock.to_dict()
    return report

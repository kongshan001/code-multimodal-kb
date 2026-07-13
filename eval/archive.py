"""报告归档层（task 1.1 / 1.2）：统一 schema + 不覆盖留底 + index 清单。

每次 `bench run` 调 `archive_report()` → 写 `reports/archive/<ts>-<subject>-<variant>.json`
（不覆盖）+ 追加 `archive/index.json`。ts 用 UTC ISO8601 基本格式（跨时区可比、
文件名安全）；index 同时记本地可读时间。

设计见 openspec/changes/add-benchmark-runner/design.md 决策 2 / 3。
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from eval.repro import detect_lockfile, stamp

# eval/reports/archive/
ARCHIVE_DIR = Path(__file__).resolve().parent / "reports" / "archive"
INDEX_PATH = ARCHIVE_DIR / "index.json"
# 仓库根（archive_meta.path 相对此根，可移植）
_REPO_ROOT = Path(__file__).resolve().parent.parent


def _utc_ts() -> tuple[str, str]:
    """返回 (紧凑 UTC ts, 本地可读 ts 带时区偏移)。"""
    now_utc = datetime.now(timezone.utc)
    compact = now_utc.strftime("%Y%m%dT%H%M%SZ")
    readable = now_utc.astimezone().strftime("%Y-%m-%d %H:%M:%S %z")
    return compact, readable


def normalize_report(report: dict, subject: str | None = None, variant: str = "") -> dict:
    """把各 subject 的 run() 输出规范成统一 schema。

    统一顶层：subject / variant / target / n / aggregate / per_query / lockfile。
    - 缺 lockfile 的（doc / cross）补 detect_lockfile() + stamp
    - cross-tool 无 aggregate：把顶层 *_rate / *@5 字段聚成 aggregate
    """
    r = dict(report)
    subj = subject or r.get("subject", "unknown")
    target = r.get("target") or r.get("graph", "")

    if "aggregate" not in r:
        # cross-tool：把顶层 *_rate / *@5 聚成 aggregate
        agg = {k: r[k] for k in list(r) if k.endswith("_rate") or k.endswith("@5")}
    else:
        agg = r["aggregate"]

    if "lockfile" not in r:
        r = stamp(r, detect_lockfile())

    return {
        "subject": subj,
        "variant": variant,
        "target": target,
        "n": r.get("n", 0),
        "aggregate": agg,
        "per_query": r.get("per_query", []),
        "lockfile": r.get("lockfile", {}),
    }


def _safe_name(s: str) -> str:
    return s.replace("/", "-").replace(" ", "-").replace(":", "-")


def _unique_path(subject: str, variant: str, ts: str) -> Path:
    """生成不冲突的归档路径；秒级同 ts 加 -2/-3 后缀（不覆盖语义）。"""
    base = f"{ts}-{_safe_name(subject)}-{_safe_name(variant or 'default')}"
    cand = ARCHIVE_DIR / f"{base}.json"
    i = 2
    while cand.exists():
        cand = ARCHIVE_DIR / f"{base}-{i}.json"
        i += 1
    return cand


def archive_report(report: dict, subject: str | None = None, variant: str = "") -> dict:
    """归档报告（不覆盖）+ 更新 index。返回 {id, path, ts}。"""
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    norm = normalize_report(report, subject, variant)
    ts, readable = _utc_ts()
    path = _unique_path(norm["subject"], norm["variant"], ts)
    rid = path.stem

    rel_path = str(path.relative_to(_REPO_ROOT))
    norm["archive_meta"] = {
        "id": rid,
        "ts": ts,
        "readable_ts": readable,
        "path": rel_path,
    }
    path.write_text(json.dumps(norm, ensure_ascii=False, indent=2), encoding="utf-8")

    entry = {
        "id": rid,
        "ts": ts,
        "readable_ts": readable,
        "subject": norm["subject"],
        "variant": norm["variant"],
        "target": norm["target"],
        "n": norm["n"],
        "lockfile": norm["lockfile"],
        "aggregate": norm["aggregate"],
        "path": rel_path,
    }
    index = _load_index()
    index["reports"].append(entry)
    _save_index(index)

    return {"id": rid, "path": rel_path, "ts": ts}


def _load_index() -> dict:
    if INDEX_PATH.exists():
        return json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    return {"reports": []}


def _save_index(index: dict) -> None:
    INDEX_PATH.write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")


def list_reports() -> list[dict]:
    return _load_index().get("reports", [])


def get_report(rid: str) -> dict | None:
    """按 id 读归档 JSON。"""
    for entry in list_reports():
        if entry["id"] == rid:
            p = _REPO_ROOT / entry["path"]
            if p.exists():
                return json.loads(p.read_text(encoding="utf-8"))
    return None


def compare_reports(rid1: str, rid2: str) -> dict | None:
    """仅 aggregate 对比（design OQ1）。返回 {left, right, diff}。"""
    r1, r2 = get_report(rid1), get_report(rid2)
    if r1 is None or r2 is None:
        return None
    keys = sorted(set(r1["aggregate"]) | set(r2["aggregate"]))
    diff = []
    for k in keys:
        a, b = r1["aggregate"].get(k), r2["aggregate"].get(k)
        delta = (b - a) if (isinstance(a, (int, float)) and isinstance(b, (int, float))) else None
        diff.append({"metric": k, "left": a, "right": b, "delta": delta})
    return {"left": rid1, "right": rid2, "diff": diff}

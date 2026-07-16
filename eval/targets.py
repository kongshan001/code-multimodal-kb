"""Per-target loader：target.json（本地配置）+ problems.json（gold 题库）。

零依赖（stdlib json）。题库与目标工程绑定从 Python 源码（gold_*.py）迁到声明式 JSON。

目录布局（eval/targets/<id>/）：
  target.json          工程描述（id/language/subjects/工具路径/依赖），gitignored 本地配置
                       （含机器路径；由 target.json.example 复制而来，各自本地改不冲突）
  target.json.example  模板（入库），cp 为 target.json 后填本机路径
  problems.json        题库（gold，type 判别 + 稳定 id + 元数据），提交

5 种 problem type，gold 形状由 type 决定（discriminated union，见 _GOLD_FIELDS）。
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parent.parent
TARGETS_DIR = REPO / "eval" / "targets"

# problem type → gold 必须含的字段集合（gold 形状由 type 决定）
_GOLD_FIELDS: dict[str, set[str]] = {
    "code_retrieval": {"symbols"},
    "doc_retrieval": {"node_labels"},
    "cross_anchor": {"doc_node_label", "cmm_identifier", "code_file"},
    "memory_recall": {"source_files"},
    "memory_routing": {"layer"},
    "bug_fix": {"symbols", "files"},
}

# memory_routing 的 layer 取值（D1 四层归属）
_ROUTING_LAYERS = {"objective", "procedural", "episodic", "subjective"}

_VALID_STATUS = {"pending", "accepted"}

# 列表型 gold 字段（值须为非空 list[str]）
_LIST_GOLD = {"symbols", "node_labels", "source_files", "files"}


class TargetError(Exception):
    """target/problems 加载或校验失败。"""


# ── target 加载 ───────────────────────────────────────────────────────────
def _target_dir(target_id: str) -> Path:
    d = TARGETS_DIR / target_id
    if not d.is_dir():
        raise TargetError(f"target 不存在: {target_id}（找不到 {d}）")
    return d


def load_target_raw(target_id: str) -> dict:
    """读 target.json（不含 local overlay，不含 deps 解析）。供 deps 解析递归用。"""
    f = _target_dir(target_id) / "target.json"
    if not f.is_file():
        raise TargetError(f"target {target_id} 缺 target.json")
    return json.loads(f.read_text(encoding="utf-8"))


def load_target(target_id: str) -> dict:
    """读 target.json（本地配置）。

    cross target（含 deps）额外校验依赖 target 存在，并在返回里附 `deps_resolved`：
    {dep_role: 该依赖 target 的 merged 配置}，使 runner 无感取 doc_graph/cmm 路径。
    """
    base = load_target_raw(target_id)
    # deps 解析（cross_anchor）
    deps = base.get("deps")
    if deps:
        if not isinstance(deps, dict) or not deps:
            raise TargetError(f"target {target_id} 的 deps 须为非空 object")
        resolved: dict[str, dict] = {}
        for role, dep_id in deps.items():
            if not isinstance(dep_id, str):
                raise TargetError(f"target {target_id} deps.{role} 须为 target id 字符串")
            dep_dir = TARGETS_DIR / dep_id
            if not dep_dir.is_dir():
                raise TargetError(
                    f"target {target_id} 声明 deps.{role}={dep_id}，但该 target 不存在")
            resolved[role] = load_target(dep_id)  # 递归（含该 dep 自己的 local overlay）
        base["deps_resolved"] = resolved
    return base


def list_targets() -> list[str]:
    """列全部 target id（eval/targets/ 下含 target.json 的子目录）。"""
    if not TARGETS_DIR.is_dir():
        return []
    return sorted(
        d.name for d in TARGETS_DIR.iterdir()
        if d.is_dir() and (d / "target.json").is_file()
    )


# ── problems 加载 + schema 校验 ───────────────────────────────────────────
def _validate_problem(p: dict, target_id: str, seen_ids: set[str]) -> None:
    if not isinstance(p, dict):
        raise TargetError(f"[{target_id}] 题目须为 object，得到 {type(p).__name__}")
    pid = p.get("id")
    if not pid or not isinstance(pid, str):
        raise TargetError(f"[{target_id}] 题目缺 id 或 id 非字符串")
    if pid in seen_ids:
        raise TargetError(f"[{target_id}] 题目 id 重复: {pid}")
    seen_ids.add(pid)

    ptype = p.get("type")
    if ptype not in _GOLD_FIELDS:
        raise TargetError(
            f"[{target_id}] 题目 {pid} type 非法: {ptype!r}（合法: {sorted(_GOLD_FIELDS)}）")

    # query vs fact：routing 用 fact，其余用 query
    text_field = "fact" if ptype == "memory_routing" else "query"
    if not p.get(text_field) or not isinstance(p.get(text_field), str):
        raise TargetError(f"[{target_id}] 题目 {pid} 缺 {text_field} 或非字符串")

    status = p.get("status")
    if status not in _VALID_STATUS:
        raise TargetError(
            f"[{target_id}] 题目 {pid} status 非法: {status!r}（合法: {sorted(_VALID_STATUS)}）")

    gold = p.get("gold")
    if not isinstance(gold, dict):
        raise TargetError(f"[{target_id}] 题目 {pid} gold 须为 object")
    required = _GOLD_FIELDS[ptype]
    for fld in required:
        if fld not in gold:
            raise TargetError(f"[{target_id}] 题目 {pid}（{ptype}）gold 缺字段: {fld}")
        v = gold[fld]
        if fld in _LIST_GOLD:
            if not isinstance(v, list) or not v or not all(isinstance(x, str) for x in v):
                raise TargetError(f"[{target_id}] 题目 {pid} gold.{fld} 须为非空 list[str]")
        else:
            if not isinstance(v, str) or not v:
                raise TargetError(f"[{target_id}] 题目 {pid} gold.{fld} 须为非空字符串")
    if ptype == "memory_routing" and gold["layer"] not in _ROUTING_LAYERS:
        raise TargetError(
            f"[{target_id}] 题目 {pid} gold.layer 非法: {gold['layer']!r}"
            f"（合法: {sorted(_ROUTING_LAYERS)}）")


def load_problems(target_id: str) -> list[dict]:
    """读 problems.json，逐题校验 schema（type↔gold、id 唯一、必填字段）。返题目列表。"""
    f = _target_dir(target_id) / "problems.json"
    if not f.is_file():
        raise TargetError(f"target {target_id} 缺 problems.json")
    data = json.loads(f.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise TargetError(f"{target_id}/problems.json 顶层须为 object")
    problems = data.get("problems")
    if not isinstance(problems, list):
        raise TargetError(f"{target_id}/problems.json 缺 problems 数组")
    seen: set[str] = set()
    for p in problems:
        _validate_problem(p, target_id, seen)
    return problems


def load(target_id: str) -> dict:
    """一站式：{target: merged 配置, problems: 校验后列表}。runner 主入口。"""
    return {"target": load_target(target_id), "problems": load_problems(target_id)}


# ── slug + 写回（goldgen / 前端编辑器共用）────────────────────────────────
_TOKEN = re.compile(r"[A-Za-z0-9一-鿿]+")


def slugify(text: str, n: int = 3) -> str:
    """text → lowercase kebab slug（前 n 个 token；CJK 连串视作一个 token）。

    稳定 id 用：<target-id>-<slug(query/fact)>。撞名由调用方加 -2/-3。
    """
    tokens = _TOKEN.findall(text.lower())
    return "-".join(tokens[:n]) or "q"


def assign_ids(target_id: str, problems: list[dict]) -> None:
    """给无 id 的题分配 <target_id>-<slug(text)>，撞名加 -2/-3。就地改 problems。

    已有 id 的题保留（幂等）。text = fact（routing）或 query（其余）。
    """
    seen: dict[str, int] = {p["id"]: 1 for p in problems if p.get("id")}
    for p in problems:
        if p.get("id"):
            continue
        text = p.get("fact") or p.get("query") or ""
        base = f"{target_id}-{slugify(text)}"
        if base in seen:
            seen[base] += 1
            pid = f"{base}-{seen[base]}"
        else:
            seen[base] = 1
            pid = base
        p["id"] = pid


def save_problems(target_id: str, problems: list[dict], *, assign: bool = True) -> list[dict]:
    """校验 + 写回 targets/<id>/problems.json。

    assign=True（默认）：先给无 id 的题分配稳定 id（goldgen 新候选用）。
    逐题校验 schema（type↔gold、id 唯一、必填字段）。校验失败抛 TargetError，不写。
    返回写回的 problems（含分配后的 id）。
    """
    if assign:
        assign_ids(target_id, problems)
    seen: set[str] = set()
    for p in problems:
        _validate_problem(p, target_id, seen)
    f = _target_dir(target_id) / "problems.json"
    f.write_text(
        json.dumps({"version": 1, "target": target_id, "problems": problems},
                   ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8")
    return problems

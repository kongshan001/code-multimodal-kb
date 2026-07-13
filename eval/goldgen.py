"""Gold 生成器：symbol-driven 挖掘 + 两层自动验收 + 人审（低成本扩题库）。

候选直接落 targets/<id>/problems.json（status: pending + provenance）。人审 = 前端逐条
approve（status→accepted）或删。**无 pending.md、无 fold、无全量重写**——所有编辑增量
作用于 problems.json 单条目（design D6）。

仅适用于 code_retrieval target（枚举代码符号造题）。root / cmm_project 从该 target 的
target.json 读（经 overlay），引擎零硬编码。

流程：
  bench goldgen <seeds> --target <id>     codegraph 枚举真实符号 + LLM 拟 NL 题
                                           （gold=符号，构造即正确，零 LLM judge）→ 写 pending 候选
  bench goldgen-verify --target <id>       实证验收（零 LLM）：在 pending 候选原地标 verdict/reason
  （主 agent spawn 独立 subagent 做语义验收；人审 approve/删 在前端）
"""
from __future__ import annotations

import json
import os
import re
import subprocess

from eval.targets import load_problems, load_target, save_problems

# 非"真符号"的节点 kind（文件/导入/目录级），枚举时滤掉
_NON_SYMBOL_KINDS = {"file", "import", "directory", "unknown", "module", "package"}


# ── 符号枚举（codegraph，零 LLM）──────────────────────────────────────────
def _run_codegraph(args: list[str], timeout: int = 30) -> str:
    """跑 codegraph 子命令，强制 UTF-8 解码。

    Windows 中文系统默认用 GBK(cp936) 解码子进程 stdout；codegraph 输出含 UTF-8 非
    ASCII 字节（符号名/路径）会 UnicodeDecodeError → reader 线程崩 → stdout=None →
    后续 .strip() AttributeError。显式 encoding=utf-8 + errors=replace 修掉，跨平台一致。
    兜底返回 ""（绝不返 None）。
    """
    return subprocess.run(
        ["codegraph", *args], capture_output=True, text=True,
        encoding="utf-8", errors="replace", timeout=timeout,
    ).stdout or ""


def _codegraph_query(seed: str, root: str, limit: int) -> list[dict]:
    out = _run_codegraph(["query", seed, "--path", root, "--limit", str(limit), "--json"])
    try:
        data = json.loads(out) if out.strip() else []
    except json.JSONDecodeError:
        return []
    items = data if isinstance(data, list) else (data.get("results") or [])
    out_list = []
    for it in items:
        n = it.get("node", it) if isinstance(it, dict) else {}
        kind = n.get("kind", "")
        if kind in _NON_SYMBOL_KINDS:
            continue
        out_list.append({"name": n.get("name", ""), "kind": kind, "file": n.get("filePath", "")})
    return out_list


def list_symbols(seeds: list[str], root: str, per_seed: int = 5) -> list[dict]:
    """多 seed 并集枚举真实符号，按 name 去重。"""
    seen, out = set(), []
    for seed in seeds:
        for s in _codegraph_query(seed, root, per_seed):
            key = (s["name"], s["kind"])
            if s["name"] and key not in seen:
                seen.add(key)
                out.append(s)
    return out


def seeds_from_dir(dir_path: str, root: str, max_files: int = 8) -> list[str]:
    """目录 → 文件 basename 当 seed（兜底；snake/camelCase 可能漏，人审时补）。"""
    try:
        out = _run_codegraph(["files", "--path", root, "--json"])
        files = [f["path"] for f in json.loads(out) if isinstance(f, dict)]
    except Exception:
        files = []
    rel = dir_path.rstrip("/")
    seeds = []
    for fp in files:
        if fp.startswith(rel + "/"):
            base = os.path.splitext(os.path.basename(fp))[0]
            base = re.sub(r"\.(compat|gen|inc)$", "", base)  # a_star.cpp → a_star
            if base and base not in seeds:
                seeds.append(base)
        if len(seeds) >= max_files:
            break
    return seeds


# ── LLM 出题（仅 query 措辞；gold 来自符号）───────────────────────────────
def phrase_query(symbol: dict, client, model: str) -> str:
    """LLM 为符号拟一个 NL 问题，其答案就是该符号名。仅返 query 文本。"""
    prompt = (
        f"你是代码 benchmark 的出题人。给定代码里的符号：`{symbol['name']}`"
        f"（{symbol['kind']}，位于 {symbol['file']}）。\n"
        f"拟**一个**开发者会自然问的问题，这个符号名就是答案。要求：\n"
        f"- 问题里**可以**用概念描述，但答案确定就是 `{symbol['name']}`；\n"
        f"- 简短一句，不要给答案、不要解释。\n"
        f"只输出问题本身。"
    )
    resp = client.messages.create(
        model=model, max_tokens=120, temperature=0.0,
        messages=[{"role": "user", "content": prompt}],
    )
    text = "".join(b.text for b in resp.content if getattr(b, "type", "") == "text")
    return text.strip().strip('"').strip("“”")


# ── 实证验收（零 LLM）─────────────────────────────────────────────────────
def _norm(s: str) -> str:
    return "".join(c.lower() for c in str(s) if c.isalnum())


def ambiguity_check(name: str, root: str) -> dict:
    """gold 名是否同名多【不同模块】的符号（broad 判分会撞）。"""
    hits = _codegraph_query(name, root, 15)
    exact = [h for h in hits if _norm(h["name"]) == _norm(name)]
    modules = sorted({os.path.splitext(os.path.basename(h["file"]))[0] for h in exact if h["file"]})
    kinds = sorted({h["kind"] for h in exact})
    return {"ambiguous": len(modules) > 1, "modules": modules,
            "kinds": kinds, "n_hits": len(exact)}


def retrieval_check(query: str, gold: str, root: str, cmm_project: str) -> dict:
    """query 能否检索到 gold。codegraph（词面）+ cmm（语义，best-effort 容冷启动）。"""
    gn = _norm(gold)
    cg_names = {_norm(r["name"]) for r in _codegraph_query(query, root, 8)}
    cg_hit = any(gn and gn in n for n in cg_names) or gn in cg_names
    cmm_hit = False
    try:
        from eval.subjects import cmm_bm25, norm_item
        for r in cmm_bm25(cmm_project, query, 8):
            if isinstance(r, dict) and gn and gn in _norm(norm_item(r).get("node", "")):
                cmm_hit = True
                break
    except Exception:
        pass  # cmm 冷启动/未装 → 仅靠 codegraph
    return {"retrievable": cg_hit or cmm_hit, "via_codegraph": cg_hit, "via_cmm": cmm_hit}


def verify_candidate(candidate: dict, root: str, cmm_project: str) -> dict:
    """实证验收（零 LLM）：可靠信号 = gold 同名歧义；检索仅信息项。"""
    gold = candidate["gold"][0] if candidate.get("gold") else ""
    amb = ambiguity_check(gold, root)
    ret = retrieval_check(candidate.get("query", ""), gold, root, cmm_project)
    reasons = []
    if amb["ambiguous"]:
        reasons.append(f"gold `{gold}` 同名多模块 modules={amb['modules']}（歧义，broad 判分会撞）")
    if ret["retrievable"]:
        reasons.append(f"实证检索到 gold（via codegraph={ret['via_codegraph']}/cmm={ret['via_cmm']}）")
    else:
        reasons.append("NL query 词面未直接命中（正常，NL↔gold 匹配交 subagent 判）")
    verdict = "review" if amb["ambiguous"] else "pass"
    return {"verdict": verdict, "ambiguous": amb["ambiguous"],
            "retrievable": ret["retrievable"], "reason": "; ".join(reasons)}


# ── generate / verify（直接写 problems.json）──────────────────────────────
def generate(seeds: list[str], target_id: str, client, model: str, n: int = 20) -> dict:
    """seed → 枚举符号 → LLM 拟题 → 候选（status: pending + provenance）追加进 problems.json。

    root / cmm_project 从 target.json 读。返 {symbols, candidates, target}。
    """
    target = load_target(target_id)
    root = target["code"]["codegraph_root"]
    cmm_project = target["code"]["cmm_project"]
    syms = list_symbols(seeds, root)[:n]
    existing = load_problems(target_id)
    existing_q = {p["query"] for p in existing if p["type"] == "code_retrieval"}
    new = []
    for s in syms:
        q = phrase_query(s, client, model)
        if not q or q in existing_q:
            continue
        existing_q.add(q)
        new.append({
            "type": "code_retrieval", "query": q, "gold": {"symbols": [s["name"]]},
            "status": "pending",
            "provenance": {"source_symbol": s["name"], "kind": s["kind"], "file": s["file"]},
        })
    save_problems(target_id, existing + new)  # 给新候选分配稳定 id + 校验 + 写回
    return {"symbols": len(syms), "candidates": len(new), "target": target_id}


def verify(target_id: str) -> dict:
    """对 problems.json 里的 status: pending 候选，原地标 verdict/reason（增量，幂等）。

    仅对 code_retrieval 候选（歧义/检索是 code 概念）。返 {n, pass, review, target}。
    """
    target = load_target(target_id)
    root = target["code"]["codegraph_root"]
    cmm_project = target["code"]["cmm_project"]
    problems = load_problems(target_id)
    npass = nreview = 0
    for p in problems:
        if p.get("status") != "pending" or p["type"] != "code_retrieval":
            continue
        v = verify_candidate({"query": p["query"], "gold": p["gold"]["symbols"]}, root, cmm_project)
        p["verdict"] = v["verdict"]
        p["reason"] = v["reason"]
        if v["verdict"] == "pass":
            npass += 1
        else:
            nreview += 1
    save_problems(target_id, problems, assign=False)  # id 已存在，不重分配；只写回 verdict/reason
    return {"n": npass + nreview, "pass": npass, "review": nreview, "target": target_id}

"""Gold 生成器：symbol-driven 挖掘 + 人审 query（低成本扩题库）。

流程：人给范围（seed 词 / 目录）→ codegraph 枚举真实符号 → LLM 为每个符号拟 NL 问题 →
写审核队列文件 → 人审（删/改）→ fold 进 gold_<target>.py。

**成本分离（关键）**：
- gold = 真实符号（codegraph 自证存在，**构造即正确，零 LLM judge**）
- LLM 只拟 query 措辞（它擅长、错了人审）
- 人只审 query 是否清晰无歧义（~10 秒/条，review ≪ author）

用法：
  bench goldgen <seed> [--seed S2 ...] --target godot [--dir core/math] [--n 20]
  bench goldgen-fold --target godot
"""
from __future__ import annotations

import json
import os
import re
import subprocess

# 非"真符号"的节点 kind（文件/导入/目录级），枚举时滤掉
_NON_SYMBOL_KINDS = {"file", "import", "directory", "unknown", "module", "package"}
# codegraph 项目根（换代码库改这里，或 --root 传）
DEFAULT_ROOT = "/Users/ks_128/Documents/godot-src/core"


# ── 符号枚举（codegraph，零 LLM）──────────────────────────────────────────

def _codegraph_query(seed: str, root: str, limit: int) -> list[dict]:
    out = subprocess.run(
        ["codegraph", "query", seed, "--path", root, "--limit", str(limit), "--json"],
        capture_output=True, text=True, timeout=30,
    ).stdout
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


def list_symbols(seeds: list[str], root: str = DEFAULT_ROOT, per_seed: int = 5) -> list[dict]:
    """多 seed 并集枚举真实符号，按 name 去重。"""
    seen, out = set(), []
    for seed in seeds:
        for s in _codegraph_query(seed, root, per_seed):
            key = (s["name"], s["kind"])
            if s["name"] and key not in seen:
                seen.add(key)
                out.append(s)
    return out


def seeds_from_dir(dir_path: str, root: str = DEFAULT_ROOT, max_files: int = 8) -> list[str]:
    """目录 → 文件 basename 当 seed（兜底；snake/camelCase 可能漏，人审时补）。"""
    try:
        out = subprocess.run(
            ["codegraph", "files", "--path", root, "--json"],
            capture_output=True, text=True, timeout=30,
        ).stdout
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
        f"你是代码 benchmark 的出题人。给定 Godot 代码里的符号：`{symbol['name']}`"
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


# ── 审核队列文件 ──────────────────────────────────────────────────────────

def generate(seeds: list[str], target: str, client, model: str,
             root: str = DEFAULT_ROOT, n: int = 20) -> dict:
    """编排：seed → 枚举符号 → LLM 拟题 → 写审核队列。返 {symbols, candidates, pending_path}。"""
    syms = list_symbols(seeds, root)[:n]
    cands = []
    for s in syms:
        q = phrase_query(s, client, model)
        if q:
            cands.append({"query": q, "gold": [s["name"]], "name": s["name"],
                          "kind": s["kind"], "file": s["file"]})
    p = write_pending(target, cands)
    return {"symbols": len(syms), "candidates": len(cands), "pending_path": p}


def pending_path(target: str) -> str:
    return os.path.join(os.path.dirname(__file__), "reports", f"gold_pending_{target}.md")


def write_pending(target: str, candidates: list[dict]) -> str:
    """写审核队列 md：每块一个 candidate，人删/改后跑 fold。"""
    p = pending_path(target)
    lines = [
        f"# gold_pending · target={target}",
        f"# 审核：保留你要的块、删不要的、可改 `query:` 措辞。完成后跑 `bench goldgen-fold --target {target}`。",
        "# 每块以 `## candidate` 开头；fold 只收 `query:` + `gold:` 两行。",
        "",
    ]
    for c in candidates:
        lines += [
            "## candidate",
            f"- query: {c['query']}",
            f"- gold: {json.dumps(c['gold'], ensure_ascii=False)}",
            f"- source: {c['name']} [{c['kind']}] {c['file']}",
            "",
        ]
    with open(p, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return p


def parse_pending(target: str) -> list[tuple[str, list[str]]]:
    """解析审核后的 pending 文件：每个 ## candidate 块取 query + gold。"""
    p = pending_path(target)
    if not os.path.exists(p):
        return []
    text = open(p, encoding="utf-8").read()
    out = []
    for block in re.split(r"^## candidate\s*$", text, flags=re.MULTILINE):
        qm = re.search(r"^-\s*query:\s*(.+)$", block, re.MULTILINE)
        gm = re.search(r"^-\s*gold:\s*(.+)$", block, re.MULTILINE)
        if qm and gm:
            try:
                gold = json.loads(gm.group(1).strip())
            except json.JSONDecodeError:
                gold = [gm.group(1).strip().strip('"')]
            out.append((qm.group(1).strip(), gold))
    return out


# ── fold 进 gold_<target>.py ──────────────────────────────────────────────

def _gold_file_path(target: str) -> str:
    return os.path.join(os.path.dirname(__file__), f"gold_{target}.py")


def write_gold_module(target: str, gold: list[tuple[str, set]], project: str = "") -> str:
    """（重）写 gold_<target>.py：GOLD = [(query, {symbols}), ...]。"""
    p = _gold_file_path(target)
    body = [f'"""gold 集（target={target}）。部分由 goldgen 生成 + 人审。"""', "from __future__ import annotations", ""]
    if project:
        body += [f'PROJECT = "{project}"', ""]
    body.append("GOLD: list[tuple[str, set[str]]] = [")
    for q, gs in gold:
        syms = ", ".join(f'"{s}"' for s in sorted(gs))
        body.append(f"    ({q!r}, {{{syms}}}),")
    body.append("]")
    with open(p, "w", encoding="utf-8") as f:
        f.write("\n".join(body) + "\n")
    return p


def fold(target: str) -> dict:
    """把审核后 pending 里的 candidate fold 进 gold_<target>.py（去重合并）。"""
    new = parse_pending(target)
    # 读现有 gold
    existing = []
    project = ""
    try:
        import importlib
        mod = importlib.import_module(f"eval.gold_{target}")
        existing = list(mod.GOLD)
        project = getattr(mod, "PROJECT", "")
    except Exception:
        pass
    existing_q = {q for q, _ in existing}
    added = 0
    for q, gold in new:
        if q in existing_q:
            continue
        existing.append((q, set(gold)))
        existing_q.add(q)
        added += 1
    write_gold_module(target, existing, project)
    return {"added": added, "total": len(existing), "target": target}

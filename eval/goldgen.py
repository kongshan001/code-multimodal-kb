"""Gold 生成器：symbol-driven 挖掘 + 两层自动验收 + 人审（低成本扩题库）。

**4 阶段流程**（人审前过两层自动 vet）：
  1. generate：人给范围（seed 词 / 目录）→ codegraph 枚举真实符号 → LLM 拟 NL 问题
     （gold = 符号，构造即正确，零 LLM judge）→ 写审核队列
  2. 实证 verify（bench goldgen-verify）：codegraph 查同名歧义 + 检索可达，标 verdict/reason
  3. 独立 subagent 验收（主 agent spawn）：判 NL query↔gold 语义匹配（实证做不到的，抓错配/前提错）
  4. 人审（删/改）→ fold 进 gold_<target>.py

**两层验收互补**：实证层抓歧义 gold（grounded，零 LLM）；subagent 抓语义错配（如 query 说"数学
向量"但 gold=Vector 动态数组、或前提事实错）。人只做最终拍板。

用法：
  bench goldgen <seed> [--seed S2 ...] --target godot [--dir core/math] [--n 20]
  bench goldgen-verify --target godot        # 实证验收（自动 vet）
  # 主 agent spawn 独立 subagent 做语义验收（见上面流程 3）
  bench goldgen-fold --target godot          # 人审后入库
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

def _norm(s: str) -> str:
    return "".join(c.lower() for c in str(s) if c.isalnum())


def ambiguity_check(name: str, root: str = DEFAULT_ROOT) -> dict:
    """gold 名是否同名多【不同模块】的符号（broad 判分会撞）。
    method+class 同符号（.h 声明 + .cpp 定义 = 同模块）不算歧义；
    不同模块出现同名（Color 在 math/color + rb_map + variant）才算。"""
    hits = _codegraph_query(name, root, 15)
    exact = [h for h in hits if _norm(h["name"]) == _norm(name)]
    # 按模块（basename 去扩展名）归并：resource_uid.h/.cpp → "resource_uid" 同模块
    modules = sorted({os.path.splitext(os.path.basename(h["file"]))[0] for h in exact if h["file"]})
    kinds = sorted({h["kind"] for h in exact})
    return {"ambiguous": len(modules) > 1, "modules": modules,
            "kinds": kinds, "n_hits": len(exact)}


def retrieval_check(query: str, gold: str, root: str = DEFAULT_ROOT) -> dict:
    """query 能否检索到 gold。codegraph（词面）+ cmm（语义，best-effort 容冷启动）。"""
    gn = _norm(gold)
    # codegraph（词面，对 NL 弱但对术语强）
    cg_names = {_norm(r["name"]) for r in _codegraph_query(query, root, 8)}
    cg_hit = any(gn and gn in n for n in cg_names) or gn in cg_names
    # cmm 语义（best-effort，冷启动容错）
    cmm_hit = False
    try:
        from eval.subjects import cmm_bm25, norm_item
        for r in cmm_bm25(_CMM_PROJ_FALLBACK, query, 8):
            if isinstance(r, dict) and gn and gn in _norm(norm_item(r).get("node", "")):
                cmm_hit = True
                break
    except Exception:
        pass  # cmm 冷启动/未装 → 仅靠 codegraph
    return {"retrievable": cg_hit or cmm_hit, "via_codegraph": cg_hit, "via_cmm": cmm_hit}


def verify_candidate(candidate: dict, root: str = DEFAULT_ROOT) -> dict:
    """实证验收（零 LLM）：可靠信号 = gold 是否同名歧义（不同模块同名→broad 判分会撞）。
    retrieval 仅信息项——NL/中文 query 词面检索本就够不着符号名，不代表错配（NL 匹配交 subagent 判）。
    """
    gold = candidate["gold"][0] if candidate.get("gold") else ""
    amb = ambiguity_check(gold, root)
    ret = retrieval_check(candidate.get("query", ""), gold, root)
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


# cmm 项目名（retrieval_check 用；与 ab_tools.CMM_PROJECT 同值，这里独立声明避循环导入）
_CMM_PROJ_FALLBACK = "Users-ks-128-Documents-godot-src-core"


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


def verify_pending(target: str, root: str = DEFAULT_ROOT) -> dict:
    """独立 subagent/实证 验收：对 pending 每个 candidate 算 verdict，回写 `- verdict:` / `- reason:` 行。
    在人审前自动 vet（catches 歧义 gold + query↔gold 错配）。返回 {n, pass, review}。"""
    p = pending_path(target)
    if not os.path.exists(p):
        return {"n": 0, "pass": 0, "review": 0}
    text = open(p, encoding="utf-8").read()
    header, *rest = re.split(r"^(## candidate\s*)$", text, flags=re.MULTILINE)
    # rest 交替：[marker, block, marker, block, ...]
    npass = nreview = 0
    out = [header]
    for i in range(0, len(rest), 2):
        marker = rest[i] if i < len(rest) else ""
        block = rest[i + 1] if i + 1 < len(rest) else ""
        qm = re.search(r"^-\s*query:\s*(.+)$", block, re.MULTILINE)
        gm = re.search(r"^-\s*gold:\s*(.+)$", block, re.MULTILINE)
        if qm and gm:
            try:
                gold = json.loads(gm.group(1).strip())
            except json.JSONDecodeError:
                gold = [gm.group(1).strip().strip('"')]
            v = verify_candidate({"query": qm.group(1).strip(), "gold": gold}, root)
            if v["verdict"] == "pass":
                npass += 1
            else:
                nreview += 1
            # 去掉旧的 verdict/reason 行（重跑幂等），再加新的
            block = re.sub(r"^-\s*(verdict|reason):.*$\n?", "", block, flags=re.MULTILINE)
            block = block.rstrip() + f"\n- verdict: {v['verdict']}\n- reason: {v['reason']}\n"
        out.append(marker)
        out.append(block)
    with open(p, "w", encoding="utf-8") as f:
        f.write("".join(out))
    return {"n": npass + nreview, "pass": npass, "review": nreview}


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

"""跑代码侧基线：对指定 target 的 gold 集用指定检索路调 cmm，算 recall@k（多指标）。

三路检索（实证修正后架构，见 reports/retrieval-comparison-godot.md）：
  grep     — search_code（精确/路径）
  bm25     — search_graph query（NL 概念主路）
  semantic — search_graph semantic_query（token-相似兜底；需 moderate/full 索引）

用法：
  python -m eval.run_code_baseline --target godot --method bm25
  python -m eval.run_code_baseline --target godot --method grep     # 默认
"""
from __future__ import annotations

import argparse
import importlib
import json
import re
import statistics

from eval.metrics import hit_rate_at_k, recall_at_k
from eval.repro import detect_lockfile, stamp
from eval.subjects import cmm_bm25, cmm_search, cmm_semantic, norm_item

KS = (1, 3, 5, 10)
LIMIT = 10

_STOP = {"a", "an", "the", "to", "of", "for", "and", "or", "in", "on", "is", "are",
         "how", "where", "what", "who", "with", "abstraction"}


def load_gold(target: str):
    mod = importlib.import_module(f"eval.gold_{target}")
    return mod.PROJECT, mod.GOLD


def _keywords(nl: str) -> list[str]:
    """naive NL→关键词（semantic_query 用）。仅作可复现基线；真实场景靠 agent 翻译更准。"""
    toks = [t.lower() for t in re.split(r"[^A-Za-z0-9_]+", nl) if t]
    ks = [t for t in toks if len(t) >= 2 and t not in _STOP]
    return ks or toks[:1]


def _retrieve(method: str, project: str, query: str):
    if method == "grep":
        return cmm_search(project, query, LIMIT)
    if method == "bm25":
        return cmm_bm25(project, query, LIMIT)
    if method == "semantic":
        return cmm_semantic(project, _keywords(query), LIMIT)
    raise ValueError(f"unknown method: {method}")


def _norm(s: str) -> str:
    return "".join(c.lower() for c in str(s) if c.isalnum())


def _item_text(it: dict) -> str:
    return _norm(" ".join(str(it.get(k, "")) for k in ("node", "qualified_name", "file")))


def broad_recall_at_k(items: list[dict], gold: set[str], k: int) -> float:
    if not gold:
        return 0.0
    texts = [_item_text(it) for it in items[:k]]
    hits = sum(1 for g in gold if any(_norm(g) in t for t in texts))
    return hits / len(gold)


def run(target: str = "code", method: str = "grep") -> dict:
    project, gold = load_gold(target)
    rows = []
    for query, goldset in gold:
        raw = [r for r in _retrieve(method, project, query) if isinstance(r, dict)]
        items = [norm_item(r) for r in raw]
        nodes = [it["node"] for it in items]
        row = {"query": query, "gold": sorted(goldset), "retrieved_top5": nodes[:5]}
        if method == "semantic":
            row["keywords"] = _keywords(query)
        for k in KS:
            row[f"recall@{k}"] = round(recall_at_k(nodes, goldset, k), 3)  # strict
            row[f"broad_recall@{k}"] = round(broad_recall_at_k(items, goldset, k), 3)
        rows.append(row)

    agg = {}
    for k in KS:
        agg[f"mean_recall@{k}"] = round(statistics.mean(r[f"recall@{k}"] for r in rows), 3)
        agg[f"mean_broad_recall@{k}"] = round(statistics.mean(r[f"broad_recall@{k}"] for r in rows), 3)

    report = stamp(
        {"subject": f"cmm.{method}", "target": target, "project": project,
         "n": len(rows), "aggregate": agg, "per_query": rows},
        detect_lockfile(),
    )
    return report


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", default="code")
    ap.add_argument("--method", default="grep", choices=["grep", "bm25", "semantic"])
    args = ap.parse_args()
    print(json.dumps(run(args.target, args.method), ensure_ascii=False, indent=2))

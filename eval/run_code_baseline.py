"""跑代码侧首基线（task 2.2/2.3/2.4 串起来）：对 graphify gold 集调 cmm search_code，
算 recall@k / hit_rate@k（Symbol Hit@k = 符号级 recall@k，同公式）。

用法：python -m eval.run_code_baseline
"""
from __future__ import annotations

import json
import statistics

from eval.gold_code import GOLD, PROJECT
from eval.metrics import hit_rate_at_k, recall_at_k
from eval.repro import detect_lockfile, stamp
from eval.subjects import cmm_search

KS = (1, 3, 5, 10)
LIMIT = 10


def run() -> dict:
    rows = []
    for query, gold in GOLD:
        results = cmm_search(PROJECT, query, limit=LIMIT)
        retrieved = [r.get("node") for r in results if isinstance(r, dict)]
        row = {"query": query, "gold": sorted(gold), "retrieved_top5": retrieved[:5]}
        for k in KS:
            row[f"recall@{k}"] = round(recall_at_k(retrieved, gold, k), 3)  # = Symbol Hit@k
            row[f"hit@{k}"] = hit_rate_at_k(retrieved, gold, k)
        rows.append(row)

    agg = {}
    for k in KS:
        agg[f"mean_recall@{k}"] = round(statistics.mean(r[f"recall@{k}"] for r in rows), 3)
        agg[f"hit_rate@{k}"] = round(statistics.mean(r[f"hit@{k}"] for r in rows), 3)

    report = stamp(
        {"subject": "cmm.search_code", "target": "graphify", "n": len(rows),
         "aggregate": agg, "per_query": rows},
        detect_lockfile(),
    )
    return report


if __name__ == "__main__":
    rep = run()
    print(json.dumps(rep, ensure_ascii=False, indent=2))

"""跑文档侧基线（task 3.2/3.4）：对 Godot 文档图跑 graphify query，算召回。

检索 = graphify query（BFS 遍历 graph.json，不调 LLM）。graphify 自动从 NL 选起始节点。
用法：python -m eval.run_doc_baseline
"""
from __future__ import annotations

import json
import re
import subprocess
import statistics

from eval.gold_docs import GRAPH, GOLD
from eval.metrics import recall_at_k

KS = (1, 3, 5, 100)  # 第 4 档用大值=全部返回节点


def graphify_query(graph: str, question: str, budget: int = 1200) -> list[str]:
    """调 graphify query，解析返回的 NODE <label> 行（有序）。"""
    proc = subprocess.run(
        ["graphify", "query", question, "--graph", graph, "--budget", str(budget)],
        capture_output=True, text=True, timeout=90,
    )
    labels: list[str] = []
    for line in proc.stdout.splitlines():
        if line.startswith("NODE "):
            rest = line[5:]
            label = rest.rsplit(" [src=", 1)[0].strip()  # 'Vector2 Class [src=...' → 'Vector2 Class'
            if label:
                labels.append(label)
    return labels


def run() -> dict:
    rows = []
    for query, gold in GOLD:
        retrieved = graphify_query(GRAPH, query)
        row = {"query": query, "gold": sorted(gold), "retrieved_top5": retrieved[:5], "n_returned": len(retrieved)}
        for k in KS:
            row[f"recall@{k}"] = round(recall_at_k(retrieved, gold, k), 3)
        rows.append(row)

    agg = {}
    for k in KS:
        agg[f"mean_recall@{k}"] = round(statistics.mean(r[f"recall@{k}"] for r in rows), 3)

    return {"subject": "graphify.query", "target": "godot-docs-subset", "graph": GRAPH,
            "n": len(rows), "aggregate": agg, "per_query": rows}


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=2))

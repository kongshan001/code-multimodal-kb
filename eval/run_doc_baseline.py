"""跑文档侧基线：对 target 的文档图跑 graphify query，算召回。

target = targets/<id>/（doc_retrieval 型）。文档图路径从该 target 的 target.json 读
（经 overlay）。检索 = graphify query（BFS 遍历 graph.json，不调 LLM）。
用法：python -m eval.run_doc_baseline --target godot-docs
"""
from __future__ import annotations

import argparse
import json
import statistics

from eval._subproc import run_text
from eval.metrics import recall_at_k
from eval.targets import load_problems, load_target

KS = (1, 3, 5, 100)  # 第 4 档用大值=全部返回节点


def graphify_query(graph: str, question: str, budget: int = 1200) -> list[str]:
    """调 graphify query，解析返回的 NODE <label> 行（有序）。"""
    proc = run_text(
        ["graphify", "query", question, "--graph", graph, "--budget", str(budget)],
        timeout=90,
    )
    labels: list[str] = []
    for line in proc.stdout.splitlines():
        if line.startswith("NODE "):
            rest = line[5:]
            label = rest.rsplit(" [src=", 1)[0].strip()  # 'Vector2 Class [src=...' → 'Vector2 Class'
            if label:
                labels.append(label)
    return labels


def run(target_id: str = "godot-docs") -> dict:
    target = load_target(target_id)
    graph = target["doc"]["graph"]
    problems = [p for p in load_problems(target_id) if p["type"] == "doc_retrieval"]

    rows = []
    for p in problems:
        query, gold = p["query"], set(p["gold"]["node_labels"])
        retrieved = graphify_query(graph, query)
        row = {"query": query, "gold": sorted(gold), "retrieved_top5": retrieved[:5], "n_returned": len(retrieved)}
        for k in KS:
            row[f"recall@{k}"] = round(recall_at_k(retrieved, gold, k), 3)
        rows.append(row)

    agg = {}
    for k in KS:
        agg[f"mean_recall@{k}"] = round(statistics.mean(r[f"recall@{k}"] for r in rows), 3)

    return {"subject": "graphify.query", "target": target_id, "graph": graph,
            "n": len(rows), "aggregate": agg, "per_query": rows}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", default="godot-docs")
    a = ap.parse_args()
    print(json.dumps(run(a.target), ensure_ascii=False, indent=2))

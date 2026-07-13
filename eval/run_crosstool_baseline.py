"""跨工具 anchoring 基线（design：文档概念 → cmm 代码定位）。

target = targets/<id>/（cross_anchor 型）。该 target 经 deps 声明依赖 doc_graph + cmm
两个 target；loader 解析成 deps_resolved，runner 无感取文档图路径 + cmm 项目名。
每条：graphify query(concept) 找文档节点 → 拿标识符 → cmm BM25 定位代码 → 验证文件。
三率：graphify 命中、cmm 命中、端到端跨工具成功（两者都中）。
用法：python -m eval.run_crosstool_baseline --target godot-cross
"""
from __future__ import annotations

import argparse
import json
import statistics

from eval.run_doc_baseline import graphify_query
from eval.subjects import cmm_bm25
from eval.targets import load_problems, load_target

KS_CMM = (1, 3, 5)


def _cmm_file_hit(results: list[dict], expected_substr: str, k: int) -> bool:
    """cmm top-k 结果里是否有 file_path 含 expected_substr。"""
    for r in results[:k]:
        fp = (r.get("file_path") or r.get("file") or "")
        if expected_substr in fp:
            return True
    return False


def run(target_id: str = "godot-cross") -> dict:
    target = load_target(target_id)
    graph = target["deps_resolved"]["doc_graph"]["doc"]["graph"]
    cmm_project = target["deps_resolved"]["cmm"]["code"]["cmm_project"]
    problems = [p for p in load_problems(target_id) if p["type"] == "cross_anchor"]

    rows = []
    for p in problems:
        concept = p["query"]
        doc_label = p["gold"]["doc_node_label"]
        cmm_q = p["gold"]["cmm_identifier"]
        code_file = p["gold"]["code_file"]

        doc_nodes = graphify_query(graph, concept)
        graphify_hit = doc_label in doc_nodes

        cmm_res = cmm_bm25(cmm_project, cmm_q, limit=10)
        cmm_hits = {k: _cmm_file_hit(cmm_res, code_file, k) for k in KS_CMM}

        row = {"concept": concept, "doc_label": doc_label, "cmm_query": cmm_q,
               "expected_code": code_file, "graphify_hit": graphify_hit,
               "cmm_hit@5": cmm_hits[5],
               "crosstool_ok": graphify_hit and cmm_hits[5]}
        rows.append(row)

    g = sum(r["graphify_hit"] for r in rows)
    c = sum(r["cmm_hit@5"] for r in rows)
    x = sum(r["crosstool_ok"] for r in rows)
    n = len(rows)
    return {"subject": "cross-tool anchoring (graphify→cmm)", "target": target_id, "n": n,
            "graphify_hit_rate": round(g / n, 3), "cmm_hit_rate@5": round(c / n, 3),
            "crosstool_success_rate": round(x / n, 3), "per_query": rows}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", default="godot-cross")
    a = ap.parse_args()
    print(json.dumps(run(a.target), ensure_ascii=False, indent=2))

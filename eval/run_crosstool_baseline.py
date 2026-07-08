"""跨工具 anchoring 基线（design：文档概念 → cmm 代码定位）。

每条：graphify query(concept) 找文档节点 → 拿标识符 → cmm BM25 定位代码 → 验证文件。
三率：graphify 命中、cmm 命中、端到端跨工具成功（两者都中）。
用法：python -m eval.run_crosstool_baseline
"""
from __future__ import annotations

import json
import statistics

from eval.gold_crosstool import CMM_PROJECT, GRAPH, GOLD
from eval.run_doc_baseline import graphify_query
from eval.subjects import cmm_bm25

KS_CMM = (1, 3, 5)


def _cmm_file_hit(results: list[dict], expected_substr: str, k: int) -> bool:
    """cmm top-k 结果里是否有 file_path 含 expected_substr。"""
    for r in results[:k]:
        fp = (r.get("file_path") or r.get("file") or "")
        if expected_substr in fp:
            return True
    return False


def run() -> dict:
    rows = []
    for concept, doc_label, cmm_q, code_file in GOLD:
        doc_nodes = graphify_query(GRAPH, concept)
        graphify_hit = doc_label in doc_nodes

        cmm_res = cmm_bm25(CMM_PROJECT, cmm_q, limit=10)
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
    return {"subject": "cross-tool anchoring (graphify→cmm)", "n": n,
            "graphify_hit_rate": round(g / n, 3), "cmm_hit_rate@5": round(c / n, 3),
            "crosstool_success_rate": round(x / n, 3), "per_query": rows}


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=2))

"""记忆答案质量评测——Ragas 协议（faithfulness + context_precision）应用到记忆层。

填 value-benchmark §7 最后一格"记忆答案质量"（记忆召回已测 hit@5=0.933，但召回的 drawer
喂给 agent 作答的质量没测）。和 run_doc_quality_ragas 同构，只是 context 从 .rst 换成
mempalace 召回的 drawer 文本。

诚实边界（同 doc-ragas）：GLM 生成 + GLM 判 = 同家族 self-preference；相对参考值非绝对回归值。
预期：memory drawer 多为会话碎片（嘈杂/冗长），faithfulness/context_precision 可能低于文档层
（.rst 结构化文本更易忠实作答）——这本身是发现。

用法：bench run memory-quality
"""
from __future__ import annotations

import statistics

from eval.ab_agent import load_creds, make_client
from eval.repro import detect_lockfile, stamp
from eval.run_doc_quality_ragas import _generate_answer, context_precision, faithfulness
from eval.subjects_memory import mempalace_search
from eval.targets import load_problems, load_target

_MODEL = None


def run(target_id: str = "engineer-demo-memory", subset: int | None = None, k_chunks: int = 5) -> dict:
    """对 memory_recall 题每条：mempalace 召回 drawer 做 context → GLM 答 → Ragas 协议判分。"""
    target = load_target(target_id)
    palace = target.get("memory", {}).get("palace", target_id)
    problems = [p for p in load_problems(target_id) if p["type"] == "memory_recall"]
    questions = problems[:subset] if subset else problems
    client = make_client()

    rows = []
    for p in questions:
        query, gold_sources = p["query"], set(p["gold"]["source_files"])
        raw = mempalace_search(query, limit=k_chunks)
        chunks = [it["text"] for it in raw if it.get("text")]
        context = "\n".join(chunks) or "(无 context)"
        answer = _generate_answer(query, context, client)
        f = faithfulness(answer, context, client)
        c = context_precision(query, chunks, client)
        rows.append({"query": query, "gold_sources": sorted(gold_sources),
                     "answer": answer[:200], "n_chunks": len(chunks),
                     "top_sources": [it.get("source_file", "") for it in raw[:3]],
                     "faithfulness": f["score"], "context_precision": c["score"]})
        print(f"  faithful={f['score']:.2f} ctx_prec={c['score']:.2f} nc={len(chunks)}  {query[:40]}", flush=True)

    agg = {
        "n": len(rows),
        "mean_faithfulness": round(statistics.mean(r["faithfulness"] for r in rows), 3),
        "mean_context_precision": round(statistics.mean(r["context_precision"] for r in rows), 3),
        "llm_judge": "glm-5.x（self-preference 风险，相对参考值）",
        "context_source": "mempalace drawers（会话碎片为主）",
    }
    report = stamp(
        {"subject": "memory-quality-ragas-protocol", "target": target_id, "palace": palace,
         "n": len(rows), "aggregate": agg, "per_query": rows,
         "metrics": "faithfulness + context_precision（reference-free，Ragas 协议；记忆层）",
         "note": "LLM-judged（GLM 生成+判分，同家族 self-preference）；记忆 drawer 嘈杂，预期低于文档层"},
        detect_lockfile(),
    )
    return report


if __name__ == "__main__":
    import argparse, json as _json
    ap = argparse.ArgumentParser(description="记忆答案质量（Ragas 协议，mempalace drawer 做 context）")
    ap.add_argument("--target", default="engineer-demo-memory")
    ap.add_argument("--subset", type=int, default=None)
    ap.add_argument("--k", type=int, default=5)
    a = ap.parse_args()
    print(_json.dumps(run(a.target, a.subset, a.k), ensure_ascii=False, indent=2))

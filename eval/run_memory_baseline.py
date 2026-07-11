"""跑记忆侧基线（task 4.2 + 4.3）：MemPalace 召回质量 + D1 边界路由准确率。

两部分指标：
  recall    — 对 RECALL_GOLD 调 mempalace search，按 source_file 召回算
              recall@k / hit@k（k=1,3,5,10）+ unique_source_ratio@5（去重）。
  routing   — 对 ROUTING_GOLD 跑 D1 router（routing.py），算四类 + 总体准确率。
  volume    — 注入体积收敛：search 固定返回 ≤ LIMIT（不随库增长无界膨胀）。

零 LLM：MemPalace 用本地 embedding（onnxruntime），查询阶段不调 LLM，可复现。
用法：
  python -m eval.run_memory_baseline
  bench run memory
"""
from __future__ import annotations

import argparse
import json
import statistics

from eval.gold_memory import RECALL_GOLD, ROUTING_GOLD
from eval.metrics import hit_rate_at_k, recall_at_k
from eval.repro import detect_lockfile, stamp
from eval.routing import routing_accuracy
from eval.subjects_memory import mempalace_search, norm_source

KS = (1, 3, 5, 10)
LIMIT = 10


def _dedup_sources(raw: list[dict]) -> list[str]:
    """按 source_file 去重，保留首次出现的 rank 顺序（同一文件的后续 drawer 不重复计）。"""
    seen: list[str] = []
    for it in raw:
        sf = norm_source(it)
        if sf and sf not in seen:
            seen.append(sf)
    return seen


def run() -> dict:
    # ── recall：主观记忆按主题召回 ──
    rows = []
    for query, gold_sources in RECALL_GOLD:
        raw = mempalace_search(query, limit=LIMIT)
        sources = _dedup_sources(raw)
        row = {
            "query": query,
            "gold": sorted(gold_sources),
            "retrieved_top5": sources[:5],
            "n_raw": len(raw),
            "n_unique_source": len(sources),
        }
        for k in KS:
            row[f"hit@{k}"] = round(hit_rate_at_k(sources, gold_sources, k), 3)
            row[f"recall@{k}"] = round(recall_at_k(sources, gold_sources, k), 3)
        # 去重正确率代理：top-5 结果里不同 source 占比（1.0 = 无同源冗余）
        top5_raw = raw[:5]
        row["unique_source_ratio@5"] = round(
            len({norm_source(it) for it in top5_raw}) / max(1, len(top5_raw)), 3
        )
        rows.append(row)

    agg: dict = {}
    for k in KS:
        agg[f"mean_recall@{k}"] = round(statistics.mean(r[f"recall@{k}"] for r in rows), 3)
        agg[f"mean_hit@{k}"] = round(statistics.mean(r[f"hit@{k}"] for r in rows), 3)
    agg["mean_unique_source_ratio@5"] = round(
        statistics.mean(r["unique_source_ratio@5"] for r in rows), 3
    )

    # ── routing：D1 四层归属准确率 ──
    rres = routing_accuracy([(fact, gold) for fact, gold, _ in ROUTING_GOLD])
    agg["routing_overall_accuracy"] = rres["overall"]
    agg["routing_per_class"] = rres["per_class"]
    agg["routing_errors"] = rres["errors"]
    agg["routing_n"] = rres["n"]

    # ── volume：注入体积收敛（设计属性，非曲线）──
    # MemPalace search 固定返回 ≤ LIMIT；MEMORY.md 全量注入另有 ~20 条容量上限。
    # 两者都有界 → 注入体积不随库增长无界膨胀（Stage 1 已从全量切换为按需召回）。
    agg["injection_cap_search"] = LIMIT
    agg["injection_cap_memory_md"] = 20

    report = stamp(
        {"subject": "mempalace", "target": "engineer_demo",
         "n": len(rows), "aggregate": agg, "per_query": rows},
        detect_lockfile(),
    )
    return report


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="记忆侧基线（MemPalace 召回 + D1 路由）")
    args = ap.parse_args()
    print(json.dumps(run(), ensure_ascii=False, indent=2))

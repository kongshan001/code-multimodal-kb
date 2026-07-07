"""跑代码侧基线（task 2.2/2.3/2.4 串起来）：对指定 target 的 gold 集调 cmm search_code，
算 recall@k / hit_rate@k（Symbol Hit@k = 符号级 recall@k，同公式）。

**双指标**（cmm 在大 C++ 仓库返回方法/文件节点、把类定义埋在方法下 → 严格 node 匹配过严）：
  - recall@k（strict）：gold ∈ retrieved node 短名
  - broad_recall@k：gold 出现在 retrieved 的 node|qualified_name|file 任一（文件/类区级命中）

用法：
  python -m eval.run_code_baseline                 # 默认 target=code（graphify）
  python -m eval.run_code_baseline --target godot  # Godot core/
"""
from __future__ import annotations

import argparse
import importlib
import json
import statistics

from eval.metrics import hit_rate_at_k, recall_at_k
from eval.repro import detect_lockfile, stamp
from eval.subjects import cmm_search

KS = (1, 3, 5, 10)
LIMIT = 10


def load_gold(target: str):
    mod = importlib.import_module(f"eval.gold_{target}")
    return mod.PROJECT, mod.GOLD


def _norm(s: str) -> str:
    """归一化：小写 + 去非字母数字（消 snake_case/CamelCase 差异，如 message_queue==MessageQueue）。"""
    return "".join(c.lower() for c in str(s) if c.isalnum())


def _result_text(r: dict) -> str:
    return _norm(" ".join(str(r.get(k, "")) for k in ("node", "qualified_name", "file")))


def broad_recall_at_k(results: list[dict], gold: set[str], k: int) -> float:
    """gold 中任一名出现在 top-k 某结果的 node|qualified_name|file（归一化后）→ 命中（类区/文件级）。"""
    if not gold:
        return 0.0
    texts = [_result_text(r) for r in results[:k]]
    hits = sum(1 for _g in gold if any(_norm(_g) in t for t in texts))
    return hits / len(gold)


def run(target: str = "code") -> dict:
    project, gold = load_gold(target)
    rows = []
    for query, goldset in gold:
        raw = [r for r in cmm_search(project, query, limit=LIMIT) if isinstance(r, dict)]
        nodes = [r.get("node") for r in raw]
        row = {"query": query, "gold": sorted(goldset), "retrieved_top5": nodes[:5]}
        for k in KS:
            row[f"recall@{k}"] = round(recall_at_k(nodes, goldset, k), 3)  # strict
            row[f"broad_recall@{k}"] = round(broad_recall_at_k(raw, goldset, k), 3)
        rows.append(row)

    agg = {}
    for k in KS:
        agg[f"mean_recall@{k}"] = round(statistics.mean(r[f"recall@{k}"] for r in rows), 3)
        agg[f"mean_broad_recall@{k}"] = round(statistics.mean(r[f"broad_recall@{k}"] for r in rows), 3)

    report = stamp(
        {"subject": "cmm.search_code", "target": target, "project": project,
         "n": len(rows), "aggregate": agg, "per_query": rows},
        detect_lockfile(),
    )
    return report


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", default="code", help="gold 模块名（eval/gold_<target>.py）")
    args = ap.parse_args()
    print(json.dumps(run(args.target), ensure_ascii=False, indent=2))

"""检索 + 图指标（tasks 2.2、2.3）。

纯函数、零网络、零 LLM。合成样本验证见 tests/test_retrieval_metrics.py、test_graph_metrics.py。
"""
from __future__ import annotations

import math
from typing import Iterable, Sequence

Id = str
Edge = tuple[str, str]


# ── 检索指标（task 2.2：RepoBench-R recall@k/nDCG@10 + SWE-Lancer 命中率）──────────

def recall_at_k(retrieved: Sequence[Id], gold: Iterable[Id], k: int) -> float:
    """top-k 命中 gold 的比例 = |retrieved[:k] ∩ gold| / |gold|。gold 空记 0。"""
    gold_set = set(gold)
    if not gold_set:
        return 0.0
    topk = list(retrieved)[:k]
    hits = sum(1 for r in topk if r in gold_set)
    return hits / len(gold_set)


def hit_rate_at_k(retrieved: Sequence[Id], gold: Iterable[Id], k: int) -> float:
    """top-k 是否命中任一 gold（每 query 0/1，全体取均）。单 query 视角。"""
    gold_set = set(gold)
    topk = list(retrieved)[:k]
    return 1.0 if any(r in gold_set for r in topk) else 0.0


def ndcg_at_k(retrieved: Sequence[Id], gold: Iterable[Id], k: int) -> float:
    """二值相关性的 nDCG@k = DCG@k / IDCG@k。"""
    gold_set = set(gold)
    if not gold_set:
        return 0.0
    topk = list(retrieved)[:k]
    dcg = sum(
        (1.0 if topk[i] in gold_set else 0.0) / math.log2(i + 2)
        for i in range(len(topk))
    )
    ideal_hits = min(len(gold_set), k)
    idcg = sum(1.0 / math.log2(i + 2) for i in range(ideal_hits))
    return dcg / idcg if idcg > 0 else 0.0


# ── 图检索指标（task 2.3：Symbol-Level Hit@k / Call-Chain Edge Recall / Path Precision@k）──

def symbol_hit_at_k(retrieved: Sequence[Id], gold: Iterable[Id], k: int) -> float:
    """符号级 recall@k（gold 来自静态调用图）。"""
    return recall_at_k(retrieved, gold, k)


def call_chain_edge_recall(retrieved_edges: Iterable[Edge], gold_edges: Iterable[Edge]) -> float:
    """调用链边召回 = |retrieved ∩ gold edges| / |gold edges|。"""
    g = {tuple(e) for e in gold_edges}
    if not g:
        return 0.0
    r = {tuple(e) for e in retrieved_edges}
    return len(r & g) / len(g)


def path_precision_at_k(retrieved_path: Sequence[Id], gold_path: Iterable[Id], k: int) -> float:
    """路径精确率@k = top-k 路径节点中属于 gold 路径的比例（查准，非查全）。"""
    gold_set = set(gold_path)
    topk = list(retrieved_path)[:k]
    if not topk:
        return 0.0
    hits = sum(1 for n in topk if n in gold_set)
    return hits / len(topk)

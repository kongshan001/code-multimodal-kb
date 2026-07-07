"""task 2.2 合成验证：recall@k / hit_rate / nDCG@k（手算期望值）。"""
from eval.metrics import recall_at_k, hit_rate_at_k, ndcg_at_k


def test_recall_at_k_partial():
    # retrieved=[a,b,c,d], gold={b,d,f}, k=3 → top3={a,b,c}, 命中 b → 1/3
    assert recall_at_k(["a", "b", "c", "d"], ["b", "d", "f"], k=3) == 1 / 3


def test_recall_at_k_full_window():
    # k=10 → 命中 {b,d}=2 / |gold|=3
    assert recall_at_k(["a", "b", "c", "d"], ["b", "d", "f"], k=10) == 2 / 3


def test_recall_empty_gold_is_zero():
    assert recall_at_k(["a", "b"], [], k=2) == 0.0


def test_hit_rate_hit_and_miss():
    assert hit_rate_at_k(["a", "b", "c"], ["b"], k=3) == 1.0
    assert hit_rate_at_k(["x", "y", "z"], ["a"], k=3) == 0.0


def test_ndcg_at_k_handcomputed():
    # retrieved=[a,b,c,d], gold={b,d}, k=4
    # rel=[0,1,0,1] → DCG = 0 + 1/log2(3) + 0 + 1/log2(5)
    # IDCG(2 hits) = 1/log2(2) + 1/log2(3)
    import math
    dcg = 1 / math.log2(3) + 1 / math.log2(5)
    idcg = 1 / math.log2(2) + 1 / math.log2(3)
    assert ndcg_at_k(["a", "b", "c", "d"], ["b", "d"], k=4) == dcg / idcg


def test_ndcg_perfect_ranking_is_one():
    # gold 全在顶部且按序 → nDCG=1.0
    assert ndcg_at_k(["b", "d", "a"], ["b", "d"], k=3) == 1.0

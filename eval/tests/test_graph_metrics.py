"""task 2.3 合成验证：Symbol Hit@k / Call-Chain Edge Recall / Path Precision@k。"""
from eval.metrics import (
    symbol_hit_at_k,
    call_chain_edge_recall,
    path_precision_at_k,
)


def test_symbol_hit_at_k():
    # retrieved=[foo,bar,baz], gold={bar,qux}, k=2 → top2={foo,bar} 命中 bar → 1/2
    assert symbol_hit_at_k(["foo", "bar", "baz"], ["bar", "qux"], k=2) == 0.5


def test_call_chain_edge_recall_partial():
    # retrieved 边命中 gold 2/3
    ret = [("a", "b"), ("c", "d"), ("e", "f")]
    gold = [("a", "b"), ("c", "d"), ("x", "y")]
    assert call_chain_edge_recall(ret, gold) == 2 / 3


def test_call_chain_edge_recall_order_invariant_within_edge():
    # 边是 (caller,callee) 有序对；(a,b) ≠ (b,a)
    assert call_chain_edge_recall([("a", "b")], [("b", "a")]) == 0.0
    assert call_chain_edge_recall([("a", "b")], [("a", "b")]) == 1.0


def test_call_chain_empty_gold_is_zero():
    assert call_chain_edge_recall([("a", "b")], []) == 0.0


def test_path_precision_at_k_partial():
    # path=[n1,n2,n3,n4], gold={n2,n4,n6}, k=3 → top3={n1,n2,n3} 命中 n2 → 1/3
    assert path_precision_at_k(["n1", "n2", "n3", "n4"], ["n2", "n4", "n6"], k=3) == 1 / 3


def test_path_precision_all_correct():
    assert path_precision_at_k(["n2", "n4", "n6"], ["n2", "n4", "n6"], k=3) == 1.0

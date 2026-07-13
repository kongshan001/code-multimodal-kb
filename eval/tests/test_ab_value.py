"""Stage 0 token 代理测试（task 6.1 / 6.2）。零外部依赖（mock loader + cmm + grep）。"""
from eval.run_ab_value import _tok


def test_tok_estimate():
    assert _tok("") == 1                    # 空兜底为 1（避免除零）
    assert _tok("abcd") == 1                # 4 chars ≈ 1 token
    assert _tok("a" * 400) == 100           # 400 chars ≈ 100 tokens


def test_ab_value_smoke(monkeypatch):
    """L2 端到端：mock loader + cmm（命中 gold）+ grep（有命中）→ 压缩比 + kb_hit@5 预期。"""
    import eval.run_ab_value as rv
    from eval.repro import Lockfile

    # mock loader：返回 1 个 target + 2 道 code_retrieval 题
    monkeypatch.setattr(rv, "load_target", lambda tid: {
        "code": {"cmm_project": "fakeproj", "codegraph_root": "/fake/code"}})
    monkeypatch.setattr(rv, "load_problems", lambda tid: [
        {"id": "t-color", "type": "code_retrieval", "query": "color", "gold": {"symbols": ["Color"]}},
        {"id": "t-json", "type": "code_retrieval", "query": "json", "gold": {"symbols": ["JSON"]}},
    ])

    # mock cmm：返回含 gold 名的结果
    def fake_bm25(project, query, limit):
        name = "Color" if "color" in query.lower() else "JSON"
        return [{"name": name, "qualified_name": f"x.{name}", "file_path": "a.h"}]
    monkeypatch.setattr(rv, "cmm_bm25", fake_bm25)

    # mock grep：list_tokens 小、read_tokens 大 → 高压缩比（新签名 query + code_root）
    monkeypatch.setattr(rv, "_grep_read_cost", lambda q, root: {
        "file_count": 5, "list_tokens": 50, "read_tokens": 4000, "grep_miss": False})

    monkeypatch.setattr(rv, "detect_lockfile", lambda: Lockfile(cmm_version="test"))

    report = rv.run(target_id="fake")
    agg = report["aggregate"]
    assert report["n"] == 2
    assert agg["mean_kb_hit@5"] == 1.0               # mock 全命中 gold
    assert agg["mean_compression_read"] > 1.0         # naive_read(4000) >> kb_tokens → 压缩
    assert agg["grep_miss_count"] == 0
    assert report["stage"] == 0
    assert report["lockfile"]["cmm_version"] == "test"
    # per_query 字段齐全
    row = report["per_query"][0]
    assert {"kb_tokens", "naive_read_tokens", "compression_read", "kb_hit@5"} <= set(row)

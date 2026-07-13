"""记忆答案质量测试（run_memory_quality 编排层）。faithfulness/context_precision 已在
test_doc_quality_ragas 测过，这里只测 run() 用 mempalace context 的编排。"""
import eval.run_memory_quality as M


def test_memory_quality_smoke(monkeypatch):
    """mock mempalace_search + 三个 LLM 函数 → run() aggregate 预期。"""
    import eval.run_doc_quality_ragas as R
    monkeypatch.setattr(M, "mempalace_search", lambda q, limit=5: [
        {"text": "用户偏好全局工具", "source_file": "prefer-global.md"},
        {"text": "改动提交 git", "source_file": "commit.md"}])
    monkeypatch.setattr(M, "_generate_answer", lambda q, ctx, c: "用户偏好全局共享工具。")
    monkeypatch.setattr(M, "faithfulness", lambda ans, ctx, c: {"score": 1.0})
    monkeypatch.setattr(M, "context_precision", lambda q, chunks, c: {"score": 0.5})
    monkeypatch.setattr(M, "make_client", lambda: None)
    monkeypatch.setattr(M, "detect_lockfile", lambda: type("L", (), {"to_dict": lambda s: {}})())

    # subset=2 取前 2 条 memory_recall 题（经 loader 读 problems.json）
    rep = M.run(target_id="engineer-demo-memory", subset=2)
    assert rep["n"] == 2
    assert rep["aggregate"]["mean_faithfulness"] == 1.0
    assert rep["aggregate"]["mean_context_precision"] == 0.5
    assert rep["aggregate"]["context_source"].startswith("mempalace")
    # per_query 带 top_sources
    assert "top_sources" in rep["per_query"][0]

"""文档答案质量（Ragas 协议）测试。mock _llm_text，不调真 GLM。"""
import eval.run_doc_quality_ragas as R


def test_faithfulness_parses_judgement(monkeypatch):
    """claim 抽取 + 判支撑 → faithfulness = supported/total。"""
    calls = {"n": 0}
    def fake_llm(client, prompt, max_tokens=512):
        calls["n"] += 1
        if calls["n"] == 1:  # claim 抽取
            return '["Color 是 RGB", "Color 不可变"]'
        # 判支撑：第一条 supported，第二条 not
        return '[{"claim":"Color 是 RGB","supported":true},{"claim":"Color 不可变","supported":false}]'
    monkeypatch.setattr(R, "_llm_text", fake_llm)
    r = R.faithfulness("Color 是 RGB 且不可变", "context...", client=None)
    assert r["n_claims"] == 2 and r["n_supported"] == 1
    assert r["score"] == 0.5


def test_faithfulness_no_claims_is_vacuously_one(monkeypatch):
    """refusal/非事实答案抽不出 claim → 视为 1.0（无 claim 可幻觉）。"""
    monkeypatch.setattr(R, "_llm_text", lambda c, p, max_tokens=512: "[]")
    r = R.faithfulness("context 不足", "ctx", client=None)
    assert r["score"] == 1.0 and r["n_claims"] == 0


def test_context_precision_parses(monkeypatch):
    """3 chunk 1 切题 → 0.333。"""
    monkeypatch.setattr(R, "_llm_text", lambda c, p, max_tokens=512:
                        '[{"i":0,"relevant":false},{"i":1,"relevant":true},{"i":2,"relevant":false}]')
    r = R.context_precision("q", ["c0", "c1", "c2"], client=None)
    assert r["n_chunks"] == 3 and r["n_relevant"] == 1
    assert r["score"] == round(1 / 3, 3)


def test_extract_json_defensive():
    """LLM 把 JSON 裹在 prose 里也能抓出来。"""
    assert R._extract_json('答案是：["a","b"]。完成') == ["a", "b"]
    assert R._extract_json('无 json 这里') is None
    assert R._extract_json('[{"x":1}]') == [{"x": 1}]

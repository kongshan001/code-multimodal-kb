"""goldgen 测试：符号枚举（真 codegraph）+ LLM 拟题（mock）+ fold（tmp 隔离）。"""
import os


def test_list_symbols_real_codegraph():
    """真 codegraph：seed 'color' 枚举出 Color 等真实符号（非 file/import 节点）。"""
    from eval.goldgen import list_symbols
    syms = list_symbols(["color"], per_seed=5)
    assert len(syms) > 0
    names = [s["name"] for s in syms]
    assert "Color" in names                       # gold-correct-by-construction 的关键
    assert all(s["kind"] not in ("file", "import", "directory") for s in syms)


def test_verify_flags_ambiguous_gold():
    """验收：Color 同名多符号（function/enum/enum_member）→ 标 review。"""
    from eval.goldgen import verify_candidate, ambiguity_check
    amb = ambiguity_check("Color")
    assert amb["ambiguous"] is True               # Color 在 rb_map/variant/math 多处
    assert len(amb["kinds"]) >= 2
    v = verify_candidate({"query": "x", "gold": ["Color"]})
    assert v["ambiguous"] is True
    assert v["verdict"] == "review"               # 歧义 → 需人审


def test_verify_clean_unique_symbol():
    """验收：唯一名符号（如 ResourceUID）不歧义。"""
    from eval.goldgen import ambiguity_check
    amb = ambiguity_check("ResourceUID")
    assert amb["ambiguous"] is False              # ResourceUID 基本只在 resource_uid.h/.cpp


def test_verify_pending_annotates(monkeypatch, tmp_path):
    """verify_pending 给每个 candidate 块标 verdict/reason（幂等重跑）。"""
    import eval.goldgen as G
    monkeypatch.setattr(G, "pending_path", lambda target: str(tmp_path / f"vp_{target}.md"))
    monkeypatch.setattr(G, "verify_candidate", lambda c, root=G.DEFAULT_ROOT: {
        "verdict": "review", "ambiguous": True, "retrievable": False, "reason": "mock"})
    p = G.pending_path("vt")
    open(p, "w").write("## candidate\n- query: q\n- gold: [\"X\"]\n- source: X\n\n")
    res = G.verify_pending("vt")
    assert res["n"] == 1 and res["review"] == 1
    annotated = open(p).read()
    assert "- verdict: review" in annotated and "- reason: mock" in annotated
    # 幂等：重跑不重复堆积 verdict 行
    G.verify_pending("vt")
    assert annotated.count("- verdict:") == 1 or open(p).read().count("- verdict: review") == 1


class _FakeMsg:
    def __init__(self, text):
        class _B:
            type = "text"
        self.content = [type("_B", (), {"type": "text", "text": text})()]


class _FakeClient:
    def __init__(self, texts):
        self._it = iter(texts)
        self.messages = type("M", (), {"create": lambda self_, **kw: _FakeMsg(next(self._it))})()


def test_generate_writes_pending(monkeypatch, tmp_path):
    """mock LLM + mock 枚举 → generate 写审核队列，gold 来自符号（非 LLM）。"""
    import eval.goldgen as G
    # mock 枚举（不依赖 codegraph）
    monkeypatch.setattr(G, "list_symbols", lambda seeds, root, per_seed=5: [
        {"name": "Color", "kind": "class", "file": "math/color.h"},
        {"name": "JSON", "kind": "class", "file": "io/json.cpp"},
    ])
    monkeypatch.setattr(G, "pending_path", lambda target: str(tmp_path / f"gold_pending_{target}.md"))
    client = _FakeClient(["what represents a color", "json 解析在哪"])
    res = G.generate(["x"], "testtgt", client, "fake-model", n=10)
    assert res["candidates"] == 2
    text = open(res["pending_path"]).read()
    assert "## candidate" in text
    assert "what represents a color" in text
    assert '"Color"' in text                       # gold = 符号名（非 LLM 产物）


def test_fold_appends_to_gold(monkeypatch, tmp_path):
    """审核后的 pending → fold 进 gold_<target>.py（去重合并），写 tmp 隔离。"""
    import eval.goldgen as G
    # 隔离路径到 tmp
    monkeypatch.setattr(G, "pending_path", lambda target: str(tmp_path / f"gold_pending_{target}.md"))
    monkeypatch.setattr(G, "_gold_file_path", lambda target: str(tmp_path / f"gold_{target}.py"))
    # 写一个审核后的 pending（人删了第 2 个、留第 1+3）
    pending = (
        "## candidate\n- query: color 在哪\n- gold: [\"Color\"]\n- source: Color [class] math/color.h\n\n"
        "## candidate\n- query: 不要这条\n- gold: [\"Bad\"]\n- source: Bad\n\n"
    )
    open(G.pending_path("foldtest"), "w").write(pending)
    res = G.fold("foldtest")
    # 注意：fold 不删 candidate（人审时已删），收全部剩余块
    assert res["added"] == 2
    assert res["target"] == "foldtest"
    # gold 文件写出，含两条
    written = open(G._gold_file_path("foldtest")).read()
    assert "color 在哪" in written and "Color" in written


def test_fold_dedup(monkeypatch, tmp_path):
    """同一 pending 内重复 query 只加一次（fold 的 within-pending 去重）。"""
    import eval.goldgen as G
    monkeypatch.setattr(G, "pending_path", lambda target: str(tmp_path / f"pp_{target}.md"))
    monkeypatch.setattr(G, "_gold_file_path", lambda target: str(tmp_path / f"g_{target}.py"))
    open(G.pending_path("dup"), "w").write(
        '## candidate\n- query: same q\n- gold: ["X"]\n\n'
        '## candidate\n- query: same q\n- gold: ["X"]\n\n'
        '## candidate\n- query: new q\n- gold: ["Y"]\n\n')
    res = G.fold("dup")     # 2 条 same q → 去重留 1，new q +1 → 共 +2
    assert res["added"] == 2
    assert res["total"] == 2

"""goldgen 测试：符号枚举（真 codegraph）+ LLM 拟题（mock）+ generate/verify（tmp 隔离）。

新存储模型（design D6）：候选直接进 targets/<id>/problems.json（status: pending），
verify 原地标 verdict/reason，无 pending.md、无 fold。
"""
import json

import pytest

from eval.targets import load_target


# ── 真 codegraph 集成（godot-core target）──────────────────────────────────
def _root():
    return load_target("godot-core")["code"]["codegraph_root"]


def _cmm_project():
    return load_target("godot-core")["code"]["cmm_project"]


def test_list_symbols_real_codegraph():
    """真 codegraph：seed 'color' 枚举出 Color 等真实符号（非 file/import 节点）。"""
    from eval.goldgen import list_symbols
    syms = list_symbols(["color"], _root(), per_seed=5)
    assert len(syms) > 0
    names = [s["name"] for s in syms]
    assert "Color" in names                       # gold-correct-by-construction 的关键
    assert all(s["kind"] not in ("file", "import", "directory") for s in syms)


def test_verify_flags_ambiguous_gold():
    """验收：Color 同名多符号（不同模块）→ 标 review。"""
    from eval.goldgen import verify_candidate, ambiguity_check
    amb = ambiguity_check("Color", _root())
    assert amb["ambiguous"] is True               # Color 在 rb_map/variant/math 多处
    assert len(amb["kinds"]) >= 2
    v = verify_candidate({"query": "x", "gold": ["Color"]}, _root(), _cmm_project())
    assert v["ambiguous"] is True
    assert v["verdict"] == "review"               # 歧义 → 需人审


def test_verify_clean_unique_symbol():
    """验收：唯一名符号（如 ResourceUID）不歧义。"""
    from eval.goldgen import ambiguity_check
    amb = ambiguity_check("ResourceUID", _root())
    assert amb["ambiguous"] is False


# ── hermetic：generate / verify（tmp 隔离 TARGETS_DIR）─────────────────────
def _seed_target(tmp_path, monkeypatch, problems=None):
    """在 tmp 造一个 godot-core target（含 target.json + problems.json），重定向 loader。"""
    from eval import targets as T
    monkeypatch.setattr(T, "TARGETS_DIR", tmp_path)
    d = tmp_path / "godot-core"
    d.mkdir()
    (d / "target.json").write_text(json.dumps({
        "id": "godot-core", "subjects": ["code_retrieval"],
        "code": {"codegraph_root": "/fake/code", "cmm_project": "fakeproj"}}, ensure_ascii=False))
    (d / "problems.json").write_text(json.dumps(
        {"version": 1, "target": "godot-core", "problems": problems or []}, ensure_ascii=False))


class _FakeMsg:
    def __init__(self, text):
        class _B:
            type = "text"
        self.content = [type("_B", (), {"type": "text", "text": text})()]


class _FakeClient:
    def __init__(self, texts):
        self._it = iter(texts)
        self.messages = type("M", (), {"create": lambda self_, **kw: _FakeMsg(next(self._it))})()


def test_generate_appends_pending(monkeypatch, tmp_path):
    """mock 枚举 + LLM → generate 把候选（status: pending + provenance）追加进 problems.json。"""
    import eval.goldgen as G
    _seed_target(tmp_path, monkeypatch)
    monkeypatch.setattr(G, "list_symbols", lambda seeds, root, per_seed=5: [
        {"name": "Color", "kind": "class", "file": "math/color.h"},
        {"name": "JSON", "kind": "class", "file": "io/json.cpp"},
    ])
    client = _FakeClient(["what represents a color", "json 解析在哪"])
    res = G.generate(["x"], "godot-core", client, "fake-model", n=10)
    assert res["candidates"] == 2

    from eval.targets import load_problems
    problems = load_problems("godot-core")
    assert len(problems) == 2
    p0 = problems[0]
    assert p0["status"] == "pending"
    assert p0["gold"]["symbols"] == ["Color"]            # gold = 符号名（非 LLM 产物）
    assert p0["provenance"] == {"source_symbol": "Color", "kind": "class", "file": "math/color.h"}
    assert p0["id"].startswith("godot-core-")            # 分配了稳定 id


def test_generate_skips_duplicate_queries(monkeypatch, tmp_path):
    """LLM 拟出的 query 与现有题重复 → 跳过（不重复入库）。"""
    import eval.goldgen as G
    _seed_target(tmp_path, monkeypatch, problems=[
        {"id": "godot-core-color", "type": "code_retrieval", "query": "what represents a color",
         "gold": {"symbols": ["Color"]}, "status": "accepted"}])
    monkeypatch.setattr(G, "list_symbols", lambda seeds, root, per_seed=5: [
        {"name": "Color", "kind": "class", "file": "math/color.h"},
        {"name": "JSON", "kind": "class", "file": "io/json.cpp"},
    ])
    client = _FakeClient(["what represents a color", "json 解析在哪"])  # 第 1 条重复
    res = G.generate(["x"], "godot-core", client, "fake-model", n=10)
    assert res["candidates"] == 1                        # 仅 JSON 新增


def test_verify_annotates_pending_in_place(monkeypatch, tmp_path):
    """verify 在 pending 候选原地标 verdict/reason（幂等，不产生第二份文件）。"""
    import eval.goldgen as G
    _seed_target(tmp_path, monkeypatch, problems=[
        {"id": "godot-core-color", "type": "code_retrieval", "query": "color",
         "gold": {"symbols": ["Color"]}, "status": "pending"},
        {"id": "godot-core-json", "type": "code_retrieval", "query": "json",
         "gold": {"symbols": ["JSON"]}, "status": "pending"},
        {"id": "godot-core-old", "type": "code_retrieval", "query": "engine",
         "gold": {"symbols": ["Engine"]}, "status": "accepted"},  # 已 accepted，跳过
    ])
    monkeypatch.setattr(G, "verify_candidate", lambda cand, root, cmm_project: {
        "verdict": "review", "ambiguous": True, "retrievable": False, "reason": "mock"})
    res = G.verify("godot-core")
    assert res["n"] == 2 and res["review"] == 2          # 只验 2 个 pending，accepted 跳过

    from eval.targets import load_problems
    problems = {p["id"]: p for p in load_problems("godot-core")}
    assert problems["godot-core-color"]["verdict"] == "review"
    assert problems["godot-core-color"]["reason"] == "mock"
    assert "verdict" not in problems["godot-core-old"]   # accepted 未被动
    # 幂等：重跑不堆积
    G.verify("godot-core")
    problems2 = {p["id"]: p for p in load_problems("godot-core")}
    assert problems2["godot-core-color"]["reason"] == "mock"

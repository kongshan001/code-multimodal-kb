"""eval/targets.py loader + schema 校验测试。

两类：
  - 真实迁移产物集成测试：加载 eval/targets/ 下 5 个 target，校验 schema + 题数守恒
  - hermetic 校验测试：tmp_path 造合成 target，覆盖 deps/各类非法 schema
"""
from __future__ import annotations

import json

import pytest

from eval import targets as T


# ── helpers：在 tmp 目录造合成 target ──────────────────────────────────────
def _make_target(tmp_path, tid, target, problems, local=None):
    d = tmp_path / tid
    d.mkdir(parents=True)
    (d / "target.json").write_text(json.dumps(target, ensure_ascii=False), encoding="utf-8")
    (d / "problems.json").write_text(
        json.dumps({"version": 1, "target": tid, "problems": problems}, ensure_ascii=False),
        encoding="utf-8")
    if local is not None:
        (d / "target.local.json").write_text(json.dumps(local, ensure_ascii=False), encoding="utf-8")
    return d


def _problem(pid, ptype="code_retrieval", **kw):
    """造一道合法题（默认 code_retrieval）。kw 覆盖特定字段。"""
    p = {"id": pid, "type": ptype, "query": kw.get("query", "test query"),
         "gold": kw.get("gold", {"symbols": ["Foo"]}), "status": "accepted"}
    for k, v in kw.items():
        if k not in ("query", "gold"):
            p[k] = v
    if ptype == "memory_routing":
        p.pop("query", None)
        p["fact"] = kw.get("fact", "some fact")
    return p


# ── 真实题库：每个 target schema 合法 + 题数快照（drift 门禁）──────────────
EXPECTED_COUNTS = {
    "godot-core": 29, "graphify-pkg": 21, "godot-docs": 10,
    "godot-cross": 8, "engineer-demo-memory": 28,  # recall 15 + routing 13
    "claude-gui": 36,
}


def test_list_targets_real():
    ids = T.list_targets()
    assert set(ids) == set(EXPECTED_COUNTS)


@pytest.mark.parametrize("tid", list(EXPECTED_COUNTS))
def test_load_real_targets_schema_valid(tid):
    problems = T.load_problems(tid)
    assert len(problems) == EXPECTED_COUNTS[tid], f"{tid} 题数漂移"
    # 每题 id 唯一（load_problems 已校验，这里再断言）
    ids = [p["id"] for p in problems]
    assert len(ids) == len(set(ids))


def test_godot_cross_deps_resolved():
    """cross target 的 deps 经 loader 解析出 deps_resolved。"""
    t = T.load_target("godot-cross")
    assert t["deps"] == {"doc_graph": "godot-docs", "cmm": "godot-core"}
    dr = t["deps_resolved"]
    assert dr["doc_graph"]["doc"]["graph"].endswith("graph.json")
    assert "cmm_project" in dr["cmm"]["code"]


def test_load_real_uses_all_five_types():
    """5 种 type 都出现在真实题库里。"""
    seen = set()
    for tid in EXPECTED_COUNTS:
        for p in T.load_problems(tid):
            seen.add(p["type"])
    assert seen == {"code_retrieval", "doc_retrieval", "cross_anchor",
                    "memory_recall", "memory_routing", "bug_fix"}


# ── hermetic：target 加载 ─────────────────────────────────────────────────
def test_load_target_returns_config(tmp_path, monkeypatch):
    monkeypatch.setattr(T, "TARGETS_DIR", tmp_path)
    _make_target(tmp_path, "t1",
                 {"id": "t1", "code": {"cmm_project": "proj"}}, [_problem("t1-foo")])
    assert T.load_target("t1")["code"]["cmm_project"] == "proj"


# ── hermetic：deps 解析 ────────────────────────────────────────────────────
def test_deps_missing_target_fails(tmp_path, monkeypatch):
    monkeypatch.setattr(T, "TARGETS_DIR", tmp_path)
    _make_target(tmp_path, "cross",
                 {"id": "cross", "deps": {"cmm": "nope"}}, [_problem("cross-x", "cross_anchor",
                 gold={"doc_node_label": "L", "cmm_identifier": "I", "code_file": "f"})])
    with pytest.raises(T.TargetError, match="nope"):
        T.load_target("cross")


def test_deps_resolved_to_neighbor_target(tmp_path, monkeypatch):
    monkeypatch.setattr(T, "TARGETS_DIR", tmp_path)
    _make_target(tmp_path, "core", {"id": "core", "code": {"cmm_project": "p"}}, [])
    _make_target(tmp_path, "cross",
                 {"id": "cross", "deps": {"cmm": "core"}},
                 [_problem("cross-x", "cross_anchor",
                           gold={"doc_node_label": "L", "cmm_identifier": "I", "code_file": "f"})])
    t = T.load_target("cross")
    assert t["deps_resolved"]["cmm"]["code"]["cmm_project"] == "p"


# ── hermetic：schema 校验各类失败 ─────────────────────────────────────────
@pytest.mark.parametrize("bad,label", [
    # type 非法
    ({"type": "bogus", "query": "q", "gold": {"symbols": ["A"]}, "status": "accepted"}, "type"),
    # type/gold 不匹配：code_retrieval 缺 symbols
    ({"type": "code_retrieval", "query": "q", "gold": {"node_labels": ["A"]}, "status": "accepted"}, "symbols"),
    # gold.symbols 非列表
    ({"type": "code_retrieval", "query": "q", "gold": {"symbols": "Foo"}, "status": "accepted"}, "list"),
    # gold.symbols 空
    ({"type": "code_retrieval", "query": "q", "gold": {"symbols": []}, "status": "accepted"}, "非空"),
    # 缺 query
    ({"type": "code_retrieval", "gold": {"symbols": ["A"]}, "status": "accepted"}, "query"),
    # status 非法
    ({"type": "code_retrieval", "query": "q", "gold": {"symbols": ["A"]}, "status": "draft"}, "status"),
    # memory_routing layer 非法
    ({"type": "memory_routing", "fact": "f", "gold": {"layer": "unknown"}, "status": "accepted"}, "layer"),
    # memory_routing 缺 fact（routing 用 fact 不用 query）
    ({"type": "memory_routing", "query": "f", "gold": {"layer": "objective"}, "status": "accepted"}, "fact"),
    # cross_anchor 缺 code_file
    ({"type": "cross_anchor", "query": "q",
      "gold": {"doc_node_label": "L", "cmm_identifier": "I"}, "status": "accepted"}, "code_file"),
    # bug_fix 缺 files
    ({"type": "bug_fix", "query": "q", "gold": {"symbols": ["X"]}, "status": "accepted"}, "files"),
])
def test_invalid_problem_rejected(tmp_path, monkeypatch, bad, label):
    monkeypatch.setattr(T, "TARGETS_DIR", tmp_path)
    _make_target(tmp_path, "t1", {"id": "t1"}, [bad])
    with pytest.raises(T.TargetError):
        T.load_problems("t1")


def test_duplicate_id_rejected(tmp_path, monkeypatch):
    monkeypatch.setattr(T, "TARGETS_DIR", tmp_path)
    _make_target(tmp_path, "t1", {"id": "t1"},
                 [_problem("t1-same"), _problem("t1-same")])
    with pytest.raises(T.TargetError, match="重复"):
        T.load_problems("t1")


def test_missing_target_dir_fails(tmp_path, monkeypatch):
    monkeypatch.setattr(T, "TARGETS_DIR", tmp_path)
    with pytest.raises(T.TargetError, match="不存在"):
        T.load_target("ghost")


# ── hermetic：每种 type 合法 gold 形状 ────────────────────────────────────
def test_each_type_valid_shape_loads(tmp_path, monkeypatch):
    monkeypatch.setattr(T, "TARGETS_DIR", tmp_path)
    valid = [
        _problem("t-code", "code_retrieval", gold={"symbols": ["A", "B"]}),
        _problem("t-doc", "doc_retrieval", gold={"node_labels": ["Node A"]}),
        _problem("t-cross", "cross_anchor",
                 gold={"doc_node_label": "L", "cmm_identifier": "I", "code_file": "f"}),
        _problem("t-recall", "memory_recall", gold={"source_files": ["a.md", "b.jsonl"]}),
        _problem("t-route", "memory_routing", fact="some fact",
                 gold={"layer": "subjective", "signal": "用户偏好"}),
        _problem("t-bug", "bug_fix", query="memory leak on free",
                 gold={"symbols": ["memdelete"], "files": ["memory.h"]}),
    ]
    _make_target(tmp_path, "t1", {"id": "t1"}, valid)
    problems = T.load_problems("t1")
    assert len(problems) == 6

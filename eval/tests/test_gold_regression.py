"""problems.json 回归门禁：每 target 题数 + 首条 id + target 元信息防漂移。

改题数 / 首条顺序时本测试失败，强制确认是有意改动。
不再断言机器特定的 PROJECT 绝对路径（design：不断言 cmm_project 字面量）。
"""
from eval.targets import load_problems, load_target


def test_godot_core_snapshot():
    problems = load_problems("godot-core")
    assert len(problems) == 29  # 26 code_retrieval + 3 bug_fix
    assert problems[0]["id"] == "godot-core-string-format"
    t = load_target("godot-core")
    assert t["subjects"] == ["code_retrieval"]
    assert t["language"] == "C++"


def test_graphify_pkg_snapshot():
    problems = load_problems("graphify-pkg")
    assert len(problems) == 21
    assert problems[0]["id"] == "graphify-pkg-id-construction"
    assert load_target("graphify-pkg")["subjects"] == ["code_retrieval"]


def test_godot_docs_snapshot():
    problems = load_problems("godot-docs")
    assert len(problems) == 10
    assert problems[0]["id"] == "godot-docs-how-do-nodes"
    assert load_target("godot-docs")["subjects"] == ["doc_retrieval"]


def test_godot_cross_snapshot():
    problems = load_problems("godot-cross")
    assert len(problems) == 8
    assert problems[0]["id"] == "godot-cross-vector2-normalization-length"
    t = load_target("godot-cross")
    assert t["subjects"] == ["cross_anchor"]
    assert t["deps"] == {"doc_graph": "godot-docs", "cmm": "godot-core"}

"""task 3.3 gold 回归门禁：gold_*.py 快照（长度 + 首条）防漂移。

改 gold 长度 / 首条时本测试失败，强制确认是有意改动。
"""


def test_gold_godot_snapshot():
    from eval.gold_godot import GOLD, PROJECT
    assert PROJECT == "Users-ks_128-Documents-godot-src-core"
    assert len(GOLD) == 26
    assert GOLD[0] == ("string format", {"vformat"})


def test_gold_docs_snapshot():
    from eval.gold_docs import GOLD
    assert len(GOLD) == 10
    assert GOLD[0] == ("how do nodes communicate with signals", {"Signals Concept"})


def test_gold_crosstool_snapshot():
    from eval.gold_crosstool import GOLD
    assert len(GOLD) == 8
    assert GOLD[0] == ("vector2 normalization length", "Vector2 Class", "Vector2", "math/vector2")

"""Godot core/ gold 集（task 2.4 精神：gold 来自真实代码结构，零 LLM）。

target = Godot 4.7-stable 的 core/（已 index：13504 节点 / 38470 边 / 1094 类）。
gold 短名取自 cmm get_architecture + file_tree 实测存在的真实 Godot 符号。
混精确名查询与概念查询，以在真实引擎上复现/对比 cmm 的检索特征。
"""
from __future__ import annotations

PROJECT = "Users-ks_128-Documents-godot-src-core"

GOLD: list[tuple[str, set[str]]] = [
    # ── 概念查询（query 词 ≠ 符号名，测概念缺口）──
    ("string format", {"vformat"}),
    ("int to string", {"itos"}),
    ("delete object free memory", {"memdelete"}),
    ("a star pathfinding", {"AStar"}),
    ("operating system abstraction", {"OS"}),
    # ── 精确/近精确名查询（测基线检索）──
    ("color", {"Color"}),
    ("vector2", {"Vector2"}),
    ("vector3", {"Vector3"}),
    ("quaternion", {"Quaternion"}),
    ("rect2", {"Rect2"}),
    ("json", {"JSON"}),
    ("image", {"Image"}),
    ("resource loader", {"ResourceLoader"}),
    ("resource saver", {"ResourceSaver"}),
    ("file access", {"FileAccess"}),
    ("directory access", {"DirAccess"}),
    ("message queue", {"MessageQueue"}),
    ("engine", {"Engine"}),
    ("main loop", {"MainLoop"}),
    ("undo redo", {"UndoRedo"}),
    ("node path", {"NodePath"}),
    ("string name", {"StringName"}),
    ("random number generator", {"RandomNumberGenerator"}),
    ("crypto", {"Crypto"}),
    ("translation server", {"TranslationServer"}),
    ("http client", {"HTTPClient"}),
]

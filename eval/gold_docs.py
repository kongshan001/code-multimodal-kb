"""Godot 文档侧 gold 集（task 3.2/3.4：跨文档图检索评测）。

target = Godot 文档子集图（17 rst → 72 节点）：~/Documents/godot-docs-subset/graphify-out/graph.json
检索接口 = graphify query（BFS，不调 LLM）。gold label 取自建图实测的节点标签。
"""
from __future__ import annotations

GRAPH = "/Users/ks_128/Documents/godot-docs-subset/graphify-out/graph.json"

# (NL 概念查询 → 期望命中的节点 label 集合)
GOLD: list[tuple[str, set[str]]] = [
    ("how do nodes communicate with signals", {"Signals Concept"}),
    ("vector normalization and dot product", {"Vector Normalization", "Dot Product", "Vector2 Class"}),
    ("node lifecycle ready callback", {"_ready Callback", "Node Class"}),
    ("per-frame process physics update", {"_process Virtual Function", "_physics_process Virtual Function"}),
    ("attach child node get node path", {"add_child Method", "get_node Method"}),
    ("load a resource", {"Resource Class", "load Function"}),
    ("global singleton autoload", {"Singleton Pattern"}),
    ("bezier curve path", {"Quadratic Bezier Curve", "Cubic Bezier Curve", "Curve2D Class"}),
    ("matrix rotation transform 2d 3d", {"Matrix Rotation", "Transform2D Class", "Transform3D Class"}),
    ("random number generation noise", {"RandomNumberGenerator Class"}),
]

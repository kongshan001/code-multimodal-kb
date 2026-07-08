"""跨工具 anchoring gold 集（design：graphify 文档概念 → cmm 代码定位）。

每条 = (概念查询, graphify 期望命中的文档节点 label, 喂给 cmm 的标识符, cmm 期望命中的代码文件)。
概念都同时存在于 Godot 文档子集图 与 cmm core/ 索引。
"""
from __future__ import annotations

CMM_PROJECT = "Users-ks_128-Documents-godot-src-core"
GRAPH = "/Users/ks_128/Documents/godot-docs-subset/graphify-out/graph.json"

# (concept, doc_node_label, cmm_query_identifier, expected_code_file_substr)
GOLD: list[tuple[str, str, str, str]] = [
    ("vector2 normalization length", "Vector2 Class", "Vector2", "math/vector2"),
    ("vector3 cross product", "Vector3 Class", "Vector3", "math/vector3"),
    ("transform2d matrix", "Transform2D Class", "Transform2D", "math/transform_2d"),
    ("resource load", "Resource Class", "Resource", "io/resource"),
    ("random number generator", "RandomNumberGenerator Class", "RandomNumberGenerator", "math/random_number_generator"),
    ("expression evaluate", "Expression Class", "Expression", "math/expression"),
    ("quaternion rotation", "Quaternion Struct", "Quaternion", "math/quaternion"),
    ("signal connect object", "Signals Concept", "connect", "object/object"),
]

"""A/B 工具注册表测试（task 6.x）：验证注册/解析/扩展机制。"""
from eval import ab_tools


def test_registry_has_builtin_tools():
    """5 个内置工具都注册了。"""
    assert set(ab_tools.TOOL_REGISTRY) >= {"grep_code", "read_file", "cmm_search",
                                           "graphify_query", "codegraph_search"}
    for name, spec in ab_tools.TOOL_REGISTRY.items():
        assert callable(spec.exec_fn)
        assert spec.schema["name"] == name


def test_arms_resolve_to_schemas():
    """每个臂 → 正确的工具 schema 列表。"""
    base = [s["name"] for s in ab_tools.arm_schemas("baseline")]
    kb = [s["name"] for s in ab_tools.arm_schemas("kb")]
    doc = [s["name"] for s in ab_tools.arm_schemas("doc")]
    cg = [s["name"] for s in ab_tools.arm_schemas("codegraph")]
    assert base == ["grep_code", "read_file"]
    assert kb == ["cmm_search", "read_file"]
    assert doc == ["graphify_query", "read_file"]
    assert cg == ["codegraph_search", "read_file"]


def test_exec_tool_dispatches(monkeypatch):
    """exec_tool 按名调对应 executor。"""
    called = {}
    def fake(query):
        called["q"] = query
        return "(mock cmm)"
    monkeypatch.setitem(ab_tools.TOOL_REGISTRY, "cmm_search",
                        ab_tools.ToolSpec(exec_fn=fake, schema=ab_tools._CMM_DEF))
    out = ab_tools.exec_tool("cmm_search", {"query": "color"})
    assert out == "(mock cmm)"
    assert called["q"] == "color"


def test_register_new_tool_and_arm():
    """接新工具的完整路径：register → 挂臂 → arm_schemas 能解析（loop/判分不动）。"""
    def newkb(query):
        return "newkb-result"
    schema = {"name": "newkb_search", "description": "新代码KB",
              "input_schema": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}}
    ab_tools.register_tool("newkb_search", newkb, schema)
    ab_tools.ARMS["newarm"] = {"tools": ["newkb_search", "read_file"], "skills": []}
    try:
        names = [s["name"] for s in ab_tools.arm_schemas("newarm")]
        assert names == ["newkb_search", "read_file"]
        assert ab_tools.exec_tool("newkb_search", {"query": "x"}) == "newkb-result"
        assert "newarm" in ab_tools.arm_names()
    finally:  # 清理：不污染其它测试
        ab_tools.ARMS.pop("newarm", None)
        ab_tools.TOOL_REGISTRY.pop("newkb_search", None)

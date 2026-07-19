# q21 · code_retrieval · arm: `kb+openspec`

- **题**：节点路径用哪个类？
- **gold**：NodePath
- **答对**：✓
- **答案**：`NodePath`
- **指标**：tokens=2450 · llm_calls=2 · tool_steps=1 · 耗时=8.43s · 截断=否

---

**👤 用户**：节点路径用哪个类？

> 💭 **思考**：用户问"节点路径用哪个类？"，这是关于Godot代码库的问题。我需要用语义搜索来找到相关的类。

在Godot中，节点路径通常是指NodePath类。让我搜索一下确认。

**🔧 `cmm_search`**({"query": "NodePath"})

> 💭 **思考**：好的，搜索结果确认了NodePath类存在。用户问的是节点路径用哪个类，答案就是NodePath。根据指令，我需要直接给出符号名，不要长解释。

**🤖 Agent**：`NodePath`

**📋 工具结果**：
```
- NodePath  (Users-ks_128-Documents-godot-src-core.string.node_path.NodePath.NodePath)  string/node_path.cpp
- ~NodePath  (Users-ks_128-Documents-godot-src-core.string.node_path.NodePath.~NodePath)  string/node_path.cpp
- operator NodePath() const  (Users-ks_128-Documents-godot-src-core.variant.variant.Variant.operator NodePath() const)  variant/variant.cpp
- unref  (Users-ks_128-Documents-godot-src-core.string.node_path.NodePath.unref)  string/node_path.cpp
- operator==  (Users-ks_128-Documents-godot-src-core.string.node_path.NodePath.operator==)  string/node_path.cpp
```


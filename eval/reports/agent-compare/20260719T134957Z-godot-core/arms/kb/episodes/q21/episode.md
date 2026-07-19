# q21 · code_retrieval · arm: `kb`

- **题**：节点路径用哪个类？
- **gold**：NodePath
- **答对**：✓
- **答案**：`NodePath`
- **指标**：tokens=1882 · llm_calls=2 · tool_steps=1 · 耗时=8.31s · 截断=否

---

**👤 用户**：节点路径用哪个类？

> 💭 **思考**：用户问"节点路径用哪个类？"这是在问 Godot 引擎中用于表示节点路径的类。

在 Godot 中，节点路径通常用 `NodePath` 类来表示。让我搜索一下确认。

**🔧 `cmm_search`**({"query": "NodePath"})

> 💭 **思考**：工具返回了 `NodePath` 类，这就是 Godot 中用于表示节点路径的类。我应该直接用这个符号名作答。

**🤖 Agent**：`NodePath`

**📋 工具结果**：
```
- NodePath  (Users-ks_128-Documents-godot-src-core.string.node_path.NodePath.NodePath)  string/node_path.cpp
- ~NodePath  (Users-ks_128-Documents-godot-src-core.string.node_path.NodePath.~NodePath)  string/node_path.cpp
- operator NodePath() const  (Users-ks_128-Documents-godot-src-core.variant.variant.Variant.operator NodePath() const)  variant/variant.cpp
- unref  (Users-ks_128-Documents-godot-src-core.string.node_path.NodePath.unref)  string/node_path.cpp
- operator==  (Users-ks_128-Documents-godot-src-core.string.node_path.NodePath.operator==)  string/node_path.cpp
```


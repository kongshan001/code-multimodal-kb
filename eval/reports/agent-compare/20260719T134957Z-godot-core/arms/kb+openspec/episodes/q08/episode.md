# q08 · code_retrieval · arm: `kb+openspec`

- **题**：三维向量用哪个类？
- **gold**：Vector3
- **答对**：✓
- **答案**：`Vector3`
- **指标**：tokens=2447 · llm_calls=2 · tool_steps=1 · 耗时=6.81s · 截断=否

---

**👤 用户**：三维向量用哪个类？

> 💭 **思考**：用户问"三维向量用哪个类？"，这是在问 Godot 代码库中三维向量使用哪个类。

这是一个简单的代码库问题，我应该使用语义搜索工具来查找相关的类。

让我搜索三维向量相关的类。

**🔧 `cmm_search`**({"query": "三维向量 Vector3"})

> 💭 **思考**：搜索结果显示了 Vector3 类，这是 Godot 中用于三维向量的类。根据我的指令，一旦工具返回了相关符号就立刻用符号名作答，不要反复查。

所以答案是：Vector3

**🤖 Agent**：`Vector3`

**📋 工具结果**：
```
- Vector3  (Users-ks_128-Documents-godot-src-core.math.vector3.Vector3)  math/vector3.h
- rotate  (Users-ks_128-Documents-godot-src-core.math.vector3.Vector3.rotate)  math/vector3.cpp
- rotated  (Users-ks_128-Documents-godot-src-core.math.vector3.Vector3.rotated)  math/vector3.cpp
- snap  (Users-ks_128-Documents-godot-src-core.math.vector3.Vector3.snap)  math/vector3.cpp
- snapped  (Users-ks_128-Documents-godot-src-core.math.vector3.Vector3.snapped)  math/vector3.cpp
```


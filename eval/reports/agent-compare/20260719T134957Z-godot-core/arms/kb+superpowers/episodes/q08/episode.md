# q08 · code_retrieval · arm: `kb+superpowers`

- **题**：三维向量用哪个类？
- **gold**：Vector3
- **答对**：✓
- **答案**：`Vector3`
- **指标**：tokens=2557 · llm_calls=2 · tool_steps=1 · 耗时=8.18s · 截断=否

---

**👤 用户**：三维向量用哪个类？

> 💭 **思考**：用户问"三维向量用哪个类？"，这是在问Godot代码库中用于表示三维向量的类名。

我需要使用语义检索工具来查找相关的类。在Godot中，三维向量通常用Vector3类表示。让我搜索确认一下。

**🔧 `cmm_search`**({"query": "三维向量 vector3"})

> 💭 **思考**：搜索结果确认了三维向量用 `Vector3` 类。根据指令，我需要直接给出简洁的答案，用符号名作答，不要长解释。

**🤖 Agent**：`Vector3`

**📋 工具结果**：
```
- Vector3  (Users-ks_128-Documents-godot-src-core.math.vector3.Vector3)  math/vector3.h
- rotate  (Users-ks_128-Documents-godot-src-core.math.vector3.Vector3.rotate)  math/vector3.cpp
- rotated  (Users-ks_128-Documents-godot-src-core.math.vector3.Vector3.rotated)  math/vector3.cpp
- snap  (Users-ks_128-Documents-godot-src-core.math.vector3.Vector3.snap)  math/vector3.cpp
- snapped  (Users-ks_128-Documents-godot-src-core.math.vector3.Vector3.snapped)  math/vector3.cpp
```


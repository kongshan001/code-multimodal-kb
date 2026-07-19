# q08 · code_retrieval · arm: `kb`

- **题**：三维向量用哪个类？
- **gold**：Vector3
- **答对**：✓
- **答案**：`Vector3`
- **指标**：tokens=1882 · llm_calls=2 · tool_steps=1 · 耗时=8.91s · 截断=否

---

**👤 用户**：三维向量用哪个类？

> 💭 **思考**：用户在问Godot代码库中三维向量用哪个类。这是一个简单的代码定位问题，我需要搜索相关的类。

在Godot中，三维向量通常用Vector3类表示。让我搜索确认一下。

**🔧 `cmm_search`**({"query": "三维向量 Vector3"})

> 💭 **思考**：搜索结果已经明确显示了Vector3类。根据指令，我应该直接给出符号名作为答案，不需要长篇解释。收敛纪律要求我一旦工具返回了相关符号就立刻用符号名作答。

**🤖 Agent**：`Vector3`

**📋 工具结果**：
```
- Vector3  (Users-ks_128-Documents-godot-src-core.math.vector3.Vector3)  math/vector3.h
- rotate  (Users-ks_128-Documents-godot-src-core.math.vector3.Vector3.rotate)  math/vector3.cpp
- rotated  (Users-ks_128-Documents-godot-src-core.math.vector3.Vector3.rotated)  math/vector3.cpp
- snap  (Users-ks_128-Documents-godot-src-core.math.vector3.Vector3.snap)  math/vector3.cpp
- snapped  (Users-ks_128-Documents-godot-src-core.math.vector3.Vector3.snapped)  math/vector3.cpp
```


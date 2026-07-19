# q09 · code_retrieval · arm: `kb+openspec`

- **题**：四元数用哪个类？
- **gold**：Quaternion
- **答对**：✓
- **答案**：`Quaternion`
- **指标**：tokens=2484 · llm_calls=2 · tool_steps=1 · 耗时=7.14s · 截断=否

---

**👤 用户**：四元数用哪个类？

> 💭 **思考**：用户问的是"四元数用哪个类？"，这是在询问Godot引擎中表示四元数的类名。

在Godot中，四元数通常用 `Quaternion` 类来表示。这是一个常见的数学类，用于表示旋转。

我应该用工具来搜索一下，确认一下Godot core/中是否有Quaternion类。

**🔧 `cmm_search`**({"query": "Quaternion"})

> 💭 **思考**：工具返回了确切的 `Quaternion` 类，这就在 math/quaternion.h 中。这就是Godot中表示四元数的类。

根据指示，我应该直接用符号名作答，不要长解释。答案是 Quaternion。

**🤖 Agent**：`Quaternion`

**📋 工具结果**：
```
- Quaternion  (Users-ks_128-Documents-godot-src-core.math.quaternion.Quaternion.Quaternion)  math/quaternion.h
- length  (Users-ks_128-Documents-godot-src-core.math.quaternion.Quaternion.length)  math/quaternion.cpp
- normalize  (Users-ks_128-Documents-godot-src-core.math.quaternion.Quaternion.normalize)  math/quaternion.cpp
- normalized  (Users-ks_128-Documents-godot-src-core.math.quaternion.Quaternion.normalized)  math/quaternion.cpp
- inverse  (Users-ks_128-Documents-godot-src-core.math.quaternion.Quaternion.inverse)  math/quaternion.cpp
```


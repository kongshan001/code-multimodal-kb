# q07 · code_retrieval · arm: `kb+superpowers`

- **题**：二维向量用哪个类？
- **gold**：Vector2
- **答对**：✓
- **答案**：`Vector2`
- **指标**：tokens=2561 · llm_calls=2 · tool_steps=1 · 耗时=7.24s · 截断=否

---

**👤 用户**：二维向量用哪个类？

> 💭 **思考**：用户在问Godot中二维向量用哪个类。这是一个关于代码库的问题，我需要使用工具来查找相关信息。

我应该在Godot core/中搜索二维向量相关的类。在Godot中，二维向量通常是Vector2类。让我用cmm_search工具来确认一下。

**🔧 `cmm_search`**({"query": "二维向量 Vector2"})

> 💭 **思考**：搜索结果很清楚，Godot中的二维向量类是 Vector2。根据指示，我应该直接用符号名作答，不需要长解释。

**🤖 Agent**：`Vector2`

**📋 工具结果**：
```
- Vector2  (Users-ks_128-Documents-godot-src-core.math.vector2.Vector2)  math/vector2.h
- angle  (Users-ks_128-Documents-godot-src-core.math.vector2.Vector2.angle)  math/vector2.cpp
- length  (Users-ks_128-Documents-godot-src-core.math.vector2.Vector2.length)  math/vector2.cpp
- normalize  (Users-ks_128-Documents-godot-src-core.math.vector2.Vector2.normalize)  math/vector2.cpp
- normalized  (Users-ks_128-Documents-godot-src-core.math.vector2.Vector2.normalized)  math/vector2.cpp
```


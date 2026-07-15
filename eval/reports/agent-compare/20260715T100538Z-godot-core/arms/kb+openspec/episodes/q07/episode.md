# q07 · code_retrieval · arm: `kb+openspec`

**题**：二维向量用哪个类？  ·  **gold**：Vector2
**答对**：✓  ·  **答案**：二维向量用 `Vector2`（定义在 `math/vector2.h`）。
**指标**：tokens=1588 · llm_calls=3 · tool_steps=2 · 耗时=15.46s · 截断=否

---

**👤 用户**：二维向量用哪个类？

> 💭 **思考**：用户问二维向量用哪个类。这是简单问题，直接用工具查一下确认。

**🔧 `cmm_search`**({"query": "2D vector class"})

> 💭 **思考**：工具返回的是 templates/vector.h 中的容器类 Vector<T>，不是二维数学向量。我需要明确搜索数学上的二维向量 Vector2。

**🔧 `cmm_search`**({"query": "Vector2 two-dimensional math vector x y"})

**🤖 Agent**：二维向量用 `Vector2`（定义在 `math/vector2.h`）。

**📋 工具结果**：
```
- Vector  (Users-ks_128-Documents-godot-src-core.templates.vector.Vector.Vector)  templates/vector.h
- operator Vector<T>() const  (Users-ks_128-Documents-godot-src-core.templates.local_vector.LocalVector.operator Vector<T>() const)  templates/local_vector.h
- append  (Users-ks_128-Documents-godot-src-core.templates.vector.Vector.append)  templates/vector.h
- erase  (Users-ks_128-Documents-godot-src-core.templates.vector.Vector.erase)  templates/vector.h
- ptrw  (Users-ks_128-Documents-godot-src-core.templates.vector.Vector.ptrw)  templates/vector.h
```

**📋 工具结果**：
```
- flipped_y  (Users-ks_128-Documents-godot-src-core.math.projection.Projection.flipped_y)  math/projection.cpp
- flip_y  (Users-ks_128-Documents-godot-src-core.math.projection.Projection.flip_y)  math/projection.cpp
- Vector2  (Users-ks_128-Documents-godot-src-core.math.vector2.Vector2)  math/vector2.h
- angle  (Users-ks_128-Documents-godot-src-core.math.vector2.Vector2.angle)  math/vector2.cpp
- length  (Users-ks_128-Documents-godot-src-core.math.vector2.Vector2.length)  math/vector2.cpp
```


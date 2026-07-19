# q07 · code_retrieval · arm: `kb+openspec`

- **题**：二维向量用哪个类？
- **gold**：Vector2
- **答对**：✓
- **答案**：`Vector2`
- **指标**：tokens=4041 · llm_calls=3 · tool_steps=2 · 耗时=11.04s · 截断=否

---

**👤 用户**：二维向量用哪个类？

> 💭 **思考**：用户问"二维向量用哪个类？"，这是在问 Godot 代码库中表示二维向量的类名。

这是一个直接的问题，我需要用代码知识库搜索 Godot core/ 中的二维向量相关类。

根据我的了解，Godot 中二维向量通常是 `Vector2` 类，但让我搜索一下确认。

**🔧 `cmm_search`**({"query": "二维向量 2D vector"})

> 💭 **思考**：搜索结果主要是一些 Vector 模板类，但这些可能是容器类，不是二维向量。让我再搜索一下 Vector2。

**🔧 `cmm_search`**({"query": "Vector2"})

> 💭 **思考**：很好，找到了 `Vector2` 类，这是 Godot 中的二维向量类，位于 `math/vector2.h` 文件中。用户问的是二维向量用哪个类，答案就是 `Vector2`。

根据指示，我应该直接给出符号名，不要长解释。

**🤖 Agent**：`Vector2`

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
- Vector2  (Users-ks_128-Documents-godot-src-core.math.vector2.Vector2)  math/vector2.h
- angle  (Users-ks_128-Documents-godot-src-core.math.vector2.Vector2.angle)  math/vector2.cpp
- length  (Users-ks_128-Documents-godot-src-core.math.vector2.Vector2.length)  math/vector2.cpp
- normalize  (Users-ks_128-Documents-godot-src-core.math.vector2.Vector2.normalize)  math/vector2.cpp
- normalized  (Users-ks_128-Documents-godot-src-core.math.vector2.Vector2.normalized)  math/vector2.cpp
```


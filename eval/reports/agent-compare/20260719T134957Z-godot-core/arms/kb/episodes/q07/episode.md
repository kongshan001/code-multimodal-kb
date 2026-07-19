# q07 · code_retrieval · arm: `kb`

- **题**：二维向量用哪个类？
- **gold**：Vector2
- **答对**：✓
- **答案**：`Vector2`
- **指标**：tokens=1847 · llm_calls=2 · tool_steps=1 · 耗时=6.84s · 截断=否

---

**👤 用户**：二维向量用哪个类？

> 💭 **思考**：用户问"二维向量用哪个类"，这是在问 Godot 代码库中二维向量使用哪个类。

让我用语义搜索工具查找相关的类。

**🔧 `cmm_search`**({"query": "二维向量 vector2"})

> 💭 **思考**：搜索结果清楚地显示二维向量使用 `Vector2` 类，位于 math/vector2.h 头文件中。工具返回了相关符号，现在我应该直接回答。

**🤖 Agent**：`Vector2`

**📋 工具结果**：
```
- Vector2  (Users-ks_128-Documents-godot-src-core.math.vector2.Vector2)  math/vector2.h
- angle  (Users-ks_128-Documents-godot-src-core.math.vector2.Vector2.angle)  math/vector2.cpp
- length  (Users-ks_128-Documents-godot-src-core.math.vector2.Vector2.length)  math/vector2.cpp
- normalize  (Users-ks_128-Documents-godot-src-core.math.vector2.Vector2.normalize)  math/vector2.cpp
- normalized  (Users-ks_128-Documents-godot-src-core.math.vector2.Vector2.normalized)  math/vector2.cpp
```


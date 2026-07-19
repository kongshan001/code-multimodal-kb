# q10 · code_retrieval · arm: `kb+openspec`

- **题**：二维矩形用哪个类？
- **gold**：Rect2
- **答对**：✓
- **答案**：`Rect2`
- **指标**：tokens=2492 · llm_calls=2 · tool_steps=1 · 耗时=6.65s · 截断=否

---

**👤 用户**：二维矩形用哪个类？

> 💭 **思考**：用户问"二维矩形用哪个类？"，这是关于 Godot 代码库的问题。我需要在 Godot core/ 中查找与二维矩形相关的类。

在 Godot 中，二维矩形通常用 `Rect2` 类表示。让我用语义搜索来确认这一点。

**🔧 `cmm_search`**({"query": "二维矩形 Rect2 rectangle 2D"})

> 💭 **思考**：搜索结果显示了 `Rect2` 类，这是 Godot 中用于二维矩形的类。根据搜索结果，它位于 math/rect2.h 文件中，有 intersects、encloses、intersection、merge 等方法。

我应该直接用符号名回答。

**🤖 Agent**：`Rect2`

**📋 工具结果**：
```
- Rect2  (Users-ks_128-Documents-godot-src-core.math.rect2.Rect2.Rect2)  math/rect2.h
- intersects  (Users-ks_128-Documents-godot-src-core.math.rect2.Rect2.intersects)  math/rect2.h
- encloses  (Users-ks_128-Documents-godot-src-core.math.rect2.Rect2.encloses)  math/rect2.h
- intersection  (Users-ks_128-Documents-godot-src-core.math.rect2.Rect2.intersection)  math/rect2.h
- merge  (Users-ks_128-Documents-godot-src-core.math.rect2.Rect2.merge)  math/rect2.h
```


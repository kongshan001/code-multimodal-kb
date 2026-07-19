# q10 · code_retrieval · arm: `kb+superpowers`

- **题**：二维矩形用哪个类？
- **gold**：Rect2
- **答对**：✓
- **答案**：`Rect2`
- **指标**：tokens=2592 · llm_calls=2 · tool_steps=1 · 耗时=7.68s · 截断=否

---

**👤 用户**：二维矩形用哪个类？

> 💭 **思考**：用户问"二维矩形用哪个类"，这是在询问 Godot 代码库中用于表示二维矩形的类。

根据我的知识，在 Godot 中，二维矩形通常用 `Rect2` 类来表示。但我应该通过代码库搜索来确认这个答案，因为用户要求我用提供的工具查找。

让我搜索一下相关的符号。

**🔧 `cmm_search`**({"query": "Rect2 二维矩形"})

> 💭 **思考**：搜索结果显示了 `Rect2` 类，这正是用于二维矩形的类。根据工具返回的结果，我可以直接用符号名作答。

**🤖 Agent**：`Rect2`

**📋 工具结果**：
```
- Rect2  (Users-ks_128-Documents-godot-src-core.math.rect2.Rect2.Rect2)  math/rect2.h
- intersects  (Users-ks_128-Documents-godot-src-core.math.rect2.Rect2.intersects)  math/rect2.h
- encloses  (Users-ks_128-Documents-godot-src-core.math.rect2.Rect2.encloses)  math/rect2.h
- intersection  (Users-ks_128-Documents-godot-src-core.math.rect2.Rect2.intersection)  math/rect2.h
- merge  (Users-ks_128-Documents-godot-src-core.math.rect2.Rect2.merge)  math/rect2.h
```


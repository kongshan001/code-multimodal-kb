# q10 · code_retrieval · arm: `kb+openspec`

**题**：二维矩形用哪个类？  ·  **gold**：Rect2
**答对**：✓  ·  **答案**：`Rect2`（`core/math/rect2.h`）。

常用方法：`intersects`、`encloses`、`intersection`、`merge`。
**指标**：tokens=1333 · llm_calls=2 · tool_steps=1 · 耗时=16.69s · 截断=否

---

**👤 用户**：二维矩形用哪个类？

> 💭 **思考**：用户问的是 Godot 中表示二维矩形的类。这是关于回答问题的简单查询，不需要开 spec。

让我搜索一下。

**🔧 `cmm_search`**({"query": "2D rectangle rect2"})

**🤖 Agent**：`Rect2`（`core/math/rect2.h`）。

常用方法：`intersects`、`encloses`、`intersection`、`merge`。

**📋 工具结果**：
```
- Rect2  (Users-ks_128-Documents-godot-src-core.math.rect2.Rect2.Rect2)  math/rect2.h
- intersects  (Users-ks_128-Documents-godot-src-core.math.rect2.Rect2.intersects)  math/rect2.h
- encloses  (Users-ks_128-Documents-godot-src-core.math.rect2.Rect2.encloses)  math/rect2.h
- intersection  (Users-ks_128-Documents-godot-src-core.math.rect2.Rect2.intersection)  math/rect2.h
- merge  (Users-ks_128-Documents-godot-src-core.math.rect2.Rect2.merge)  math/rect2.h
```


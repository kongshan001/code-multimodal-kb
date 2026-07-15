# q10 · code_retrieval · arm: `kb+openspec`

**题**：二维矩形用哪个类？  ·  **gold**：Rect2
**答对**：✓  ·  **答案**：二维矩形用 **`Rect2`** 类（定义在 `core/math/rect2.h`）。

它由 `position`（`Vector2`）和 `size`（`Vector2`）组成，常用方法包括 `intersects()`、`encl
**指标**：tokens=1675 · llm_calls=3 · tool_steps=2 · 耗时=18.74s · 截断=否

---

**👤 用户**：二维矩形用哪个类？

> 💭 **思考**：The user is asking which class represents a 2D rectangle in Godot. Let me search for this.

**🔧 `cmm_search`**({"query": "2D rectangle type"})

> 💭 **思考**：The search didn't directly return Rect2. Let me search more specifically.

**🔧 `cmm_search`**({"query": "Rect2 rectangle class"})

> 💭 **思考**：Found it.

**🤖 Agent**：二维矩形用 **`Rect2`** 类（定义在 `core/math/rect2.h`）。

它由 `position`（`Vector2`）和 `size`（`Vector2`）组成，常用方法包括 `intersects()`、`encloses()`、`intersection()`、`merge()` 等。

> 补充：如果是整数坐标的矩形，对应的是 `Rect2i`。

**📋 工具结果**：
```
- interpolate_transform_2d  (Users-ks_128-Documents-godot-src-core.math.transform_interpolator.TransformInterpolator.interpolate_transform_2d)  math/transform_interpolator.cpp
- get_variant_type  (Users-ks_128-Documents-godot-src-core.variant.type_info.get_variant_type)  variant/type_info.h
- triangulate  (Users-ks_128-Documents-godot-src-core.math.delaunay_2d.Delaunay2D.triangulate)  math/delaunay_2d.h
- operator<  (Users-ks_128-Documents-godot-src-core.math.geometry_2d._AtlasWorkRect.operator<)  math/geometry_2d.cpp
- Transform2D  (Users-ks_128-Documents-godot-src-core.math.transform_2d.Tran
```

**📋 工具结果**：
```
- Rect2  (Users-ks_128-Documents-godot-src-core.math.rect2.Rect2.Rect2)  math/rect2.h
- intersects  (Users-ks_128-Documents-godot-src-core.math.rect2.Rect2.intersects)  math/rect2.h
- encloses  (Users-ks_128-Documents-godot-src-core.math.rect2.Rect2.encloses)  math/rect2.h
- intersection  (Users-ks_128-Documents-godot-src-core.math.rect2.Rect2.intersection)  math/rect2.h
- merge  (Users-ks_128-Documents-godot-src-core.math.rect2.Rect2.merge)  math/rect2.h
```


# q10 · code_retrieval · arm: `kb+superpowers`

**题**：二维矩形用哪个类？  ·  **gold**：Rect2
**答对**：✓  ·  **答案**：二维矩形用 **`Rect2`**（浮点坐标），定义在 `core/math/rect2.h`。

如果需要整数坐标版本，用 **`Rect2i`**（`core/math/rect2i.h`）。
**指标**：tokens=2741 · llm_calls=3 · tool_steps=2 · 耗时=14.9s · 截断=否

---

**👤 用户**：二维矩形用哪个类？

**🔧 `cmm_search`**({"query": "2D rectangle class"})

**📋 工具结果**：
```
- interpolate_transform_2d  (Users-ks_128-Documents-godot-src-core.math.transform_interpolator.TransformInterpolator.interpolate_transform_2d)  math/transform_interpolator.cpp
- triangulate  (Users-ks_128-Documents-godot-src-core.math.delaunay_2d.Delaunay2D.triangulate)  math/delaunay_2d.h
- operator<  (Users-ks_128-Documents-godot-src-core.math.geometry_2d._AtlasWorkRect.operator<)  math/geometry_2d.cpp
- Transform2D  (Users-ks_128-Documents-godot-src-core.math.transform_2d.Transform2D.Transform2D)  math/transform_2d.cpp
- operator*=  (Users-ks_128-Documents-godot-src-core.math.transform_2d.T
```

**🔧 `cmm_search`**({"query": "Rect2 rectangle area"})

**📋 工具结果**：
```
- get_area  (Users-ks_128-Documents-godot-src-core.math.rect2.Rect2.get_area)  math/rect2.h
- has_area  (Users-ks_128-Documents-godot-src-core.math.rect2.Rect2.has_area)  math/rect2.h
- get_area  (Users-ks_128-Documents-godot-src-core.math.face3.Face3.get_area)  math/face3.cpp
- get_area  (Users-ks_128-Documents-godot-src-core.math.rect2i.Rect2i.get_area)  math/rect2i.h
- has_area  (Users-ks_128-Documents-godot-src-core.math.rect2i.Rect2i.has_area)  math/rect2i.h
```

**🤖 Agent**：二维矩形用 **`Rect2`**（浮点坐标），定义在 `core/math/rect2.h`。

如果需要整数坐标版本，用 **`Rect2i`**（`core/math/rect2i.h`）。


# q10 · code_retrieval · arm: `kb`

**题**：二维矩形用哪个类？  ·  **gold**：Rect2
**答对**：✓  ·  **答案**：`Rect2`（定义在 `core/math/rect2.h`），轴对齐二维矩形，由 `position` 和 `size` 描述。
**指标**：tokens=1664 · llm_calls=5 · tool_steps=4 · 耗时=30.2s · 截断=否

---

**👤 用户**：二维矩形用哪个类？

> 💭 **思考**：用户问的是Godot中二维矩形用哪个类。让我搜索一下。

**🔧 `cmm_search`**({"query": "2D rectangle"})

> 💭 **思考**：搜索结果没有直接返回 Rect2 类。让我再搜索一下 Rect2。

**🔧 `cmm_search`**({"query": "Rect2 axis-aligned 2D bounding box"})

**🔧 `read_file`**({"path": "core/math/rect2.h"})

> 💭 **思考**：让我用正确的路径试试。

**🔧 `cmm_search`**({"query": "Rect2 class definition position size"})

**🤖 Agent**：`Rect2`（定义在 `core/math/rect2.h`），轴对齐二维矩形，由 `position` 和 `size` 描述。

**📋 工具结果**：
```
- interpolate_transform_2d  (Users-ks_128-Documents-godot-src-core.math.transform_interpolator.TransformInterpolator.interpolate_transform_2d)  math/transform_interpolator.cpp
- triangulate  (Users-ks_128-Documents-godot-src-core.math.delaunay_2d.Delaunay2D.triangulate)  math/delaunay_2d.h
- operator<  (Users-ks_128-Documents-godot-src-core.math.geometry_2d._AtlasWorkRect.operator<)  math/geometry_2d.cpp
- Transform2D  (Users-ks_128-Documents-godot-src-core.math.transform_2d.Transform2D.Transform2D)  math/transform_2d.cpp
- operator*=  (Users-ks_128-Documents-godot-src-core.math.transform_2d.T
```

**📋 工具结果**：
```
- get_aligned_address  (Users-ks_128-Documents-godot-src-core.os.memory.get_aligned_address)  os/memory.h
- build_box_planes  (Users-ks_128-Documents-godot-src-core.core_bind.Geometry3D.build_box_planes)  core_bind.cpp
- alloc_aligned_static  (Users-ks_128-Documents-godot-src-core.os.memory.Memory.alloc_aligned_static)  os/memory.cpp
- realloc_aligned_static  (Users-ks_128-Documents-godot-src-core.os.memory.Memory.realloc_aligned_static)  os/memory.cpp
- free_aligned_static  (Users-ks_128-Documents-godot-src-core.os.memory.Memory.free_aligned_static)  os/memory.cpp
```

**📋 工具结果**：
```
(read error: [Errno 2] No such file or directory: 'core/math/rect2.h')
```

**📋 工具结果**：
```
- get_position  (Users-ks_128-Documents-godot-src-core.math.rect2.Rect2.get_position)  math/rect2.h
- set_position  (Users-ks_128-Documents-godot-src-core.math.rect2.Rect2.set_position)  math/rect2.h
- get_size  (Users-ks_128-Documents-godot-src-core.math.rect2.Rect2.get_size)  math/rect2.h
- set_size  (Users-ks_128-Documents-godot-src-core.math.rect2.Rect2.set_size)  math/rect2.h
- _ignore_definition  (Users-ks_128-Documents-godot-src-core.io.xml_parser.XMLParser._ignore_definition)  io/xml_parser.cpp
```


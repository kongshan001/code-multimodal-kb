# q08 · code_retrieval · arm: `kb+superpowers`

**题**：三维向量用哪个类？  ·  **gold**：Vector3
**答对**：✓  ·  **答案**：用 **`Vector3`**（`math/vector3.h`）。
**指标**：tokens=580 · llm_calls=3 · tool_steps=2 · 耗时=16.04s · 截断=否

---

**👤 用户**：三维向量用哪个类？

> 💭 **思考**：用户问三维向量用哪个类。这是 Godot 的基础知识，但我用工具确认一下。

**🔧 `cmm_search`**({"query": "3D vector class"})

> 💭 **思考**：That returned the templated `Vector<T>` container, not the 3D vector. Let me search more specifically.

**🔧 `cmm_search`**({"query": "Vector3 xyz three-dimensional geometry vector"})

**🤖 Agent**：用 **`Vector3`**（`math/vector3.h`）。

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
- Vector3  (Users-ks_128-Documents-godot-src-core.math.vector3.Vector3)  math/vector3.h
- Vector  (Users-ks_128-Documents-godot-src-core.templates.vector.Vector.Vector)  templates/vector.h
- wrap_geometry  (Users-ks_128-Documents-godot-src-core.math.geometry_3d.Geometry3D.wrap_geometry)  math/geometry_3d.cpp
- rotate  (Users-ks_128-Documents-godot-src-core.math.vector3.Vector3.rotate)  math/vector3.cpp
- rotated  (Users-ks_128-Documents-godot-src-core.math.vector3.Vector3.rotated)  math/vector3.cpp
```


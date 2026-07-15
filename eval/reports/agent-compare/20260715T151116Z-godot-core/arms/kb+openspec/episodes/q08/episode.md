# q08 · code_retrieval · arm: `kb+openspec`

**题**：三维向量用哪个类？  ·  **gold**：Vector3
**答对**：✓  ·  **答案**：三维向量用 **`Vector3`**（`core/math/vector3.h`）。

注：还有一个模板容器也叫 `Vector`（`core/templates/vector.h`），那是动态数组不是三维向量，别混淆。
**指标**：tokens=896 · llm_calls=4 · tool_steps=3 · 耗时=20.91s · 截断=否

---

**👤 用户**：三维向量用哪个类？

> 💭 **思考**：用户问的是 Godot 中三维向量用哪个类。这是一个简单的问答问题，不需要开 spec。让我直接搜索。

**🔧 `cmm_search`**({"query": "3D vector class"})

**🔧 `cmm_search`**({"query": "Vector3 x y z float 3-dimensional"})

**🔧 `cmm_search`**({"query": "Vector3 vector3"})

**🤖 Agent**：三维向量用 **`Vector3`**（`core/math/vector3.h`）。

注：还有一个模板容器也叫 `Vector`（`core/templates/vector.h`），那是动态数组不是三维向量，别混淆。

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
- intersect_3  (Users-ks_128-Documents-godot-src-core.math.plane.Plane.intersect_3)  math/plane.cpp
- intersect_3_bind  (Users-ks_128-Documents-godot-src-core.math.plane.Plane.intersect_3_bind)  math/plane.cpp
- median_of_3_index  (Users-ks_128-Documents-godot-src-core.templates.sort_array.SortArray.median_of_3_index)  templates/sort_array.h
- get_z_far  (Users-ks_128-Documents-godot-src-core.math.projection.Projection.get_z_far)  math/projection.cpp
- get_z_near  (Users-ks_128-Documents-godot-src-core.math.projection.Projection.get_z_near)  math/projection.cpp
```

**📋 工具结果**：
```
- Vector3  (Users-ks_128-Documents-godot-src-core.math.vector3.Vector3)  math/vector3.h
- rotate  (Users-ks_128-Documents-godot-src-core.math.vector3.Vector3.rotate)  math/vector3.cpp
- rotated  (Users-ks_128-Documents-godot-src-core.math.vector3.Vector3.rotated)  math/vector3.cpp
- snap  (Users-ks_128-Documents-godot-src-core.math.vector3.Vector3.snap)  math/vector3.cpp
- snapped  (Users-ks_128-Documents-godot-src-core.math.vector3.Vector3.snapped)  math/vector3.cpp
```


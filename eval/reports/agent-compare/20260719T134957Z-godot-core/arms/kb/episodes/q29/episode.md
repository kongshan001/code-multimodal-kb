# q29 · bug_fix · arm: `kb`

- **题**：A* 寻路在两点间返回了错误路径，忽略了一个障碍物。Godot 里负责计算寻路路径的是哪个类？
- **gold**：AStar, core/math/a_star.h
- **答对**：✓
- **答案**：`AStar2D`、`AStar3D`
- **指标**：tokens=10666 · llm_calls=7 · tool_steps=6 · 耗时=13.98s · 截断=否

---

**👤 用户**：A* 寻路在两点间返回了错误路径，忽略了一个障碍物。Godot 里负责计算寻路路径的是哪个类？

> 💭 **思考**：用户在问 Godot 中负责计算寻路路径的类，特别是 A* 寻路。我需要搜索相关的类。

在 Godot 中，A* 寻路通常与导航系统相关。让我搜索一下相关的符号。

**🔧 `cmm_search`**({"query": "A* pathfinding navigation path calculate"})

> 💭 **思考**：这个搜索结果不太对，返回的是 RBMap 和 RBSet 的 depth 计算，不是寻路相关的。让我换个搜索词试试，用 "navigation" 或者 "pathfinding" 或者 "astar" 之类的。

**🔧 `cmm_search`**({"query": "AStar navigation path"})

> 💭 **思考**：这返回的也是 NodePath 和 Resource 相关的，不是我想要的寻路类。让我试试更具体的搜索词，比如 "navigation" 或者 "navmesh"。

**🔧 `cmm_search`**({"query": "navigation mesh navmesh"})

> 💭 **思考**：还是没有找到导航相关的。让我试试直接搜索 "AStar" 这个类名。

**🔧 `cmm_search`**({"query": "AStar class"})

> 💭 **思考**：太好了！找到了 AStar2D 类。让我再搜索一下是否还有其他的 AStar 相关类，比如 AStar3D 或者 AStar。

**🔧 `cmm_search`**({"query": "AStar"})

> 💭 **思考**：只找到了 AStar2D。让我搜索一下是否有 AStar3D 或其他的变体。

**🔧 `cmm_search`**({"query": "AStar3D"})

> 💭 **思考**：太好了！找到了 AStar3D 类。现在我已经找到了两个主要的 A* 寻路类：AStar2D 和 AStar3D。

用户问的是"负责计算寻路路径的类"，这些就是答案。根据收敛纪律，我应该立即回答，用符号名。

**🤖 Agent**：`AStar2D`、`AStar3D`

**📋 工具结果**：
```
- _calculate_depth  (Users-ks_128-Documents-godot-src-core.templates.rb_map.RBMap._calculate_depth)  templates/rb_map.h
- calculate_depth  (Users-ks_128-Documents-godot-src-core.templates.rb_map.RBMap.calculate_depth)  templates/rb_map.h
- _calculate_depth  (Users-ks_128-Documents-godot-src-core.templates.rb_set.RBSet._calculate_depth)  templates/rb_set.h
- calculate_depth  (Users-ks_128-Documents-godot-src-core.templates.rb_set.RBSet.calculate_depth)  templates/rb_set.h
- calculate_size  (Users-ks_128-Documents-godot-src-core.math.bvh_abb.BVH_ABB.calculate_size)  math/bvh_abb.h
```

**📋 工具结果**：
```
- rel_path_to  (Users-ks_128-Documents-godot-src-core.string.node_path.NodePath.rel_path_to)  string/node_path.cpp
- get_as_property_path  (Users-ks_128-Documents-godot-src-core.string.node_path.NodePath.get_as_property_path)  string/node_path.cpp
- set_path  (Users-ks_128-Documents-godot-src-core.io.resource.Resource.set_path)  io/resource.cpp
- get_path  (Users-ks_128-Documents-godot-src-core.io.resource.Resource.get_path)  io/resource.cpp
- _set_path  (Users-ks_128-Documents-godot-src-core.io.resource.Resource._set_path)  io/resource.cpp
```

**📋 工具结果**：
```
- TriangleMesh  (Users-ks_128-Documents-godot-src-core.math.triangle_mesh.TriangleMesh.TriangleMesh)  math/triangle_mesh.cpp
- build_convex_mesh  (Users-ks_128-Documents-godot-src-core.math.geometry_3d.Geometry3D.build_convex_mesh)  math/geometry_3d.cpp
- compute_convex_mesh_points  (Users-ks_128-Documents-godot-src-core.core_bind.Geometry3D.compute_convex_mesh_points)  core_bind.cpp
- compute_convex_mesh_points  (Users-ks_128-Documents-godot-src-core.math.geometry_3d.Geometry3D.compute_convex_mesh_points)  math/geometry_3d.cpp
- create  (Users-ks_128-Documents-godot-src-core.math.triangle_mes
```

**📋 工具结果**：
```
- astar  (Users-ks_128-Documents-godot-src-core.math.a_star.AStar2D.astar)  math/a_star.h
- class_exists  (Users-ks_128-Documents-godot-src-core.object.class_db.ClassDB.class_exists)  object/class_db.cpp
- _add_class  (Users-ks_128-Documents-godot-src-core.object.class_db.ClassDB._add_class)  object/class_db.cpp
- _is_parent_class  (Users-ks_128-Documents-godot-src-core.object.class_db.ClassDB._is_parent_class)  object/class_db.cpp
- is_parent_class  (Users-ks_128-Documents-godot-src-core.object.class_db.ClassDB.is_parent_class)  object/class_db.cpp
```

**📋 工具结果**：
```
- astar  (Users-ks_128-Documents-godot-src-core.math.a_star.AStar2D.astar)  math/a_star.h
```

**📋 工具结果**：
```
- ~AStar3D  (Users-ks_128-Documents-godot-src-core.math.a_star.AStar3D.~AStar3D)  math/a_star.cpp
- clear  (Users-ks_128-Documents-godot-src-core.math.a_star.AStar3D.clear)  math/a_star.cpp
- _solve  (Users-ks_128-Documents-godot-src-core.math.a_star.AStar3D._solve)  math/a_star.cpp
- hash  (Users-ks_128-Documents-godot-src-core.math.a_star.AStar3D.Segment.hash)  math/a_star.h
- operator==  (Users-ks_128-Documents-godot-src-core.math.a_star.AStar3D.Segment.operator==)  math/a_star.h
```


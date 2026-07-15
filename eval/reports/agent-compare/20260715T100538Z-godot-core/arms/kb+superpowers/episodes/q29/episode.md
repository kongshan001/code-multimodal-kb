# q29 · bug_fix · arm: `kb+superpowers`

**题**：Pathfinding returns a wrong path between two points, ignoring an obstacle. Which class computes the path?  ·  **gold**：AStar, core/math/a_star.h
**答对**：✓  ·  **答案**：The path is computed by one of these A* pathfinding classes:

- **`AStar3D`** — `core/math/a_star.cpp`
- **`AStar2D`** —
**指标**：tokens=1338 · llm_calls=4 · tool_steps=3 · 耗时=23.52s · 截断=否

---

**👤 用户**：Pathfinding returns a wrong path between two points, ignoring an obstacle. Which class computes the path?

> 💭 **思考**：The user is asking about which class computes the path in pathfinding in Godot. Let me search for this.

**🔧 `cmm_search`**({"query": "pathfinding compute path between points avoid obstacles"})

> 💭 **思考**：That didn't return the right results. Let me search more specifically for the pathfinding class.

**🔧 `cmm_search`**({"query": "NavigationServer path finding AStar avoidance"})

**🔧 `cmm_search`**({"query": "AStar grid path compute get_point_path"})

> 💭 **思考**：Now I have the relevant classes. The path computation classes in Godot core are:

1. `AStar` (AStar3D) - in `math/a_star.cpp`
2. `AStar2D` - in `math/a_star.cpp`
3. `AStarGrid2D` - in `math/a_star_grid_2d.cpp`
4. `NavigationServer` - the server that does navigation pathfinding

The user is asking ab

**🤖 Agent**：The path is computed by one of these A* pathfinding classes:

- **`AStar3D`** — `core/math/a_star.cpp`
- **`AStar2D`** — `core/math/a_star.cpp`
- **`AStarGrid2D`** — `core/math/a_star_grid_2d.cpp`

The path itself is returned by the **`get_point_path()`** method on each of these classes. `get_id_pat

**📋 工具结果**：
```
- get_closest_points_between_segments  (Users-ks_128-Documents-godot-src-core.core_bind.Geometry2D.get_closest_points_between_segments)  core_bind.cpp
- get_closest_points_between_segments  (Users-ks_128-Documents-godot-src-core.core_bind.Geometry3D.get_closest_points_between_segments)  core_bind.cpp
- get_closest_points_between_segments  (Users-ks_128-Documents-godot-src-core.math.geometry_2d.Geometry2D.get_closest_points_between_segments)  math/geometry_2d.h
- get_closest_points_between_segments  (Users-ks_128-Documents-godot-src-core.math.geometry_3d.Geometry3D.get_closest_points_between_se
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
- get_point_path  (Users-ks_128-Documents-godot-src-core.math.a_star_grid_2d.AStarGrid2D.get_point_path)  math/a_star_grid_2d.cpp
- get_point_path  (Users-ks_128-Documents-godot-src-core.math.a_star.AStar3D.get_point_path)  math/a_star.cpp
- get_point_path  (Users-ks_128-Documents-godot-src-core.math.a_star.AStar2D.get_point_path)  math/a_star.cpp
- _compute_cost  (Users-ks_128-Documents-godot-src-core.math.a_star_grid_2d.AStarGrid2D._compute_cost)  math/a_star_grid_2d.cpp
- set_default_compute_heuristic  (Users-ks_128-Documents-godot-src-core.math.a_star_grid_2d.AStarGrid2D.set_default_comput
```


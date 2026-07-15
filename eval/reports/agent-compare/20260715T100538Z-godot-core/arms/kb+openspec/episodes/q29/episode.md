# q29 · bug_fix · arm: `kb+openspec`

**题**：Pathfinding returns a wrong path between two points, ignoring an obstacle. Which class computes the path?  ·  **gold**：AStar, core/math/a_star.h
**答对**：✓  ·  **答案**：Path computation lives in these core classes:

- **`AStar3D`** / **`AStar2D`** — generic A* graph; path via `get_id_path
**指标**：tokens=2346 · llm_calls=5 · tool_steps=4 · 耗时=29.53s · 截断=否

---

**👤 用户**：Pathfinding returns a wrong path between two points, ignoring an obstacle. Which class computes the path?

> 💭 **思考**：The user is asking about which class in Godot core computes paths for pathfinding. Let me search for this.

**🔧 `cmm_search`**({"query": "pathfinding compute path between points obstacle"})

> 💭 **思考**：That didn't give the right results. Let me search more specifically for the navigation/pathfinding path computation.

**🔧 `cmm_search`**({"query": "NavigationServer find path AStar"})

> 💭 **思考**：The search isn't great. Let me search for the specific pathfinding classes.

**🔧 `cmm_search`**({"query": "AStarGrid2D get_id_path pathfinding grid"})

**🔧 `cmm_search`**({"query": "NavigationRegion map_get_path route computation"})

> 💭 **思考**：Got it. The relevant pathfinding classes in Godot core are:
- `AStar` (AStar3D) — math/a_star.cpp
- `AStar2D` — math/a_star.cpp
- `AStarGrid2D` — math/a_star_grid_2d.cpp

And there's likely `NavigationServer3D` for navigation path. Let me give a concise answer.

**🤖 Agent**：Path computation lives in these core classes:

- **`AStar3D`** / **`AStar2D`** — generic A* graph; path via `get_id_path()` / `get_point_path()` (core/math/a_star.cpp)
- **`AStarGrid2D`** — grid-based A*; same `get_id_path()` / `get_point_path()` API (core/math/a_star_grid_2d.cpp)
- **`NavigationSer

**📋 工具结果**：
```
- get_closest_points_between_segments  (Users-ks_128-Documents-godot-src-core.core_bind.Geometry2D.get_closest_points_between_segments)  core_bind.cpp
- get_closest_points_between_segments  (Users-ks_128-Documents-godot-src-core.core_bind.Geometry3D.get_closest_points_between_segments)  core_bind.cpp
- get_closest_points_between_segments  (Users-ks_128-Documents-godot-src-core.math.geometry_2d.Geometry2D.get_closest_points_between_segments)  math/geometry_2d.h
- get_closest_points_between_segments  (Users-ks_128-Documents-godot-src-core.math.geometry_3d.Geometry3D.get_closest_points_between_se
```

**📋 工具结果**：
```
- find  (Users-ks_128-Documents-godot-src-core.templates.span.find)  templates/span.h
- find  (Users-ks_128-Documents-godot-src-core.string.ustring.String.find)  string/ustring.cpp
- find  (Users-ks_128-Documents-godot-src-core.templates.vector.Vector.find)  templates/vector.h
- _find  (Users-ks_128-Documents-godot-src-core.templates.vset.VSet._find)  templates/vset.h
- find  (Users-ks_128-Documents-godot-src-core.templates.vset.VSet.find)  templates/vset.h
```

**📋 工具结果**：
```
- get_id_path  (Users-ks_128-Documents-godot-src-core.math.a_star_grid_2d.AStarGrid2D.get_id_path)  math/a_star_grid_2d.cpp
- get_id_path  (Users-ks_128-Documents-godot-src-core.io.resource_uid.ResourceUID.get_id_path)  io/resource_uid.cpp
- get_id_path  (Users-ks_128-Documents-godot-src-core.math.a_star.AStar3D.get_id_path)  math/a_star.cpp
- get_id_path  (Users-ks_128-Documents-godot-src-core.math.a_star.AStar2D.get_id_path)  math/a_star.cpp
- update  (Users-ks_128-Documents-godot-src-core.math.a_star_grid_2d.AStarGrid2D.update)  math/a_star_grid_2d.cpp
```

**📋 工具结果**：
```
(no results)
```


# q29 · bug_fix · arm: `kb`

**题**：Pathfinding returns a wrong path between two points, ignoring an obstacle. Which class computes the path?  ·  **gold**：AStar, core/math/a_star.h
**答对**：✓  ·  **答案**：In Godot core, pathfinding between two points is computed by one of these classes depending on the approach:

**Generic 
**指标**：tokens=3065 · llm_calls=8 · tool_steps=7 · 耗时=41.28s · 截断=否

---

**👤 用户**：Pathfinding returns a wrong path between two points, ignoring an obstacle. Which class computes the path?

> 💭 **思考**：The user is asking about which class computes the path in Godot's pathfinding system. Let me search for this.

**🔧 `cmm_search`**({"query": "pathfinding navigation path computation between points"})

> 💭 **思考**：That's not quite what I want. Let me search more specifically for the navigation path computation, like A* or NavMesh.

**🔧 `cmm_search`**({"query": "NavigationServer compute path A* obstacle avoidance"})

**🔧 `cmm_search`**({"query": "AStar grid map find path heuristic"})

> 💭 **思考**：Let me search more directly for the navigation path computation class.

**🔧 `cmm_search`**({"query": "NavMesh path corridor funnel seek"})

**🔧 `cmm_search`**({"query": "map_get_path NavigationServer map_get_simple_path"})

**🔧 `cmm_search`**({"query": "navigation pathfinding server map region bake"})

**🔧 `cmm_search`**({"query": "get_point_path get_id_path AStar"})

> 💭 **思考**：I've found the relevant classes. The pathfinding classes in Godot core that compute paths are:

1. **AStar3D** / **AStar2D** — generic A* graph pathfinders (with `get_point_path`, `get_id_path`, `_compute_cost`)
2. **AStarGrid2D** — grid-based A* with heuristic options

For navigation mesh-based pat

**🤖 Agent**：In Godot core, pathfinding between two points is computed by one of these classes depending on the approach:

**Generic A\* (graph-based)**
- `AStar3D` / `AStar2D` — methods `get_id_path()` / `get_point_path()`, with cost via `_compute_cost()` and `_estimate_cost()`
- `AStarGrid2D` — grid variant; s

**📋 工具结果**：
```
- get_closest_points_between_segments  (Users-ks_128-Documents-godot-src-core.core_bind.Geometry2D.get_closest_points_between_segments)  core_bind.cpp
- get_closest_points_between_segments  (Users-ks_128-Documents-godot-src-core.core_bind.Geometry3D.get_closest_points_between_segments)  core_bind.cpp
- get_closest_points_between_segments  (Users-ks_128-Documents-godot-src-core.math.geometry_2d.Geometry2D.get_closest_points_between_segments)  math/geometry_2d.h
- get_closest_points_between_segments  (Users-ks_128-Documents-godot-src-core.math.geometry_3d.Geometry3D.get_closest_points_between_se
```

**📋 工具结果**：
```
- _compute_cost  (Users-ks_128-Documents-godot-src-core.math.a_star.AStar3D._compute_cost)  math/a_star.cpp
- _compute_cost  (Users-ks_128-Documents-godot-src-core.math.a_star.AStar2D._compute_cost)  math/a_star.cpp
- _compute_cost  (Users-ks_128-Documents-godot-src-core.math.a_star_grid_2d.AStarGrid2D._compute_cost)  math/a_star_grid_2d.cpp
- set_default_compute_heuristic  (Users-ks_128-Documents-godot-src-core.math.a_star_grid_2d.AStarGrid2D.set_default_compute_heuristic)  math/a_star_grid_2d.cpp
- get_default_compute_heuristic  (Users-ks_128-Documents-godot-src-core.math.a_star_grid_2d.ASta
```

**📋 工具结果**：
```
- heuristic_euclidean  (Users-ks_128-Documents-godot-src-core.math.a_star_grid_2d.heuristic_euclidean)  math/a_star_grid_2d.cpp
- heuristic_manhattan  (Users-ks_128-Documents-godot-src-core.math.a_star_grid_2d.heuristic_manhattan)  math/a_star_grid_2d.cpp
- heuristic_octile  (Users-ks_128-Documents-godot-src-core.math.a_star_grid_2d.heuristic_octile)  math/a_star_grid_2d.cpp
- heuristic_chebyshev  (Users-ks_128-Documents-godot-src-core.math.a_star_grid_2d.heuristic_chebyshev)  math/a_star_grid_2d.cpp
- set_default_compute_heuristic  (Users-ks_128-Documents-godot-src-core.math.a_star_grid_2d.AS
```

**📋 工具结果**：
```
- seek  (Users-ks_128-Documents-godot-src-core.io.stream_peer.StreamPeerBuffer.seek)  io/stream_peer.cpp
- seek  (Users-ks_128-Documents-godot-src-core.io.xml_parser.XMLParser.seek)  io/xml_parser.cpp
- seek  (Users-ks_128-Documents-godot-src-core.io.file_access_compressed.FileAccessCompressed.seek)  io/file_access_compressed.cpp
- seek  (Users-ks_128-Documents-godot-src-core.io.file_access_encrypted.FileAccessEncrypted.seek)  io/file_access_encrypted.cpp
- seek  (Users-ks_128-Documents-godot-src-core.io.file_access_memory.FileAccessMemory.seek)  io/file_access_memory.cpp
```

**📋 工具结果**：
```
(no results)
```

**📋 工具结果**：
```
- get_region  (Users-ks_128-Documents-godot-src-core.io.image.Image.get_region)  io/image.cpp
- set_region  (Users-ks_128-Documents-godot-src-core.math.a_star_grid_2d.AStarGrid2D.set_region)  math/a_star_grid_2d.cpp
- get_region  (Users-ks_128-Documents-godot-src-core.math.a_star_grid_2d.AStarGrid2D.get_region)  math/a_star_grid_2d.cpp
- fill_solid_region  (Users-ks_128-Documents-godot-src-core.math.a_star_grid_2d.AStarGrid2D.fill_solid_region)  math/a_star_grid_2d.cpp
- fill_weight_scale_region  (Users-ks_128-Documents-godot-src-core.math.a_star_grid_2d.AStarGrid2D.fill_weight_scale_region)  
```

**📋 工具结果**：
```
- get_point_path  (Users-ks_128-Documents-godot-src-core.math.a_star.AStar3D.get_point_path)  math/a_star.cpp
- get_point_path  (Users-ks_128-Documents-godot-src-core.math.a_star.AStar2D.get_point_path)  math/a_star.cpp
- get_id_path  (Users-ks_128-Documents-godot-src-core.io.resource_uid.ResourceUID.get_id_path)  io/resource_uid.cpp
- get_id_path  (Users-ks_128-Documents-godot-src-core.math.a_star.AStar3D.get_id_path)  math/a_star.cpp
- get_id_path  (Users-ks_128-Documents-godot-src-core.math.a_star.AStar2D.get_id_path)  math/a_star.cpp
```


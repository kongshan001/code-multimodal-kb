# q29 · bug_fix · arm: `kb+openspec`

**题**：A* 寻路在两点间返回了错误路径，忽略了一个障碍物。Godot 里负责计算寻路路径的是哪个类？  ·  **gold**：AStar, core/math/a_star.h
**答对**：✓  ·  **答案**：Godot 中负责 A* 寻路路径计算的类是 **`AStar3D`**（位于 `core/math/a_star.h` / `a_star.cpp`），对应 2D 场景的是 **`AStar2D`**。

核心方法包括：
- `get_p
**指标**：tokens=1595 · llm_calls=2 · tool_steps=1 · 耗时=17.02s · 截断=否

---

**👤 用户**：A* 寻路在两点间返回了错误路径，忽略了一个障碍物。Godot 里负责计算寻路路径的是哪个类？

> 💭 **思考**：The user is asking which class in Godot is responsible for A* pathfinding calculation. Let me search for this.

**🔧 `cmm_search`**({"query": "A* pathfinding calculate path between points"})

> 💭 **思考**：The search returned `AStar3D` class in `math/a_star.cpp`. Let me confirm this.

**🤖 Agent**：Godot 中负责 A* 寻路路径计算的类是 **`AStar3D`**（位于 `core/math/a_star.h` / `a_star.cpp`），对应 2D 场景的是 **`AStar2D`**。

核心方法包括：
- `get_path(from_id, to_id)` — 计算两点间路径
- `get_id_path(from_id, to_id)` — 返回点 ID 路径
- `connect_points` / `disconnect_points` — 管理点之间的连通性
- `add_point` / `remove_point` — 管理导航点

障碍物的表现取决于你通过

**📋 工具结果**：
```
- get_closest_points_between_segments  (Users-ks_128-Documents-godot-src-core.core_bind.Geometry2D.get_closest_points_between_segments)  core_bind.cpp
- get_closest_points_between_segments  (Users-ks_128-Documents-godot-src-core.core_bind.Geometry3D.get_closest_points_between_segments)  core_bind.cpp
- get_closest_points_between_segments  (Users-ks_128-Documents-godot-src-core.math.geometry_2d.Geometry2D.get_closest_points_between_segments)  math/geometry_2d.h
- get_closest_points_between_segments  (Users-ks_128-Documents-godot-src-core.math.geometry_3d.Geometry3D.get_closest_points_between_se
```


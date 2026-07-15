# q29 · bug_fix · arm: `kb+superpowers`

**题**：A* 寻路在两点间返回了错误路径，忽略了一个障碍物。Godot 里负责计算寻路路径的是哪个类？  ·  **gold**：AStar, core/math/a_star.h
**答对**：✓  ·  **答案**：Godot 中负责 A* 寻路路径计算的类有三个，均在 `core/math/` 下：

| 类 | 文件 | 用途 |
|---|---|---|
| **`AStar3D`** | `math/a_star.cpp` | 3D A* 寻
**指标**：tokens=1644 · llm_calls=3 · tool_steps=2 · 耗时=16.78s · 截断=否

---

**👤 用户**：A* 寻路在两点间返回了错误路径，忽略了一个障碍物。Godot 里负责计算寻路路径的是哪个类？

**🔧 `cmm_search`**({"query": "A* pathfinding navigation compute path"})

**📋 工具结果**：
```
- _compute_cost  (Users-ks_128-Documents-godot-src-core.math.a_star.AStar3D._compute_cost)  math/a_star.cpp
- _compute_cost  (Users-ks_128-Documents-godot-src-core.math.a_star.AStar2D._compute_cost)  math/a_star.cpp
- _compute_cost  (Users-ks_128-Documents-godot-src-core.math.a_star_grid_2d.AStarGrid2D._compute_cost)  math/a_star_grid_2d.cpp
- set_default_compute_heuristic  (Users-ks_128-Documents-godot-src-core.math.a_star_grid_2d.AStarGrid2D.set_default_compute_heuristic)  math/a_star_grid_2d.cpp
- get_default_compute_heuristic  (Users-ks_128-Documents-godot-src-core.math.a_star_grid_2d.ASta
```

**🔧 `cmm_search`**({"query": "AStar get_id_path get_point_path obstacle"})

**📋 工具结果**：
```
- get_point_path  (Users-ks_128-Documents-godot-src-core.math.a_star.AStar3D.get_point_path)  math/a_star.cpp
- get_point_path  (Users-ks_128-Documents-godot-src-core.math.a_star.AStar2D.get_point_path)  math/a_star.cpp
- get_id_path  (Users-ks_128-Documents-godot-src-core.io.resource_uid.ResourceUID.get_id_path)  io/resource_uid.cpp
- get_id_path  (Users-ks_128-Documents-godot-src-core.math.a_star.AStar3D.get_id_path)  math/a_star.cpp
- get_id_path  (Users-ks_128-Documents-godot-src-core.math.a_star.AStar2D.get_id_path)  math/a_star.cpp
```

**🤖 Agent**：Godot 中负责 A* 寻路路径计算的类有三个，均在 `core/math/` 下：

| 类 | 文件 | 用途 |
|---|---|---|
| **`AStar3D`** | `math/a_star.cpp` | 3D A* 寻路 |
| **`AStar2D`** | `math/a_star.cpp` | 2D A* 寻路 |
| **`AStarGrid2D`** | `math/a_star_grid_2d.cpp` | 2D 网格专用 A* |

核心方法：
- **`get_id_path()`** — 返回点 ID 路径
- **`get_point_path()`*


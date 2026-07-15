# q29 · bug_fix · arm: `kb`

**题**：A* 寻路在两点间返回了错误路径，忽略了一个障碍物。Godot 里负责计算寻路路径的是哪个类？  ·  **gold**：AStar, core/math/a_star.h
**答对**：✓  ·  **答案**：Godot 中负责 A* 寻路路径计算的类有三个：

- **`AStar3D`** — 3D 空间的 A* 寻路（`math/a_star.cpp`）
- **`AStar2D`** — 2D 空间的 A* 寻路（`math/a_star
**指标**：tokens=851 · llm_calls=2 · tool_steps=1 · 耗时=10.64s · 截断=否

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

**🤖 Agent**：Godot 中负责 A* 寻路路径计算的类有三个：

- **`AStar3D`** — 3D 空间的 A* 寻路（`math/a_star.cpp`）
- **`AStar2D`** — 2D 空间的 A* 寻路（`math/a_star.cpp`）
- **`AStarGrid2D`** — 2D 网格专用 A* 寻路（`math/a_star_grid_2d.cpp`）

核心方法都是 `get_id_path()`（返回路径点序列）。如果路径忽略了障碍物，应检查：
1. 障碍物对应的点是否通过 `set_point_disabled()` 正确标记为不可通行。
2. 自定义代价函数 `


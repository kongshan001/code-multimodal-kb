# q29 · bug_fix · arm: `kb+superpowers`

**题**：A* 寻路在两点间返回了错误路径，忽略了一个障碍物。Godot 里负责计算寻路路径的是哪个类？  ·  **gold**：AStar, core/math/a_star.h
**答对**：✓  ·  **答案**：Godot 中负责 A* 寻路路径计算的类有：

- **`AStar3D`** — 3D 空间的 A* 寻路（`math/a_star.cpp`）
- **`AStar2D`** — 2D 空间的 A* 寻路（`math/a_star.c
**指标**：tokens=712 · llm_calls=2 · tool_steps=1 · 耗时=22.98s · 截断=否

---

**👤 用户**：A* 寻路在两点间返回了错误路径，忽略了一个障碍物。Godot 里负责计算寻路路径的是哪个类？

> 💭 **思考**：The user is asking which class in Godot is responsible for computing A* pathfinding paths. Let me search for this.

**🔧 `cmm_search`**({"query": "A* pathfinding navigation path compute"})

> 💭 **思考**：The search returned A* related classes. The main classes responsible for A* pathfinding in Godot are:
- `AStar3D` (math/a_star.cpp)
- `AStar2D` (math/a_star.cpp)
- `AStarGrid2D` (math/a_star_grid_2d.cpp)

The user is asking about which class computes the pathfinding path. These are the core A* imple

**🤖 Agent**：Godot 中负责 A* 寻路路径计算的类有：

- **`AStar3D`** — 3D 空间的 A* 寻路（`math/a_star.cpp`）
- **`AStar2D`** — 2D 空间的 A* 寻路（`math/a_star.cpp`）
- **`AStarGrid2D`** — 2D 网格专用 A* 寻路（`math/a_star_grid_2d.cpp`）

如果需要导航系统（NavigationServer 端）的路径计算，则是 **`NavigationServer3D`** / **`NavigationServer2D`**，它们底层调用 `navmesh` 做路径查找

**📋 工具结果**：
```
- _compute_cost  (Users-ks_128-Documents-godot-src-core.math.a_star.AStar3D._compute_cost)  math/a_star.cpp
- _compute_cost  (Users-ks_128-Documents-godot-src-core.math.a_star.AStar2D._compute_cost)  math/a_star.cpp
- _compute_cost  (Users-ks_128-Documents-godot-src-core.math.a_star_grid_2d.AStarGrid2D._compute_cost)  math/a_star_grid_2d.cpp
- set_default_compute_heuristic  (Users-ks_128-Documents-godot-src-core.math.a_star_grid_2d.AStarGrid2D.set_default_compute_heuristic)  math/a_star_grid_2d.cpp
- get_default_compute_heuristic  (Users-ks_128-Documents-godot-src-core.math.a_star_grid_2d.ASta
```


# q29 · bug_fix · arm: `kb`

**题**：A* 寻路在两点间返回了错误路径，忽略了一个障碍物。Godot 里负责计算寻路路径的是哪个类？  ·  **gold**：AStar, core/math/a_star.h
**答对**：✓  ·  **答案**：Godot 中负责 A* 寻路路径计算的有三个类（均在 `core/math/`）：

- **`AStar`** — 通用 3D A* 寻路（`math/a_star.cpp`）
- **`AStar2D`** — 2D 版本（`math
**指标**：tokens=1312 · llm_calls=2 · tool_steps=1 · 耗时=9.47s · 截断=否

---

**👤 用户**：A* 寻路在两点间返回了错误路径，忽略了一个障碍物。Godot 里负责计算寻路路径的是哪个类？

> 💭 **思考**：The user is asking about which class in Godot is responsible for A* pathfinding calculation. Let me search for it.

**🔧 `cmm_search`**({"query": "A* pathfinding compute path"})

> 💭 **思考**：The results show three A* classes in Godot: AStar3D, AStar2D, and AStarGrid2D. These are the classes responsible for A* pathfinding in Godot.

**🤖 Agent**：Godot 中负责 A* 寻路路径计算的有三个类（均在 `core/math/`）：

- **`AStar`** — 通用 3D A* 寻路（`math/a_star.cpp`）
- **`AStar2D`** — 2D 版本（`math/a_star.cpp`）
- **`AStarGrid2D`** — 2D 网格专用 A*（`math/a_star_grid_2d.cpp`）

根据你的场景（2D 网格、障碍物被忽略），最可能涉及的是 **`AStarGrid2D`**，也可能用了 `AStar2D`。核心路径计算方法都是 `get_id_path()` / `get_point_pa

**📋 工具结果**：
```
- _compute_cost  (Users-ks_128-Documents-godot-src-core.math.a_star.AStar3D._compute_cost)  math/a_star.cpp
- _compute_cost  (Users-ks_128-Documents-godot-src-core.math.a_star.AStar2D._compute_cost)  math/a_star.cpp
- _compute_cost  (Users-ks_128-Documents-godot-src-core.math.a_star_grid_2d.AStarGrid2D._compute_cost)  math/a_star_grid_2d.cpp
- set_default_compute_heuristic  (Users-ks_128-Documents-godot-src-core.math.a_star_grid_2d.AStarGrid2D.set_default_compute_heuristic)  math/a_star_grid_2d.cpp
- get_default_compute_heuristic  (Users-ks_128-Documents-godot-src-core.math.a_star_grid_2d.ASta
```


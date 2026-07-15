# q29 · bug_fix · arm: `no-kb`

**题**：A* 寻路在两点间返回了错误路径，忽略了一个障碍物。Godot 里负责计算寻路路径的是哪个类？  ·  **gold**：AStar, core/math/a_star.h
**答对**：✓  ·  **答案**：负责 A* 寻路计算的类是：

- **`AStar`** — 定义在 `core/math/a_star.h`，通用的 3D A* 寻路。
- **`AStarGrid2D`** — 定义在 `core/math/a_star_grid_
**指标**：tokens=1071 · llm_calls=2 · tool_steps=1 · 耗时=9.7s · 截断=否

---

**👤 用户**：A* 寻路在两点间返回了错误路径，忽略了一个障碍物。Godot 里负责计算寻路路径的是哪个类？

> 💭 **思考**：The user is asking about which class in Godot is responsible for A* pathfinding. Let me search for it.

**🔧 `grep_code`**({"pattern": "class AStar"})

> 💭 **思考**：Found it. There are two classes: `AStar` (in `a_star.h`) and `AStarGrid2D` (in `a_star_grid_2d.h`).

**🤖 Agent**：负责 A* 寻路计算的类是：

- **`AStar`** — 定义在 `core/math/a_star.h`，通用的 3D A* 寻路。
- **`AStarGrid2D`** — 定义在 `core/math/a_star_grid_2d.h`，专用于 2D 网格寻路。

如果是在 2D 网格场景中遇到障碍物被忽略的问题，重点排查 **`AStarGrid2D`**（障碍物通过 `set_solid` / `set_point_solid` 标记）。

**📋 工具结果**：
```
matched 2 files:
/Users/ks_128/Documents/godot-src/core/math/a_star_grid_2d.h
/Users/ks_128/Documents/godot-src/core/math/a_star.h
```


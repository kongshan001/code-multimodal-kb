# q29 · bug_fix · arm: `no-kb`

**题**：A* 寻路在两点间返回了错误路径，忽略了一个障碍物。Godot 里负责计算寻路路径的是哪个类？  ·  **gold**：AStar, core/math/a_star.h
**答对**：✓  ·  **答案**：负责 A* 寻路路径计算的类是 **`AStar`**（通用 2D/3D 图寻路，定义在 `core/math/a_star.h`）和 **`AStarGrid2D`**（2D 网格专用，定义在 `core/math/a_star_grid
**指标**：tokens=952 · llm_calls=2 · tool_steps=1 · 耗时=13.81s · 截断=否

---

**👤 用户**：A* 寻路在两点间返回了错误路径，忽略了一个障碍物。Godot 里负责计算寻路路径的是哪个类？

**🔧 `grep_code`**({"pattern": "class AStar"})

**📋 工具结果**：
```
matched 2 files:
/Users/ks_128/Documents/godot-src/core/math/a_star_grid_2d.h
/Users/ks_128/Documents/godot-src/core/math/a_star.h
```

**🤖 Agent**：负责 A* 寻路路径计算的类是 **`AStar`**（通用 2D/3D 图寻路，定义在 `core/math/a_star.h`）和 **`AStarGrid2D`**（2D 网格专用，定义在 `core/math/a_star_grid_2d.h`）。

- `AStar` — 通用 A* 寻路，手动添加点和连接。
- `AStarGrid2D` — 基于矩形网格的 A* 寻路，支持障碍物（`set_solid`）。

如果你是在 2D 网格场景中遇到障碍物被忽略的问题，重点排查 **`AStarGrid2D`**。


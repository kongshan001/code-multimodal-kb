# q04 · code_retrieval · arm: `no-kb`

**题**：A* 寻路算法用哪个类？  ·  **gold**：AStar
**答对**：✓  ·  **答案**：Godot 中的 A* 寻路算法使用以下类：

- **`AStar`** — 通用的 A* 寻路（2D/3D 通用，自定义图结构），定义在 `core/math/a_star.h`
- **`AStar2D`** — 2D 版本
- **
**指标**：tokens=1090 · llm_calls=2 · tool_steps=1 · 耗时=24.57s · 截断=否

---

**👤 用户**：A* 寻路算法用哪个类？

> 💭 **思考**：用户问 A* 寻路算法用哪个类。让我搜索一下。

**🔧 `grep_code`**({"pattern": "AStar"})

**🤖 Agent**：Godot 中的 A* 寻路算法使用以下类：

- **`AStar`** — 通用的 A* 寻路（2D/3D 通用，自定义图结构），定义在 `core/math/a_star.h`
- **`AStar2D`** — 2D 版本
- **`AStar3D`** — 3D 版本
- **`AStarGrid2D`** — 专用于 2D 网格的 A* 寻路，定义在 `core/math/a_star_grid_2d.h`

如果需要基于网格的 2D 寻路，推荐用 `AStarGrid2D`；自定义节点图寻路则用 `AStar2D` / `AStar3D`。

**📋 工具结果**：
```
matched 6 files:
/Users/ks_128/Documents/godot-src/core/extension/gdextension_special_compat_hashes.cpp
/Users/ks_128/Documents/godot-src/core/math/a_star_grid_2d.h
/Users/ks_128/Documents/godot-src/core/math/a_star_grid_2d.cpp
/Users/ks_128/Documents/godot-src/core/math/a_star.h
/Users/ks_128/Documents/godot-src/core/math/a_star.cpp
/Users/ks_128/Documents/godot-src/core/register_core_types.cpp
```


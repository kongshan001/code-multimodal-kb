# q04 · code_retrieval · arm: `kb+openspec`

**题**：A* 寻路算法用哪个类？  ·  **gold**：AStar
**答对**：✓  ·  **答案**：Godot 中 A* 寻路用以下两个类：

- **`AStar3D`** — 3D 寻路，核心实现 `math/a_star.cpp`，内部方法 `_solve()` 执行 A* 算法
- **`AStar2D`** — 2D 寻路（`A
**指标**：tokens=1427 · llm_calls=2 · tool_steps=1 · 耗时=13.15s · 截断=否

---

**👤 用户**：A* 寻路算法用哪个类？

> 💭 **思考**：用户问 A* 寻路算法在 Godot core 中用哪个类。让我搜索一下。

**🔧 `cmm_search`**({"query": "A* pathfinding algorithm"})

> 💭 **思考**：找到了。A* 寻路算法用的是 AStar3D 类（3D）以及对应的 AStar2D（2D）。让我直接回答。

**🤖 Agent**：Godot 中 A* 寻路用以下两个类：

- **`AStar3D`** — 3D 寻路，核心实现 `math/a_star.cpp`，内部方法 `_solve()` 执行 A* 算法
- **`AStar2D`** — 2D 寻路（`AStar3D` 的 2D 封装）

**📋 工具结果**：
```
- ~AStar3D  (Users-ks_128-Documents-godot-src-core.math.a_star.AStar3D.~AStar3D)  math/a_star.cpp
- AHashMap  (Users-ks_128-Documents-godot-src-core.templates.a_hash_map.AHashMap.AHashMap)  templates/a_hash_map.h
- ~AHashMap  (Users-ks_128-Documents-godot-src-core.templates.a_hash_map.AHashMap.~AHashMap)  templates/a_hash_map.h
- clear  (Users-ks_128-Documents-godot-src-core.math.a_star.AStar3D.clear)  math/a_star.cpp
- _solve  (Users-ks_128-Documents-godot-src-core.math.a_star.AStar3D._solve)  math/a_star.cpp
```


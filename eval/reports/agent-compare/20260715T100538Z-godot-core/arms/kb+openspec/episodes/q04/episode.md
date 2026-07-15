# q04 · code_retrieval · arm: `kb+openspec`

**题**：A* 寻路算法用哪个类？  ·  **gold**：AStar
**答对**：✓  ·  **答案**：`AStar3D`（3D）和对应的 `AStar2D`（2D）。核心实现位于 `core/math/a_star.cpp`，其中 `_solve` 方法是 A* 搜索的核心逻辑。
**指标**：tokens=1366 · llm_calls=2 · tool_steps=1 · 耗时=13.36s · 截断=否

---

**👤 用户**：A* 寻路算法用哪个类？

> 💭 **思考**：The user is asking which class implements A* pathfinding algorithm in Godot core/. Let me search for it.

**🔧 `cmm_search`**({"query": "A* pathfinding algorithm"})

> 💭 **思考**：The answer is clear.

**🤖 Agent**：`AStar3D`（3D）和对应的 `AStar2D`（2D）。核心实现位于 `core/math/a_star.cpp`，其中 `_solve` 方法是 A* 搜索的核心逻辑。

**📋 工具结果**：
```
- ~AStar3D  (Users-ks_128-Documents-godot-src-core.math.a_star.AStar3D.~AStar3D)  math/a_star.cpp
- AHashMap  (Users-ks_128-Documents-godot-src-core.templates.a_hash_map.AHashMap.AHashMap)  templates/a_hash_map.h
- ~AHashMap  (Users-ks_128-Documents-godot-src-core.templates.a_hash_map.AHashMap.~AHashMap)  templates/a_hash_map.h
- clear  (Users-ks_128-Documents-godot-src-core.math.a_star.AStar3D.clear)  math/a_star.cpp
- _solve  (Users-ks_128-Documents-godot-src-core.math.a_star.AStar3D._solve)  math/a_star.cpp
```


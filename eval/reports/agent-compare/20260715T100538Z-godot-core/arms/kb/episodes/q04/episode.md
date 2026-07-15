# q04 · code_retrieval · arm: `kb`

**题**：A* 寻路算法用哪个类？  ·  **gold**：AStar
**答对**：✓  ·  **答案**：A* 寻路算法在 Godot core 中由 `AStar3D`（3D）实现，对应 2D 的变体是 `AStar2D`。核心文件是 `math/a_star.cpp`，关键方法为 `AStar3D::_solve`。
**指标**：tokens=1062 · llm_calls=2 · tool_steps=1 · 耗时=13.41s · 截断=否

---

**👤 用户**：A* 寻路算法用哪个类？

> 💭 **思考**：The user is asking which class implements the A* pathfinding algorithm in Godot.

**🔧 `cmm_search`**({"query": "A* pathfinding algorithm"})

**🤖 Agent**：A* 寻路算法在 Godot core 中由 `AStar3D`（3D）实现，对应 2D 的变体是 `AStar2D`。核心文件是 `math/a_star.cpp`，关键方法为 `AStar3D::_solve`。

**📋 工具结果**：
```
- ~AStar3D  (Users-ks_128-Documents-godot-src-core.math.a_star.AStar3D.~AStar3D)  math/a_star.cpp
- AHashMap  (Users-ks_128-Documents-godot-src-core.templates.a_hash_map.AHashMap.AHashMap)  templates/a_hash_map.h
- ~AHashMap  (Users-ks_128-Documents-godot-src-core.templates.a_hash_map.AHashMap.~AHashMap)  templates/a_hash_map.h
- clear  (Users-ks_128-Documents-godot-src-core.math.a_star.AStar3D.clear)  math/a_star.cpp
- _solve  (Users-ks_128-Documents-godot-src-core.math.a_star.AStar3D._solve)  math/a_star.cpp
```


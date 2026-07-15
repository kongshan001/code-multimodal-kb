# q04 · code_retrieval · arm: `kb+superpowers`

**题**：A* 寻路算法用哪个类？  ·  **gold**：AStar
**答对**：✓  ·  **答案**：A* 寻路算法使用 `AStar3D` 类（3D）和 `AStar2D` 类（2D），核心求解逻辑在 `AStar3D::_solve` 方法中，代码位于 `core/math/a_star.cpp`。
**指标**：tokens=1306 · llm_calls=2 · tool_steps=1 · 耗时=7.77s · 截断=否

---

**👤 用户**：A* 寻路算法用哪个类？

**🔧 `cmm_search`**({"query": "A* pathfinding algorithm"})

**📋 工具结果**：
```
- ~AStar3D  (Users-ks_128-Documents-godot-src-core.math.a_star.AStar3D.~AStar3D)  math/a_star.cpp
- AHashMap  (Users-ks_128-Documents-godot-src-core.templates.a_hash_map.AHashMap.AHashMap)  templates/a_hash_map.h
- ~AHashMap  (Users-ks_128-Documents-godot-src-core.templates.a_hash_map.AHashMap.~AHashMap)  templates/a_hash_map.h
- clear  (Users-ks_128-Documents-godot-src-core.math.a_star.AStar3D.clear)  math/a_star.cpp
- _solve  (Users-ks_128-Documents-godot-src-core.math.a_star.AStar3D._solve)  math/a_star.cpp
```

**🤖 Agent**：A* 寻路算法使用 `AStar3D` 类（3D）和 `AStar2D` 类（2D），核心求解逻辑在 `AStar3D::_solve` 方法中，代码位于 `core/math/a_star.cpp`。


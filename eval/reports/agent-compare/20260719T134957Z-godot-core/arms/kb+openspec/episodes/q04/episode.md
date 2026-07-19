# q04 · code_retrieval · arm: `kb+openspec`

- **题**：A* 寻路算法用哪个类？
- **gold**：AStar
- **答对**：✓
- **答案**：`AStar2D`、`AStar3D`
- **指标**：tokens=4152 · llm_calls=3 · tool_steps=2 · 耗时=8.12s · 截断=否

---

**👤 用户**：A* 寻路算法用哪个类？

> 💭 **思考**：用户问 A* 寻路算法用哪个类，这是关于 Godot 代码库的问题。我需要在 Godot core/ 中搜索与 A* 寻路相关的类。

让我用 cmm_search 工具搜索 A* 寻路算法相关的内容。

**🔧 `cmm_search`**({"query": "A* pathfinding algorithm"})

> 💭 **思考**：好的，搜索结果显示 `AStar3D` 类，这是一个 A* 寻路算法的实现。让我再搜索一下看看是否有其他的 A* 相关类，比如 AStar2D。

**🔧 `cmm_search`**({"query": "AStar2D"})

> 💭 **思考**：好的，Godot 中有两个 A* 寻路算法的类：
- `AStar2D` - 用于 2D 寻路
- `AStar3D` - 用于 3D 寻路

用户问的是 A* 寻路算法用哪个类，我需要简洁地给出答案。根据搜索结果，这两个类都是 A* 寻路算法的实现。

**🤖 Agent**：`AStar2D`、`AStar3D`

**📋 工具结果**：
```
- ~AStar3D  (Users-ks_128-Documents-godot-src-core.math.a_star.AStar3D.~AStar3D)  math/a_star.cpp
- AHashMap  (Users-ks_128-Documents-godot-src-core.templates.a_hash_map.AHashMap.AHashMap)  templates/a_hash_map.h
- ~AHashMap  (Users-ks_128-Documents-godot-src-core.templates.a_hash_map.AHashMap.~AHashMap)  templates/a_hash_map.h
- clear  (Users-ks_128-Documents-godot-src-core.math.a_star.AStar3D.clear)  math/a_star.cpp
- _solve  (Users-ks_128-Documents-godot-src-core.math.a_star.AStar3D._solve)  math/a_star.cpp
```

**📋 工具结果**：
```
- clear  (Users-ks_128-Documents-godot-src-core.math.a_star.AStar2D.clear)  math/a_star.cpp
- _solve  (Users-ks_128-Documents-godot-src-core.math.a_star.AStar2D._solve)  math/a_star.cpp
- add_point  (Users-ks_128-Documents-godot-src-core.math.a_star.AStar2D.add_point)  math/a_star.cpp
- remove_point  (Users-ks_128-Documents-godot-src-core.math.a_star.AStar2D.remove_point)  math/a_star.cpp
- has_point  (Users-ks_128-Documents-godot-src-core.math.a_star.AStar2D.has_point)  math/a_star.cpp
```


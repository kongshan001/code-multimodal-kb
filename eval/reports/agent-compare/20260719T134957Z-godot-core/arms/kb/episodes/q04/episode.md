# q04 · code_retrieval · arm: `kb`

- **题**：A* 寻路算法用哪个类？
- **gold**：AStar
- **答对**：✓
- **答案**：`AStar2D`、`AStar3D`
- **指标**：tokens=3368 · llm_calls=3 · tool_steps=2 · 耗时=8.25s · 截断=否

---

**👤 用户**：A* 寻路算法用哪个类？

> 💭 **思考**：用户问A*寻路算法用哪个类。这是在问Godot引擎中A*寻路算法的实现类。

我需要在Godot core/代码库中搜索相关的类。A*寻路算法通常是在导航或路径查找相关的模块中。

让我搜索一下A*相关的类。

**🔧 `cmm_search`**({"query": "A* pathfinding astar navigation"})

> 💭 **思考**：搜索结果显示了AStar2D和AStar3D类，这些就是Godot中A*寻路算法的实现类。让我再搜索一下确认这些类的详细信息。

**🔧 `cmm_search`**({"query": "AStar2D AStar3D class pathfinding"})

> 💭 **思考**：好的，我找到了Godot中A*寻路算法的实现类。从搜索结果可以看出：

1. `AStar2D` - 用于2D空间的A*寻路
2. `AStar3D` - 用于3D空间的A*寻路

这些类提供了标准的A*算法功能，包括添加点、移除点、解决路径等方法。

根据用户的指令，我需要用简短的符号名直接作答，不要长解释。

**🤖 Agent**：`AStar2D`、`AStar3D`

**📋 工具结果**：
```
- astar  (Users-ks_128-Documents-godot-src-core.math.a_star.AStar2D.astar)  math/a_star.h
- ~AStar3D  (Users-ks_128-Documents-godot-src-core.math.a_star.AStar3D.~AStar3D)  math/a_star.cpp
- AHashMap  (Users-ks_128-Documents-godot-src-core.templates.a_hash_map.AHashMap.AHashMap)  templates/a_hash_map.h
- ~AHashMap  (Users-ks_128-Documents-godot-src-core.templates.a_hash_map.AHashMap.~AHashMap)  templates/a_hash_map.h
- clear  (Users-ks_128-Documents-godot-src-core.math.a_star.AStar3D.clear)  math/a_star.cpp
```

**📋 工具结果**：
```
- ~AStar3D  (Users-ks_128-Documents-godot-src-core.math.a_star.AStar3D.~AStar3D)  math/a_star.cpp
- clear  (Users-ks_128-Documents-godot-src-core.math.a_star.AStar2D.clear)  math/a_star.cpp
- _solve  (Users-ks_128-Documents-godot-src-core.math.a_star.AStar2D._solve)  math/a_star.cpp
- add_point  (Users-ks_128-Documents-godot-src-core.math.a_star.AStar2D.add_point)  math/a_star.cpp
- remove_point  (Users-ks_128-Documents-godot-src-core.math.a_star.AStar2D.remove_point)  math/a_star.cpp
```


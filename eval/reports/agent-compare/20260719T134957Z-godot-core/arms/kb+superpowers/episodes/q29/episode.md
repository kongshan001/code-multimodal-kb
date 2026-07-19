# q29 · bug_fix · arm: `kb+superpowers`

- **题**：A* 寻路在两点间返回了错误路径，忽略了一个障碍物。Godot 里负责计算寻路路径的是哪个类？
- **gold**：AStar, core/math/a_star.h
- **答对**：✓
- **答案**：`AStar2D` / `AStar3D`
- **指标**：tokens=2885 · llm_calls=3 · tool_steps=2 · 耗时=7.96s · 截断=否

---

**👤 用户**：A* 寻路在两点间返回了错误路径，忽略了一个障碍物。Godot 里负责计算寻路路径的是哪个类？

> 💭 **思考**：用户问的是 Godot 中负责计算 A* 寻路路径的类。我需要在 Godot core/ 代码库中查找与 A* 寻路相关的类。

让我先搜索 A* 寻路相关的代码。

**🔧 `cmm_search`**({"query": "A* pathfinding find path"})

**🔧 `cmm_search`**({"query": "astar pathfinding class"})

> 💭 **思考**：找到了！Godot 中负责 A* 寻路的是：
- `AStar2D` 类（2D 寻路）
- `AStar3D` 类（3D 寻路）

这些类在 `math/a_star.cpp` 和 `math/a_star.h` 中定义。

用户问的是"负责计算寻路路径的是哪个类"，应该直接给出这两个类的名称。

**🤖 Agent**：`AStar2D` / `AStar3D`

**📋 工具结果**：
```
- find  (Users-ks_128-Documents-godot-src-core.templates.a_hash_map.AHashMap.find)  templates/a_hash_map.h
- get_point_path  (Users-ks_128-Documents-godot-src-core.math.a_star.AStar3D.get_point_path)  math/a_star.cpp
- get_id_path  (Users-ks_128-Documents-godot-src-core.math.a_star.AStar3D.get_id_path)  math/a_star.cpp
- get_point_path  (Users-ks_128-Documents-godot-src-core.math.a_star.AStar2D.get_point_path)  math/a_star.cpp
- get_id_path  (Users-ks_128-Documents-godot-src-core.math.a_star.AStar2D.get_id_path)  math/a_star.cpp
```

**📋 工具结果**：
```
- astar  (Users-ks_128-Documents-godot-src-core.math.a_star.AStar2D.astar)  math/a_star.h
- class_exists  (Users-ks_128-Documents-godot-src-core.object.class_db.ClassDB.class_exists)  object/class_db.cpp
- _add_class  (Users-ks_128-Documents-godot-src-core.object.class_db.ClassDB._add_class)  object/class_db.cpp
- _is_parent_class  (Users-ks_128-Documents-godot-src-core.object.class_db.ClassDB._is_parent_class)  object/class_db.cpp
- is_parent_class  (Users-ks_128-Documents-godot-src-core.object.class_db.ClassDB.is_parent_class)  object/class_db.cpp
```


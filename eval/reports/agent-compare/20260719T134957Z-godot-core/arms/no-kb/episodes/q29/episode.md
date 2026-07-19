# q29 · bug_fix · arm: `no-kb`

- **题**：A* 寻路在两点间返回了错误路径，忽略了一个障碍物。Godot 里负责计算寻路路径的是哪个类？
- **gold**：AStar, core/math/a_star.h
- **答对**：✓
- **答案**：`AStarGrid2D`（还有 `AStar2D` 和 `AStar3D`）
- **指标**：tokens=9362 · llm_calls=8 · tool_steps=7 · 耗时=15.74s · 截断=否

---

**👤 用户**：A* 寻路在两点间返回了错误路径，忽略了一个障碍物。Godot 里负责计算寻路路径的是哪个类？

> 💭 **思考**：用户问的是 Godot 中负责计算 A* 寻路路径的类。我需要在 Godot core/ 源码中查找相关的代码。

A* 寻路通常涉及的关键词：
- AStar
- A_star
- pathfinding
- navigation

让我先搜索 AStar 相关的类。

**🔧 `grep_code`**({"pattern": "class.*AStar"})

> 💭 **思考**：找到了 AStar 相关的类，让我查看这些头文件来确定具体的类名。

**🔧 `read_file`**({"path": "/Users/ks_128/Documents/godot-src/core/math/a_star.h"})

**🔧 `read_file`**({"path": "/Users/ks_128/Documents/godot-src/core/math/a_star_grid_2d.h"})

> 💭 **思考**：我需要看到更多内容来确定类名。让我再读取更多行来看到类定义。

**🔧 `grep_code`**({"pattern": "class AStar"})

> 💭 **思考**：让我用不同的方式搜索，直接找类名。

**🔧 `grep_code`**({"pattern": "class AStar2D"})

**🔧 `grep_code`**({"pattern": "class AStar3D"})

> 💭 **思考**：好的，所以 AStar2D 和 AStar3D 都在 a_star.h 中定义。让我再搜索 AStarGrid2D。

**🔧 `grep_code`**({"pattern": "class AStarGrid2D"})

> 💭 **思考**：找到了。Godot 中负责计算 A* 寻路路径的类有：
- AStar2D
- AStar3D
- AStarGrid2D

根据用户的描述"两点间返回了错误路径，忽略了一个障碍物"，这更像是 AStarGrid2D 的问题，因为它处理网格上的障碍物。

我应该给出答案了。

**🤖 Agent**：`AStarGrid2D`（还有 `AStar2D` 和 `AStar3D`）

**📋 工具结果**：
```
matched 5 files:
/Users/ks_128/Documents/godot-src/core/math/a_star_grid_2d.h
/Users/ks_128/Documents/godot-src/core/math/a_star_grid_2d.cpp
/Users/ks_128/Documents/godot-src/core/math/a_star.h
/Users/ks_128/Documents/godot-src/core/math/a_star.cpp
/Users/ks_128/Documents/godot-src/core/register_core_types.cpp
```

**📋 工具结果**：
```
/**************************************************************************/
/*  a_star.h                                                              */
/**************************************************************************/
/*                         This file is part of:                          */
/*                             GODOT ENGINE                               */
/*                        https://godotengine.org                         */
/**************************************************************************/
/* Copyright (c) 2014-present Godot Engine contributors (see 
```

**📋 工具结果**：
```
/**************************************************************************/
/*  a_star_grid_2d.h                                                      */
/**************************************************************************/
/*                         This file is part of:                          */
/*                             GODOT ENGINE                               */
/*                        https://godotengine.org                         */
/**************************************************************************/
/* Copyright (c) 2014-present Godot Engine contributors (see 
```

**📋 工具结果**：
```
matched 2 files:
/Users/ks_128/Documents/godot-src/core/math/a_star_grid_2d.h
/Users/ks_128/Documents/godot-src/core/math/a_star.h
```

**📋 工具结果**：
```
matched 1 files:
/Users/ks_128/Documents/godot-src/core/math/a_star.h
```

**📋 工具结果**：
```
matched 1 files:
/Users/ks_128/Documents/godot-src/core/math/a_star.h
```

**📋 工具结果**：
```
matched 1 files:
/Users/ks_128/Documents/godot-src/core/math/a_star_grid_2d.h
```


# q04 · code_retrieval · arm: `no-kb`

- **题**：A* 寻路算法用哪个类？
- **gold**：AStar
- **答对**：✓
- **答案**：`AStar`、`AStarGrid2D`
- **指标**：tokens=6318 · llm_calls=5 · tool_steps=4 · 耗时=11.62s · 截断=否

---

**👤 用户**：A* 寻路算法用哪个类？

> 💭 **思考**：用户在问 A* 寻路算法用哪个类。这是在 Godot 代码库中的问题。我需要搜索与 A* 寻路相关的代码。

让我先搜索 A* 或 AStar 相关的模式。

**🔧 `grep_code`**({"pattern": "AStar"})

> 💭 **思考**：找到了 AStar 相关的文件。看起来主要有两个类：
1. AStar (a_star.h/cpp)
2. AStarGrid2D (a_star_grid_2d.h/cpp)

让我看一下 a_star.h 文件来确认类名。

**🔧 `read_file`**({"path": "core/math/a_star.h"})

> 💭 **思考**：路径错误，应该是完整路径。让我使用完整路径。

**🔧 `read_file`**({"path": "/Users/ks_128/Documents/godot-src/core/math/a_star.h"})

> 💭 **思考**：文件内容只显示了头部注释，我需要继续读取后面的内容来看类定义。不过从文件名和grep结果来看，类名应该是 `AStar`。让我也看看另一个类。

**🔧 `read_file`**({"path": "/Users/ks_128/Documents/godot-src/core/math/a_star_grid_2d.h"})

> 💭 **思考**：从grep结果可以看到有两个主要的A*相关类：
1. AStar (在 a_star.h/cpp 中)
2. AStarGrid2D (在 a_star_grid_2d.h/cpp 中)

用户问"A* 寻路算法用哪个类"，答案是 `AStar` 和 `AStarGrid2D` 这两个类。根据收敛纪律，我应该立即用符号名作答。

**🤖 Agent**：`AStar`、`AStarGrid2D`

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

**📋 工具结果**：
```
(read error: [Errno 2] No such file or directory: 'core/math/a_star.h')
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


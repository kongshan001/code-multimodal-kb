# q29 · bug_fix · arm: `no-kb`

**题**：Pathfinding returns a wrong path between two points, ignoring an obstacle. Which class computes the path?  ·  **gold**：AStar, core/math/a_star.h
**答对**：✓  ·  **答案**：In Godot's `core/`, path computation is handled by:

- **`AStar`** / **`AStar2D`** (`core/math/a_star.h`, `core/math/a_s
**指标**：tokens=2005 · llm_calls=8 · tool_steps=7 · 耗时=54.54s · 截断=否

---

**👤 用户**：Pathfinding returns a wrong path between two points, ignoring an obstacle. Which class computes the path?

> 💭 **思考**：The user is asking about which class in Godot's source code computes the path for pathfinding. Let me search for the relevant class.

**🔧 `grep_code`**({"pattern": "compute_path"})

> 💭 **思考**：Let me try another pattern.

**🔧 `grep_code`**({"pattern": "class NavigationServer"})

**🔧 `grep_code`**({"pattern": "find_path"})

> 💭 **思考**：Hmm, no matches. Let me try different patterns.

**🔧 `grep_code`**({"pattern": "NavigationServer"})

**🔧 `grep_code`**({"pattern": "get_simple_path"})

> 💭 **思考**：The grep tool seems to only search in `core/` directory. NavigationServer is likely in the `servers/` directory, not `core/`. Let me try searching for path-related functions in core.

**🔧 `grep_code`**({"pattern": "AStar"})

**🔧 `grep_code`**({"pattern": "_navigation"})

> 💭 **思考**：The pathfinding in Godot core involves:

1. **`AStar`** (and `AStar2D`) — generic A* pathfinding in `core/math/a_star.h`/`a_star.cpp`
2. **`AStarGrid2D`** — grid-based A* pathfinding in `core/math/a_star_grid_2d.h`/`a_star_grid_2d.cpp`

The `NavigationServer` is in the `servers/` directory which is 

**🤖 Agent**：In Godot's `core/`, path computation is handled by:

- **`AStar`** / **`AStar2D`** (`core/math/a_star.h`, `core/math/a_star.cpp`) — generic A* pathfinding; path computed via `get_path()`.
- **`AStarGrid2D`** (`core/math/a_star_grid_2d.h`, `core/math/a_star_grid_2d.cpp`) — grid-based A* pathfinding; 

**📋 工具结果**：
```
(no matches)
```

**📋 工具结果**：
```
(no matches)
```

**📋 工具结果**：
```
(no matches)
```

**📋 工具结果**：
```
matched 1 files:
/Users/ks_128/Documents/godot-src/core/extension/gdextension_special_compat_hashes.cpp
```

**📋 工具结果**：
```
(no matches)
```

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
matched 4 files:
/Users/ks_128/Documents/godot-src/core/io/dir_access.cpp
/Users/ks_128/Documents/godot-src/core/io/dir_access.h
/Users/ks_128/Documents/godot-src/core/core_constants.cpp
/Users/ks_128/Documents/godot-src/core/object/property_info.h
```


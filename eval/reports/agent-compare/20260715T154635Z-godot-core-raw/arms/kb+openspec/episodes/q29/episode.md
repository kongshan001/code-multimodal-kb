# q29 · bug_fix · arm: `kb+openspec`

**题**：A* 寻路在两点间返回了错误路径，忽略了一个障碍物。Godot 里负责计算寻路路径的是哪个类？  ·  **gold**：AStar, core/math/a_star.h
**答对**：✓  ·  **答案**：Godot 中负责 A* 寻路路径计算的类主要有以下几个：

1. **`AStar3D`** — 3D 空间的通用 A* 寻路（`core/math/a_star.cpp`）
2. **`AStar2D`** — 2D 空间的通用 A* 
**指标**：tokens=2793 · llm_calls=4 · tool_steps=3 · 耗时=20.58s · 截断=否

---

**👤 用户**：A* 寻路在两点间返回了错误路径，忽略了一个障碍物。Godot 里负责计算寻路路径的是哪个类？

**🔧 `cmm_search`**({"query": "A* pathfinding navigation compute path"})

**📋 工具结果**：
```
- _compute_cost  (Users-ks_128-Documents-godot-src-core.math.a_star.AStar3D._compute_cost)  math/a_star.cpp
- _compute_cost  (Users-ks_128-Documents-godot-src-core.math.a_star.AStar2D._compute_cost)  math/a_star.cpp
- _compute_cost  (Users-ks_128-Documents-godot-src-core.math.a_star_grid_2d.AStarGrid2D._compute_cost)  math/a_star_grid_2d.cpp
- set_default_compute_heuristic  (Users-ks_128-Documents-godot-src-core.math.a_star_grid_2d.AStarGrid2D.set_default_compute_heuristic)  math/a_star_grid_2d.cpp
- get_default_compute_heuristic  (Users-ks_128-Documents-godot-src-core.math.a_star_grid_2d.ASta
```

**🔧 `cmm_search`**({"query": "NavigationServer get path navigation path query"})

**📋 工具结果**：
```
- get_as_property_path  (Users-ks_128-Documents-godot-src-core.string.node_path.NodePath.get_as_property_path)  string/node_path.cpp
- get_path  (Users-ks_128-Documents-godot-src-core.io.resource.Resource.get_path)  io/resource.cpp
- get_path  (Users-ks_128-Documents-godot-src-core.io.file_access.FileAccess.get_path)  io/file_access.h
- get_executable_path  (Users-ks_128-Documents-godot-src-core.core_bind.OS.get_executable_path)  core_bind.cpp
- _get_library_path  (Users-ks_128-Documents-godot-src-core.extension.gdextension.GDExtension._get_library_path)  extension/gdextension.cpp
```

**🔧 `cmm_search`**({"query": "NavigationServer3D map_get_path server pathfinding"})

**📋 工具结果**：
```
- server  (Users-ks_128-Documents-godot-src-core.crypto.crypto.TLSOptions.server)  crypto/crypto.cpp
- is_server  (Users-ks_128-Documents-godot-src-core.crypto.crypto.TLSOptions.is_server)  crypto/crypto.h
- SocketServer  (Users-ks_128-Documents-godot-src-core.io.socket_server.SocketServer.SocketServer)  io/socket_server.cpp
- ~SocketServer  (Users-ks_128-Documents-godot-src-core.io.socket_server.SocketServer.~SocketServer)  io/socket_server.cpp
- UDPServer  (Users-ks_128-Documents-godot-src-core.io.udp_server.UDPServer.UDPServer)  io/udp_server.cpp
```

**🤖 Agent**：Godot 中负责 A* 寻路路径计算的类主要有以下几个：

1. **`AStar3D`** — 3D 空间的通用 A* 寻路（`core/math/a_star.cpp`）
2. **`AStar2D`** — 2D 空间的通用 A* 寻路（`core/math/a_star.cpp`）
3. **`AStarGrid2D`** — 2D 网格专用 A* 寻路（`core/math/a_star_grid_2d.cpp`）

核心路径计算方法都是 **`get_id_path()`**，代价估算走 **`_compute_cost()`**。

---

**如果你用的是导航系统（Navi


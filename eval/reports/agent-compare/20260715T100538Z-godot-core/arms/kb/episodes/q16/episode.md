# q16 · code_retrieval · arm: `kb`

**题**：目录操作用哪个类？  ·  **gold**：DirAccess
**答对**：✓  ·  **答案**：`DirAccess`（定义于 `io/dir_access.cpp` / `io/dir_access.h`）。

主要用法：
- `DirAccess::create()` — 创建实例
- `DirAccess::create_for
**指标**：tokens=1378 · llm_calls=3 · tool_steps=2 · 耗时=23.33s · 截断=否

---

**👤 用户**：目录操作用哪个类？

> 💭 **思考**：用户问的是目录操作用哪个类。让我搜索一下。

**🔧 `cmm_search`**({"query": "directory operations filesystem"})

> 💭 **思考**：Let me search more specifically for the DirAccess class which is the main directory access class in Godot.

**🔧 `cmm_search`**({"query": "DirAccess create directory remove"})

**🤖 Agent**：`DirAccess`（定义于 `io/dir_access.cpp` / `io/dir_access.h`）。

主要用法：
- `DirAccess::create()` — 创建实例
- `DirAccess::create_for_path()` — 针对特定路径创建
- `DirAccess::create_temp()` — 创建临时目录
- `DirAccess::remove_absolute()` — 删除目录

创建实例后通过 `make_dir()`、`list_dir_begin()` / `list_dir_end()`、`get_next()`、`copy()`、

**📋 工具结果**：
```
- list_directory  (Users-ks_128-Documents-godot-src-core.core_bind.ResourceLoader.list_directory)  core_bind.cpp
- list_directory  (Users-ks_128-Documents-godot-src-core.io.resource_loader.ResourceLoader.list_directory)  io/resource_loader.cpp
- add_directory  (Users-ks_128-Documents-godot-src-core.io.file_access_pack.PackedSourceDirectory.add_directory)  io/file_access_pack.cpp
- has_directory  (Users-ks_128-Documents-godot-src-core.io.file_access_pack.PackedData.has_directory)  io/file_access_pack.h
- try_open_directory  (Users-ks_128-Documents-godot-src-core.io.file_access_pack.PackedData.t
```

**📋 工具结果**：
```
- create  (Users-ks_128-Documents-godot-src-core.io.dir_access.DirAccess.create)  io/dir_access.cpp
- remove_absolute  (Users-ks_128-Documents-godot-src-core.io.dir_access.DirAccess.remove_absolute)  io/dir_access.cpp
- create_temp  (Users-ks_128-Documents-godot-src-core.io.dir_access.DirAccess.create_temp)  io/dir_access.cpp
- _create_temp  (Users-ks_128-Documents-godot-src-core.io.dir_access.DirAccess._create_temp)  io/dir_access.cpp
- create_for_path  (Users-ks_128-Documents-godot-src-core.io.dir_access.DirAccess.create_for_path)  io/dir_access.cpp
```


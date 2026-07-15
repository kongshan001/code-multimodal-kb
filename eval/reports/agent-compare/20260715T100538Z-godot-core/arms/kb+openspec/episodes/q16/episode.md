# q16 · code_retrieval · arm: `kb+openspec`

**题**：目录操作用哪个类？  ·  **gold**：DirAccess
**答对**：✓  ·  **答案**：`DirAccess`（`core/io/dir_access.h`），提供 `make_dir`、`copy`、`remove`、`list_dir_begin`、`dir_exists`、`file_exists` 等方法。
**指标**：tokens=1600 · llm_calls=3 · tool_steps=2 · 耗时=17.91s · 截断=否

---

**👤 用户**：目录操作用哪个类？

> 💭 **思考**：用户问目录操作用哪个类。在 Godot 中，目录操作通常用 `DirAccess` 类。让我搜索确认一下。

**🔧 `cmm_search`**({"query": "directory operations DirAccess"})

> 💭 **思考**：Let me search more specifically for DirAccess class.

**🔧 `cmm_search`**({"query": "DirAccess class make_dir copy remove file"})

**🤖 Agent**：`DirAccess`（`core/io/dir_access.h`），提供 `make_dir`、`copy`、`remove`、`list_dir_begin`、`dir_exists`、`file_exists` 等方法。

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
- make_dir_recursive  (Users-ks_128-Documents-godot-src-core.io.dir_access.DirAccess.make_dir_recursive)  io/dir_access.cpp
- make_dir_absolute  (Users-ks_128-Documents-godot-src-core.io.dir_access.DirAccess.make_dir_absolute)  io/dir_access.cpp
- make_dir_recursive_absolute  (Users-ks_128-Documents-godot-src-core.io.dir_access.DirAccess.make_dir_recursive_absolute)  io/dir_access.cpp
- remove_file_or_error  (Users-ks_128-Documents-godot-src-core.io.dir_access.DirAccess.remove_file_or_error)  io/dir_access.h
- copy  (Users-ks_128-Documents-godot-src-core.io.dir_access.DirAccess.copy)  io/dir_a
```


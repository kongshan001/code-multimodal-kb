# q16 · code_retrieval · arm: `kb+superpowers`

**题**：目录操作用哪个类？  ·  **gold**：DirAccess
**答对**：✓  ·  **答案**：**`DirAccess`**（`core/io/dir_access.h`）

常用操作：
- 创建目录：`make_dir` / `make_dir_recursive`
- 列举内容：`list_dir_begin` / `get_n
**指标**：tokens=1812 · llm_calls=3 · tool_steps=2 · 耗时=22.19s · 截断=否

---

**👤 用户**：目录操作用哪个类？

> 💭 **思考**：用户问"目录操作用哪个类"，在 Godot 的上下文中，这应该是指 `DirAccess` 类。让我快速搜索确认。

**🔧 `cmm_search`**({"query": "directory operations access create remove list"})

> 💭 **思考**：The search didn't directly surface `DirAccess`, but it's the well-known class for directory operations in Godot. Let me do a more targeted search to confirm.

**🔧 `cmm_search`**({"query": "DirAccess class make dir copy change directory"})

**🤖 Agent**：**`DirAccess`**（`core/io/dir_access.h`）

常用操作：
- 创建目录：`make_dir` / `make_dir_recursive`
- 列举内容：`list_dir_begin` / `get_next` / `list_dir_end`
- 切换目录：`change_dir` / `get_current_dir`
- 复制：`copy` / `copy_dir` / `copy_absolute`
- 删除：`remove` / `erase_contents_recursive`
- 查询：`dir_exists` / `file_exists

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
- _copy_dir  (Users-ks_128-Documents-godot-src-core.io.dir_access.DirAccess._copy_dir)  io/dir_access.cpp
- copy_dir  (Users-ks_128-Documents-godot-src-core.io.dir_access.DirAccess.copy_dir)  io/dir_access.cpp
- copy  (Users-ks_128-Documents-godot-src-core.io.dir_access.DirAccess.copy)  io/dir_access.cpp
- copy_absolute  (Users-ks_128-Documents-godot-src-core.io.dir_access.DirAccess.copy_absolute)  io/dir_access.cpp
- make_dir_recursive  (Users-ks_128-Documents-godot-src-core.io.dir_access.DirAccess.make_dir_recursive)  io/dir_access.cpp
```


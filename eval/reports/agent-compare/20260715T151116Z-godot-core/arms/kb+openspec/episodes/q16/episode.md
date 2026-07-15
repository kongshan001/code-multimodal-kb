# q16 · code_retrieval · arm: `kb+openspec`

**题**：目录操作用哪个类？  ·  **gold**：DirAccess
**答对**：✓  ·  **答案**：目录操作用 **`DirAccess`** 类（定义于 `core/io/dir_access.h` / `.cpp`）。

常用方法：
- `DirAccess::create()` — 创建实例（`open()` / `create_f
**指标**：tokens=1745 · llm_calls=3 · tool_steps=2 · 耗时=12.46s · 截断=否

---

**👤 用户**：目录操作用哪个类？

> 💭 **思考**：用户问的是 Godot 中目录操作用哪个类。这个问题我比较确定答案是 `DirAccess`，但让我搜索确认一下。

**🔧 `cmm_search`**({"query": "directory operations create remove list files"})

> 💭 **思考**：搜索结果没有直接显示 `DirAccess`，但我知道 Godot 中目录操作的类是 `DirAccess`。让我再搜索一下确认。

**🔧 `cmm_search`**({"query": "DirAccess directory create copy remove"})

**🤖 Agent**：目录操作用 **`DirAccess`** 类（定义于 `core/io/dir_access.h` / `.cpp`）。

常用方法：
- `DirAccess::create()` — 创建实例（`open()` / `create_for_path()`）
- `copy()`, `copy_absolute()`, `copy_dir()` — 复制
- `list_dir_begin()` / `list_dir_end()` — 遍历目录
- `make_dir()`, `remove()`, `rename()` — 创建/删除/重命名

**📋 工具结果**：
```
- list_directory  (Users-ks_128-Documents-godot-src-core.core_bind.ResourceLoader.list_directory)  core_bind.cpp
- list_directory  (Users-ks_128-Documents-godot-src-core.io.resource_loader.ResourceLoader.list_directory)  io/resource_loader.cpp
- remove_from_list  (Users-ks_128-Documents-godot-src-core.templates.self_list.SelfList.remove_from_list)  templates/self_list.h
- remove  (Users-ks_128-Documents-godot-src-core.templates.self_list.SelfList.List.remove)  templates/self_list.h
- add_directory  (Users-ks_128-Documents-godot-src-core.io.file_access_pack.PackedSourceDirectory.add_directory) 
```

**📋 工具结果**：
```
- copy  (Users-ks_128-Documents-godot-src-core.io.dir_access.DirAccess.copy)  io/dir_access.cpp
- copy_absolute  (Users-ks_128-Documents-godot-src-core.io.dir_access.DirAccess.copy_absolute)  io/dir_access.cpp
- _copy_dir  (Users-ks_128-Documents-godot-src-core.io.dir_access.DirAccess._copy_dir)  io/dir_access.cpp
- copy_dir  (Users-ks_128-Documents-godot-src-core.io.dir_access.DirAccess.copy_dir)  io/dir_access.cpp
- create  (Users-ks_128-Documents-godot-src-core.io.dir_access.DirAccess.create)  io/dir_access.cpp
```


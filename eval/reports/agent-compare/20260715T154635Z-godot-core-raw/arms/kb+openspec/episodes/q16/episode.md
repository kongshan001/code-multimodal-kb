# q16 · code_retrieval · arm: `kb+openspec`

**题**：目录操作用哪个类？  ·  **gold**：DirAccess
**答对**：✓  ·  **答案**：目录操作用 **`DirAccess`** 类（`io/dir_access.h` / `io/dir_access.cpp`）。

主要用法：
- `DirAccess::create(DirAccess::AccessType)` — 
**指标**：tokens=1971 · llm_calls=3 · tool_steps=2 · 耗时=11.29s · 截断=否

---

**👤 用户**：目录操作用哪个类？

**🔧 `cmm_search`**({"query": "directory operations filesystem"})

**📋 工具结果**：
```
- list_directory  (Users-ks_128-Documents-godot-src-core.core_bind.ResourceLoader.list_directory)  core_bind.cpp
- list_directory  (Users-ks_128-Documents-godot-src-core.io.resource_loader.ResourceLoader.list_directory)  io/resource_loader.cpp
- add_directory  (Users-ks_128-Documents-godot-src-core.io.file_access_pack.PackedSourceDirectory.add_directory)  io/file_access_pack.cpp
- has_directory  (Users-ks_128-Documents-godot-src-core.io.file_access_pack.PackedData.has_directory)  io/file_access_pack.h
- try_open_directory  (Users-ks_128-Documents-godot-src-core.io.file_access_pack.PackedData.t
```

**🔧 `cmm_search`**({"query": "DirAccess directory create remove list"})

**📋 工具结果**：
```
- list_directory  (Users-ks_128-Documents-godot-src-core.core_bind.ResourceLoader.list_directory)  core_bind.cpp
- list_directory  (Users-ks_128-Documents-godot-src-core.io.resource_loader.ResourceLoader.list_directory)  io/resource_loader.cpp
- remove_from_list  (Users-ks_128-Documents-godot-src-core.templates.self_list.SelfList.remove_from_list)  templates/self_list.h
- remove  (Users-ks_128-Documents-godot-src-core.templates.self_list.SelfList.List.remove)  templates/self_list.h
- create  (Users-ks_128-Documents-godot-src-core.io.dir_access.DirAccess.create)  io/dir_access.cpp
```

**🤖 Agent**：目录操作用 **`DirAccess`** 类（`io/dir_access.h` / `io/dir_access.cpp`）。

主要用法：
- `DirAccess::create(DirAccess::AccessType)` — 创建实例
- `list_dir_begin()` / `get_next()` / `list_dir_end()` — 遍历目录
- `make_dir()` / `make_dir_recursive()` — 创建目录
- `remove()` / `remove_dir()` / `remove_dir_recursive()` — 删除
- `c


# q16 · code_retrieval · arm: `kb+superpowers`

**题**：目录操作用哪个类？  ·  **gold**：DirAccess
**答对**：✓  ·  **答案**：`DirAccess`（定义在 `io/dir_access.h` / `io/dir_access.cpp`）。

通过静态方法 `DirAccess::create()` 获取实例，提供目录的创建、删除、列举、拷贝等操作。
**指标**：tokens=624 · llm_calls=3 · tool_steps=2 · 耗时=12.67s · 截断=否

---

**👤 用户**：目录操作用哪个类？

> 💭 **思考**：用户问目录操作用哪个类。让我搜索一下。

**🔧 `cmm_search`**({"query": "directory operations"})

> 💭 **思考**：让我搜索更明确的目录操作类，比如 DirAccess。

**🔧 `cmm_search`**({"query": "DirAccess directory create remove list"})

> 💭 **思考**：找到了。`DirAccess` 类是目录操作的核心类。让我确认一下它的位置。

**🤖 Agent**：`DirAccess`（定义在 `io/dir_access.h` / `io/dir_access.cpp`）。

通过静态方法 `DirAccess::create()` 获取实例，提供目录的创建、删除、列举、拷贝等操作。

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
- list_directory  (Users-ks_128-Documents-godot-src-core.core_bind.ResourceLoader.list_directory)  core_bind.cpp
- list_directory  (Users-ks_128-Documents-godot-src-core.io.resource_loader.ResourceLoader.list_directory)  io/resource_loader.cpp
- remove_from_list  (Users-ks_128-Documents-godot-src-core.templates.self_list.SelfList.remove_from_list)  templates/self_list.h
- remove  (Users-ks_128-Documents-godot-src-core.templates.self_list.SelfList.List.remove)  templates/self_list.h
- create  (Users-ks_128-Documents-godot-src-core.io.dir_access.DirAccess.create)  io/dir_access.cpp
```


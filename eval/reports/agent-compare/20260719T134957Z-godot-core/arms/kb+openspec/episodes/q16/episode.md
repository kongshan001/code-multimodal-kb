# q16 · code_retrieval · arm: `kb+openspec`

- **题**：目录操作用哪个类？
- **gold**：DirAccess
- **答对**：✓
- **答案**：`DirAccess`
- **指标**：tokens=4014 · llm_calls=3 · tool_steps=2 · 耗时=9.26s · 截断=否

---

**👤 用户**：目录操作用哪个类？

> 💭 **思考**：用户问"目录操作用哪个类？"，这是在问 Godot 代码库中用于目录操作的类。

我需要使用语义检索工具来查找 Godot core/ 中与目录操作相关的类。

让我搜索相关的符号。

**🔧 `cmm_search`**({"query": "目录操作 DirAccess Directory"})

> 💭 **思考**：搜索结果没有直接显示 DirAccess 类。让我再搜一下 DirAccess：

**🔧 `cmm_search`**({"query": "DirAccess"})

> 💭 **思考**：好的，找到了 `DirAccess` 类。在 Godot 中，目录操作使用的类是 `DirAccess`。

根据检索结果，这个类位于 `io/dir_access.cpp` 文件中，提供了如 `open`, `create`, `copy` 等目录操作方法。

我直接用符号名回答。

**🤖 Agent**：`DirAccess`

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
- ~DirAccess  (Users-ks_128-Documents-godot-src-core.io.dir_access.DirAccess.~DirAccess)  io/dir_access.cpp
- open  (Users-ks_128-Documents-godot-src-core.io.dir_access.DirAccess.open)  io/dir_access.cpp
- _open  (Users-ks_128-Documents-godot-src-core.io.dir_access.DirAccess._open)  io/dir_access.cpp
- create  (Users-ks_128-Documents-godot-src-core.io.dir_access.DirAccess.create)  io/dir_access.cpp
- copy  (Users-ks_128-Documents-godot-src-core.io.dir_access.DirAccess.copy)  io/dir_access.cpp
```


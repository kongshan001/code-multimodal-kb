# q16 · code_retrieval · arm: `kb`

- **题**：目录操作用哪个类？
- **gold**：DirAccess
- **答对**：✓
- **答案**：DirAccess
- **指标**：tokens=3215 · llm_calls=3 · tool_steps=2 · 耗时=8.42s · 截断=否

---

**👤 用户**：目录操作用哪个类？

> 💭 **思考**：用户问"目录操作用哪个类"，这是在问 Godot 代码库中用于目录操作的类。

我需要在 Godot core/ 中搜索相关的类。常见的目录操作类可能叫 `DirAccess`、`Directory`、`Folder` 之类的。

让我搜索一下。

**🔧 `cmm_search`**({"query": "目录操作 directory"})

> 💭 **思考**：搜索结果显示了一些 list_directory 方法，但还没有找到专门的目录操作类。让我再搜索一下 DirAccess 或 Directory 相关的类。

**🔧 `cmm_search`**({"query": "DirAccess"})

> 💭 **思考**：找到了！DirAccess 类就是用于目录操作的类。搜索结果显示了它的构造函数、open、create、copy 等方法，这些都是典型的目录操作功能。

根据收敛纪律，工具返回了相关符号就应该立刻用符号名作答。答案是 `DirAccess`。

**🤖 Agent**：DirAccess

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


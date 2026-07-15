# q15 · code_retrieval · arm: `kb+openspec`

**题**：文件读写操作用哪个类？  ·  **gold**：FileAccess
**答对**：✓  ·  **答案**：文件读写操作用 **`FileAccess`** 类（位于 `core/io/file_access.cpp`）。

主要操作如：`file_store_buffer`、`file_get_buffer`、`set_read_only_at
**指标**：tokens=1392 · llm_calls=2 · tool_steps=1 · 耗时=12.69s · 截断=否

---

**👤 用户**：文件读写操作用哪个类？

> 💭 **思考**：用户问的是文件读写操作用哪个类。让我搜索一下。

**🔧 `cmm_search`**({"query": "file read write operations"})

> 💭 **思考**：结果指向 `FileAccess` 类，这是 Godot 中文件读写操作的核心类。

**🤖 Agent**：文件读写操作用 **`FileAccess`** 类（位于 `core/io/file_access.cpp`）。

主要操作如：`file_store_buffer`、`file_get_buffer`、`set_read_only_attribute` / `get_read_only_attribute` 等都定义在此类中。

> 补充：目录操作（创建/遍历/删除目录）则用 **`DirAccess`** 类。

**📋 工具结果**：
```
- godot_write  (Users-ks_128-Documents-godot-src-core.io.file_access_zip.godot_write)  io/file_access_zip.cpp
- godot_read  (Users-ks_128-Documents-godot-src-core.io.file_access_zip.godot_read)  io/file_access_zip.cpp
- read_link  (Users-ks_128-Documents-godot-src-core.io.file_access_pack.DirAccessPack.read_link)  io/file_access_pack.h
- get_read_only_attribute  (Users-ks_128-Documents-godot-src-core.io.file_access.FileAccess.get_read_only_attribute)  io/file_access.cpp
- set_read_only_attribute  (Users-ks_128-Documents-godot-src-core.io.file_access.FileAccess.set_read_only_attribute)  io/file
```


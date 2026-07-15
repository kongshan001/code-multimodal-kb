# q15 · code_retrieval · arm: `kb+openspec`

**题**：文件读写操作用哪个类？  ·  **gold**：FileAccess
**答对**：✓  ·  **答案**：`FileAccess`

定义在 `core/io/file_access.h`，是 Godot 中文件读写操作的核心类。提供 `open`、`get_buffer`、`store_buffer`、`get_line`、`store_st
**指标**：tokens=1397 · llm_calls=2 · tool_steps=1 · 耗时=11.02s · 截断=否

---

**👤 用户**：文件读写操作用哪个类？

> 💭 **思考**：The user is asking which class is used for file read/write operations in Godot.

**🔧 `cmm_search`**({"query": "file read write operations"})

> 💭 **思考**：The results point to `FileAccess` class in `io/file_access.h`. That's the main class for file read/write operations in Godot.

**🤖 Agent**：`FileAccess`

定义在 `core/io/file_access.h`，是 Godot 中文件读写操作的核心类。提供 `open`、`get_buffer`、`store_buffer`、`get_line`、`store_string` 等方法。

> 补充：目录操作（创建/遍历目录）用 `DirAccess`。

**📋 工具结果**：
```
- godot_write  (Users-ks_128-Documents-godot-src-core.io.file_access_zip.godot_write)  io/file_access_zip.cpp
- godot_read  (Users-ks_128-Documents-godot-src-core.io.file_access_zip.godot_read)  io/file_access_zip.cpp
- read_link  (Users-ks_128-Documents-godot-src-core.io.file_access_pack.DirAccessPack.read_link)  io/file_access_pack.h
- get_read_only_attribute  (Users-ks_128-Documents-godot-src-core.io.file_access.FileAccess.get_read_only_attribute)  io/file_access.cpp
- set_read_only_attribute  (Users-ks_128-Documents-godot-src-core.io.file_access.FileAccess.set_read_only_attribute)  io/file
```


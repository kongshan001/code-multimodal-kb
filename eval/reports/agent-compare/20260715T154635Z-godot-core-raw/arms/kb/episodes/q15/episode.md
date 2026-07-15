# q15 · code_retrieval · arm: `kb`

**题**：文件读写操作用哪个类？  ·  **gold**：FileAccess
**答对**：✓  ·  **答案**：文件读写操作使用 **`FileAccess`** 类（位于 `core/io/file_access.h` / `.cpp`）。

常用方法包括：
- `FileAccess::open()` — 打开文件
- `file->get_bu
**指标**：tokens=702 · llm_calls=2 · tool_steps=1 · 耗时=12.57s · 截断=否

---

**👤 用户**：文件读写操作用哪个类？

**🔧 `cmm_search`**({"query": "file read write operations"})

**📋 工具结果**：
```
- godot_write  (Users-ks_128-Documents-godot-src-core.io.file_access_zip.godot_write)  io/file_access_zip.cpp
- godot_read  (Users-ks_128-Documents-godot-src-core.io.file_access_zip.godot_read)  io/file_access_zip.cpp
- read_link  (Users-ks_128-Documents-godot-src-core.io.file_access_pack.DirAccessPack.read_link)  io/file_access_pack.h
- get_read_only_attribute  (Users-ks_128-Documents-godot-src-core.io.file_access.FileAccess.get_read_only_attribute)  io/file_access.cpp
- set_read_only_attribute  (Users-ks_128-Documents-godot-src-core.io.file_access.FileAccess.set_read_only_attribute)  io/file
```

**🤖 Agent**：文件读写操作使用 **`FileAccess`** 类（位于 `core/io/file_access.h` / `.cpp`）。

常用方法包括：
- `FileAccess::open()` — 打开文件
- `file->get_buffer()` / `file->get_8()` / `file->get_line()` 等 — 读取
- `file->store_buffer()` / `file->store_8()` / `file->store_string()` 等 — 写入
- `file->close()` — 关闭

此外，目录/路径操作可使用 **`DirAcces


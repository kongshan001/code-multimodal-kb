# q15 · code_retrieval · arm: `kb+openspec`

**题**：文件读写操作用哪个类？  ·  **gold**：FileAccess
**答对**：✓  ·  **答案**：文件读写操作使用 **`FileAccess`** 类（`core/io/file_access.h`）。

常用方法：
- **打开/读取**：`FileAccess::open()`、`get_buffer()`、`get_line()
**指标**：tokens=1574 · llm_calls=2 · tool_steps=1 · 耗时=10.64s · 截断=否

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

**🤖 Agent**：文件读写操作使用 **`FileAccess`** 类（`core/io/file_access.h`）。

常用方法：
- **打开/读取**：`FileAccess::open()`、`get_buffer()`、`get_line()`、`get_string()` 等
- **写入**：`store_buffer()`、`store_string()`、`store_line()` 等
- **静态便捷方法**：`FileAccess::get_file_as_string()`、`FileAccess::write_file()` 等

如果涉及目录操作，则用 **`DirAcces


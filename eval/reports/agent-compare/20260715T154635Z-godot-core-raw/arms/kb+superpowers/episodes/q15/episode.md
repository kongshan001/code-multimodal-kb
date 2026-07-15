# q15 · code_retrieval · arm: `kb+superpowers`

**题**：文件读写操作用哪个类？  ·  **gold**：FileAccess
**答对**：✓  ·  **答案**：文件读写操作使用 **`FileAccess`** 类（`core/io/file_access.h`）。

常用方法：
- **打开/关闭**：`FileAccess::open()`、`close()`
- **读取**：`get_8(
**指标**：tokens=1684 · llm_calls=2 · tool_steps=1 · 耗时=15.76s · 截断=否

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
- **打开/关闭**：`FileAccess::open()`、`close()`
- **读取**：`get_8()`、`get_16()`、`get_32()`、`get_buffer()`、`get_line()`、`get_string()` 等
- **写入**：`store_8()`、`store_32()`、`store_buffer()`、`store_string()` 等

此外，目录操作用 **`DirAccess`** 类。


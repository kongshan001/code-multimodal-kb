# q15 · code_retrieval · arm: `kb+superpowers`

**题**：文件读写操作用哪个类？  ·  **gold**：FileAccess
**答对**：✓  ·  **答案**：文件读写操作用 **`FileAccess`** 类，位于 `core/io/file_access.cpp`。

常用方法：
- `FileAccess::open(path, flags)` — 打开文件
- `FileAccess::
**指标**：tokens=1392 · llm_calls=2 · tool_steps=1 · 耗时=33.67s · 截断=否

---

**👤 用户**：文件读写操作用哪个类？

> 💭 **思考**：The user is asking about which class is used for file read/write operations in Godot.

**🔧 `cmm_search`**({"query": "file read write open"})

**🤖 Agent**：文件读写操作用 **`FileAccess`** 类，位于 `core/io/file_access.cpp`。

常用方法：
- `FileAccess::open(path, flags)` — 打开文件
- `FileAccess::open_encrypted()` — 打开加密文件
- `FileAccess::open_compressed()` — 打开压缩文件

**📋 工具结果**：
```
- open  (Users-ks_128-Documents-godot-src-core.io.file_access.FileAccess.open)  io/file_access.cpp
- _open  (Users-ks_128-Documents-godot-src-core.io.file_access.FileAccess._open)  io/file_access.cpp
- godot_write  (Users-ks_128-Documents-godot-src-core.io.file_access_zip.godot_write)  io/file_access_zip.cpp
- open_encrypted  (Users-ks_128-Documents-godot-src-core.io.file_access.FileAccess.open_encrypted)  io/file_access.cpp
- open_compressed  (Users-ks_128-Documents-godot-src-core.io.file_access.FileAccess.open_compressed)  io/file_access.cpp
```


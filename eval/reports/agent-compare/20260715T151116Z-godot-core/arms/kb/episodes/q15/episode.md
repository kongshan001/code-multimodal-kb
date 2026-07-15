# q15 · code_retrieval · arm: `kb`

**题**：文件读写操作用哪个类？  ·  **gold**：FileAccess
**答对**：✓  ·  **答案**：**`FileAccess`**

Godot 核心的文件读写操作统一通过 `FileAccess` 类（`io/file_access.cpp`）完成。主要方法：

- `FileAccess::open(path, flags)` — 
**指标**：tokens=1145 · llm_calls=2 · tool_steps=1 · 耗时=14.79s · 截断=否

---

**👤 用户**：文件读写操作用哪个类？

> 💭 **思考**：The user is asking about which class is used for file read/write operations in Godot. Let me search for this.

**🔧 `cmm_search`**({"query": "file read write open"})

> 💭 **思考**：The answer is clear: `FileAccess`.

**🤖 Agent**：**`FileAccess`**

Godot 核心的文件读写操作统一通过 `FileAccess` 类（`io/file_access.cpp`）完成。主要方法：

- `FileAccess::open(path, flags)` — 打开文件（静态方法，返回 `Ref<FileAccess>`）
- `FileAccess::open_compressed()` — 打开压缩文件
- `FileAccess::open_encrypted()` — 打开加密文件
- 内部虚函数 `_open()` — 子类实现具体打开逻辑

`FileAccess` 本身是抽象基类，不同平台/后端（如 

**📋 工具结果**：
```
- open  (Users-ks_128-Documents-godot-src-core.io.file_access.FileAccess.open)  io/file_access.cpp
- _open  (Users-ks_128-Documents-godot-src-core.io.file_access.FileAccess._open)  io/file_access.cpp
- godot_write  (Users-ks_128-Documents-godot-src-core.io.file_access_zip.godot_write)  io/file_access_zip.cpp
- open_encrypted  (Users-ks_128-Documents-godot-src-core.io.file_access.FileAccess.open_encrypted)  io/file_access.cpp
- open_compressed  (Users-ks_128-Documents-godot-src-core.io.file_access.FileAccess.open_compressed)  io/file_access.cpp
```


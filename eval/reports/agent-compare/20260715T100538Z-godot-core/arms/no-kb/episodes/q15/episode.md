# q15 · code_retrieval · arm: `no-kb`

**题**：文件读写操作用哪个类？  ·  **gold**：FileAccess
**答对**：✓  ·  **答案**：文件读写操作的核心类是 **`FileAccess`**（定义在 `core/io/file_access.h`）。

常用静态方法包括：
- `FileAccess::open(path, flags)` — 打开文件，返回 `Ref<F
**指标**：tokens=1117 · llm_calls=2 · tool_steps=1 · 耗时=16.14s · 截断=否

---

**👤 用户**：文件读写操作用哪个类？

> 💭 **思考**：用户问的是 Godot 中文件读写操作用哪个类。让我搜索一下。

**🔧 `grep_code`**({"pattern": "class FileAccess"})

> 💭 **思考**：文件读写操作的核心类是 `FileAccess`。

**🤖 Agent**：文件读写操作的核心类是 **`FileAccess`**（定义在 `core/io/file_access.h`）。

常用静态方法包括：
- `FileAccess::open(path, flags)` — 打开文件，返回 `Ref<FileAccess>`
- 配合 `ModeFlags`（`READ` / `WRITE` / `READ_WRITE` 等）指定读写模式

其下还有多个子类用于不同后端：`FileAccessCompressed`、`FileAccessMemory`、`FileAccessPack`、`FileAccessZip`、`FileAccessEncrypte

**📋 工具结果**：
```
matched 10 files:
/Users/ks_128/Documents/godot-src/core/io/file_access_compressed.h
/Users/ks_128/Documents/godot-src/core/io/file_access_patched.h
/Users/ks_128/Documents/godot-src/core/io/file_access_pack.h
/Users/ks_128/Documents/godot-src/core/io/file_access_zip.h
/Users/ks_128/Documents/godot-src/core/io/file_access_memory.h
/Users/ks_128/Documents/godot-src/core/io/file_access.h
/Users/ks_128/Documents/godot-src/core/io/resource_uid.h
/Users/ks_128/Documents/godot-src/core/io/pck_packer.h
/Users/ks_128/Documents/godot-src/core/io/logger.h
/Users/ks_128/Documents/godot-src/core/io/file_a
```


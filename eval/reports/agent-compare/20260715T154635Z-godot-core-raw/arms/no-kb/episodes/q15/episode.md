# q15 · code_retrieval · arm: `no-kb`

**题**：文件读写操作用哪个类？  ·  **gold**：FileAccess
**答对**：✓  ·  **答案**：文件读写操作使用 **`FileAccess`** 类（定义在 `core/io/file_access.h`）。

相关子类/变体：
- `FileAccessCompressed` — 压缩文件读写
- `FileAccessEncry
**指标**：tokens=975 · llm_calls=2 · tool_steps=1 · 耗时=10.21s · 截断=否

---

**👤 用户**：文件读写操作用哪个类？

**🔧 `grep_code`**({"pattern": "class FileAccess"})

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

**🤖 Agent**：文件读写操作使用 **`FileAccess`** 类（定义在 `core/io/file_access.h`）。

相关子类/变体：
- `FileAccessCompressed` — 压缩文件读写
- `FileAccessEncrypted` — 加密文件读写
- `FileAccessMemory` — 内存文件读写
- `FileAccessPack` / `FileAccessZip` — PCK 包 / ZIP 包内文件访问


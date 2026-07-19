# q15 · code_retrieval · arm: `kb`

- **题**：文件读写操作用哪个类？
- **gold**：FileAccess
- **答对**：✓
- **答案**：`FileAccess`
- **指标**：tokens=3263 · llm_calls=3 · tool_steps=2 · 耗时=10.9s · 截断=否

---

**👤 用户**：文件读写操作用哪个类？

> 💭 **思考**：用户问的是"文件读写操作用哪个类？"，这是在问 Godot 4.7 core/ 代码库中用于文件读写操作的类。

我需要用 cmm_search 来搜索相关的类。常见的文件读写类可能是 `FileAccess` 或类似的。

让我搜索一下。

**🔧 `cmm_search`**({"query": "file read write access file operations"})

> 💭 **思考**：搜索结果显示了一些相关的符号，其中 `FileAccess` 类出现了。这看起来是 Godot 中用于文件读写操作的主要类。让我再搜索一下更具体的信息。

**🔧 `cmm_search`**({"query": "FileAccess class file"})

> 💭 **思考**：很好，`FileAccess` 类确实是 Godot 中的文件访问类，有 `open`、`create`、`exists` 等方法。这应该是用户询问的答案。

根据指示，我应该直接用符号名作答，不要长解释。

**🤖 Agent**：`FileAccess`

**📋 工具结果**：
```
- godot_write  (Users-ks_128-Documents-godot-src-core.io.file_access_zip.godot_write)  io/file_access_zip.cpp
- godot_read  (Users-ks_128-Documents-godot-src-core.io.file_access_zip.godot_read)  io/file_access_zip.cpp
- read_link  (Users-ks_128-Documents-godot-src-core.io.file_access_pack.DirAccessPack.read_link)  io/file_access_pack.h
- get_read_only_attribute  (Users-ks_128-Documents-godot-src-core.io.file_access.FileAccess.get_read_only_attribute)  io/file_access.cpp
- set_read_only_attribute  (Users-ks_128-Documents-godot-src-core.io.file_access.FileAccess.set_read_only_attribute)  io/file
```

**📋 工具结果**：
```
- ~FileAccess  (Users-ks_128-Documents-godot-src-core.io.file_access.FileAccess.~FileAccess)  io/file_access.cpp
- create  (Users-ks_128-Documents-godot-src-core.io.file_access.FileAccess.create)  io/file_access.cpp
- exists  (Users-ks_128-Documents-godot-src-core.io.file_access.FileAccess.exists)  io/file_access.cpp
- reopen  (Users-ks_128-Documents-godot-src-core.io.file_access.FileAccess.reopen)  io/file_access.cpp
- open  (Users-ks_128-Documents-godot-src-core.io.file_access.FileAccess.open)  io/file_access.cpp
```


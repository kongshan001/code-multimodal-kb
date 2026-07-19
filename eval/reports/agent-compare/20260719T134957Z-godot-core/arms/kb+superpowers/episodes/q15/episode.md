# q15 · code_retrieval · arm: `kb+superpowers`

- **题**：文件读写操作用哪个类？
- **gold**：FileAccess
- **答对**：✓
- **答案**：`FileAccess`
- **指标**：tokens=6127 · llm_calls=4 · tool_steps=3 · 耗时=12.66s · 截断=否

---

**👤 用户**：文件读写操作用哪个类？

> 💭 **思考**：用户在问 Godot 代码库中文件读写操作使用哪个类。这是一个关于 Godot 核心代码库的问题，我需要用提供的工具来查找相关信息。

我应该使用 `mcp__bench__cmm_search` 来搜索与文件读写相关的类。

让我搜索一下文件读写相关的类。

**🔧 `cmm_search`**({"query": "file read write operations class"})

> 💭 **思考**：搜索结果返回了一些与文件读写相关的内容，但是看起来主要是 FileAccess 类。让我再搜索一下更具体的类名，比如 FileAccess、FileAccess 类本身。

**🔧 `cmm_search`**({"query": "FileAccess class"})

> 💭 **思考**：现在我看到了 FileAccess 类，这应该是 Godot 中用于文件读写操作的主要类。让我再搜索一下是否还有其他相关的类，比如 DirAccess 或者其他的文件操作类。

**🔧 `cmm_search`**({"query": "DirAccess class file operations"})

> 💭 **思考**：好的，现在我有了两个主要的类：
1. FileAccess - 用于文件的读写操作
2. DirAccess - 用于目录的操作

根据用户的问题"文件读写操作用哪个类？"，答案应该是 FileAccess 类。

根据指令，我需要直接给出符号名，不要长篇解释。

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

**📋 工具结果**：
```
- remove_file_or_error  (Users-ks_128-Documents-godot-src-core.io.dir_access.DirAccess.remove_file_or_error)  io/dir_access.h
- ~DirAccess  (Users-ks_128-Documents-godot-src-core.io.dir_access.DirAccess.~DirAccess)  io/dir_access.cpp
- open  (Users-ks_128-Documents-godot-src-core.io.dir_access.DirAccess.open)  io/dir_access.cpp
- _open  (Users-ks_128-Documents-godot-src-core.io.dir_access.DirAccess._open)  io/dir_access.cpp
- create  (Users-ks_128-Documents-godot-src-core.io.dir_access.DirAccess.create)  io/dir_access.cpp
```


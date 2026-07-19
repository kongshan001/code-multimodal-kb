# q15 · code_retrieval · arm: `kb+openspec`

- **题**：文件读写操作用哪个类？
- **gold**：FileAccess
- **答对**：✓
- **答案**：`FileAccess`
- **指标**：tokens=5806 · llm_calls=4 · tool_steps=3 · 耗时=11.89s · 截断=否

---

**👤 用户**：文件读写操作用哪个类？

> 💭 **思考**：用户问 Godot 代码库中文件读写操作用哪个类。这是一个简单的代码定位问题，我应该用语义检索工具搜索相关内容。

让我搜索"文件读写"或"file read write"相关的内容。

**🔧 `cmm_search`**({"query": "文件读写操作"})

> 💭 **思考**：搜索结果不相关，让我用英文搜索 "file read write" 或 " FileAccess"。

**🔧 `cmm_search`**({"query": "FileAccess file read write"})

> 💭 **思考**：好的，搜索到了 FileAccess 类。看起来 Godot 中文件读写操作是用 FileAccess 类。让我再搜索一下确认。

**🔧 `cmm_search`**({"query": "FileAccess class"})

> 💭 **思考**：确认了，FileAccess 类是 Godot 中用于文件读写操作的类。搜索结果中显示了 create、open、exists 等方法，这些都是典型的文件操作接口。

根据指示，一旦工具返回了相关符号就立刻用符号名作答，不要反复查。查到即答。

答案应该是：FileAccess

**🤖 Agent**：`FileAccess`

**📋 工具结果**：
```
- $id  (Users-ks_128-Documents-godot-src-core.extension.gdextension_interface.schema.$id)  extension/gdextension_interface.schema.json
- $schema  (Users-ks_128-Documents-godot-src-core.extension.gdextension_interface.$schema)  extension/gdextension_interface.json
- $schema  (Users-ks_128-Documents-godot-src-core.extension.gdextension_interface.schema.$schema)  extension/gdextension_interface.schema.json
- &_cowdata  (Users-ks_128-Documents-godot-src-core.string.ustring.CharProxy.&_cowdata)  string/ustring.h
- &func  (Users-ks_128-Documents-godot-src-core.variant.callable.CallableComparator.&fu
```

**📋 工具结果**：
```
- get_read_only_attribute  (Users-ks_128-Documents-godot-src-core.io.file_access.FileAccess.get_read_only_attribute)  io/file_access.cpp
- set_read_only_attribute  (Users-ks_128-Documents-godot-src-core.io.file_access.FileAccess.set_read_only_attribute)  io/file_access.cpp
- godot_write  (Users-ks_128-Documents-godot-src-core.io.file_access_zip.godot_write)  io/file_access_zip.cpp
- godot_read  (Users-ks_128-Documents-godot-src-core.io.file_access_zip.godot_read)  io/file_access_zip.cpp
- read_link  (Users-ks_128-Documents-godot-src-core.io.file_access_pack.DirAccessPack.read_link)  io/file_ac
```

**📋 工具结果**：
```
- ~FileAccess  (Users-ks_128-Documents-godot-src-core.io.file_access.FileAccess.~FileAccess)  io/file_access.cpp
- create  (Users-ks_128-Documents-godot-src-core.io.file_access.FileAccess.create)  io/file_access.cpp
- exists  (Users-ks_128-Documents-godot-src-core.io.file_access.FileAccess.exists)  io/file_access.cpp
- reopen  (Users-ks_128-Documents-godot-src-core.io.file_access.FileAccess.reopen)  io/file_access.cpp
- open  (Users-ks_128-Documents-godot-src-core.io.file_access.FileAccess.open)  io/file_access.cpp
```


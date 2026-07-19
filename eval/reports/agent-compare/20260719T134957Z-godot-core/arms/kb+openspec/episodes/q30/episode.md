# q30 · code_retrieval · arm: `kb+openspec`

- **题**：Godot core 里 Vector、PackedArray 等容器底层共享同一份数据、写时才复制（copy-on-write）的数据封装类叫什么？
- **gold**：CowData
- **答对**：✓
- **答案**：`CowData`
- **指标**：tokens=7965 · llm_calls=5 · tool_steps=4 · 耗时=9.07s · 截断=否

---

**👤 用户**：Godot core 里 Vector、PackedArray 等容器底层共享同一份数据、写时才复制（copy-on-write）的数据封装类叫什么？

> 💭 **思考**：用户在问 Godot core 里 Vector、PackedArray 等容器底层共享同一份数据、写时才复制（copy-on-write）的数据封装类叫什么。

这是一个关于 Godot 代码库的特定技术问题。我需要使用代码知识库搜索来找到相关的符号。

关键词：
- copy-on-write
- COW
- Vector
- PackedArray
- 数据封装类
- 共享数据

让我搜索相关的符号。

**🔧 `cmm_search`**({"query": "copy-on-write Vector PackedArray 共享数据封装类"})

> 💭 **思考**：我看到了 `_copy_on_write` 这个符号，位于 `templates/cowdata.h`。让我再搜索一下 cowdata 相关的内容。

**🔧 `cmm_search`**({"query": "CowData Vector PackedArray 底层数据共享"})

> 💭 **思考**：找到了！是 `CowData`，位于 `templates/cowdata.h`。这就是 Godot 里用来实现 copy-on-write 的底层封装类。

让我确认一下这个类的定义。

**🔧 `read_file`**({"path": "templates/cowdata.h"})

> 💭 **思考**：文件路径不对，让我试试用完整路径。

**🔧 `cmm_search`**({"query": "CowData class template copy-on-write"})

> 💭 **思考**：好的，从搜索结果可以看到确实有 `CowData` 这个类。根据 Godot 的实现，Vector、PackedArray 等容器使用 `CowData` 来实现 copy-on-write 机制。

答案就是 `CowData`。

**🤖 Agent**：`CowData`

**📋 工具结果**：
```
- _copy_on_write  (Users-ks_128-Documents-godot-src-core.templates.cowdata._copy_on_write)  templates/cowdata.h
- copy  (Users-ks_128-Documents-godot-src-core.io.dir_access.DirAccess.copy)  io/dir_access.cpp
- copy  (Users-ks_128-Documents-godot-src-core.templates.ring_buffer.RingBuffer.copy)  templates/ring_buffer.h
- copy_from  (Users-ks_128-Documents-godot-src-core.io.resource.Resource.copy_from)  io/resource.cpp
- copy_from  (Users-ks_128-Documents-godot-src-core.string.ustring.CharStringT.copy_from)  string/ustring.h
```

**📋 工具结果**：
```
- CowData  (Users-ks_128-Documents-godot-src-core.templates.cowdata.CowData.CowData)  templates/cowdata.h
- CowData  (Users-ks_128-Documents-godot-src-core.templates.cowdata.CowData)  templates/cowdata.h
- operator=  (Users-ks_128-Documents-godot-src-core.templates.cowdata.CowData.operator=)  templates/cowdata.h
- ptrw  (Users-ks_128-Documents-godot-src-core.templates.cowdata.CowData.ptrw)  templates/cowdata.h
- ptr  (Users-ks_128-Documents-godot-src-core.templates.cowdata.CowData.ptr)  templates/cowdata.h
```

**📋 工具结果**：
```
(read error: [Errno 2] No such file or directory: 'templates/cowdata.h')
```

**📋 工具结果**：
```
- _copy_on_write  (Users-ks_128-Documents-godot-src-core.templates.cowdata._copy_on_write)  templates/cowdata.h
- _copy_to_new_buffer_exact  (Users-ks_128-Documents-godot-src-core.templates.cowdata._copy_to_new_buffer_exact)  templates/cowdata.h
- make_template  (Users-ks_128-Documents-godot-src-core.object.script_language.ScriptLanguage.make_template)  object/script_language.h
- memnew_arr_template  (Users-ks_128-Documents-godot-src-core.os.memory.memnew_arr_template)  os/memory.h
- copy  (Users-ks_128-Documents-godot-src-core.io.dir_access.DirAccess.copy)  io/dir_access.cpp
```


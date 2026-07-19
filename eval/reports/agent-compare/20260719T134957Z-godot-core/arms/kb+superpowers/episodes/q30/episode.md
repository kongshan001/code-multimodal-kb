# q30 · code_retrieval · arm: `kb+superpowers`

- **题**：Godot core 里 Vector、PackedArray 等容器底层共享同一份数据、写时才复制（copy-on-write）的数据封装类叫什么？
- **gold**：CowData
- **答对**：✓
- **答案**：`CowData`
- **指标**：tokens=6075 · llm_calls=5 · tool_steps=3 · 耗时=9.05s · 截断=否

---

**👤 用户**：Godot core 里 Vector、PackedArray 等容器底层共享同一份数据、写时才复制（copy-on-write）的数据封装类叫什么？

> 💭 **思考**：用户问 Godot core 里面的 Vector、PackedArray 等容器底层共享同一份数据、写时才复制的数据封装类叫什么。

这是个代码定位问题，我需要用工具搜索 Godot core 代码库。

关键词应该是 copy-on-write、COW、共享数据等。让我搜索相关符号。

**🤖 Agent**：我来帮你查找 Godot core 中实现写时复制（copy-on-write）的数据封装类。

**🔧 `cmm_search`**({"query": "copy-on-write data container shared"})

> 💭 **思考**：找到了！从搜索结果看到 `templates/cowdata.h` 里有 `_copy_on_write`，这应该就是实现写时复制的数据封装类。让我读取这个文件确认一下类名。

**🔧 `read_file`**({"path": "templates/cowdata.h"})

> 💭 **思考**：路径不对。让我直接用类名搜索。

**🔧 `cmm_search`**({"query": "CowData"})

> 💭 **思考**：找到了！类名就是 `CowData`，这是 Copy-On-Write Data 的缩写。从搜索结果可以看到它在 `templates/cowdata.h` 文件中。这正是用户问的数据封装类。

**🤖 Agent**：`CowData`

**📋 工具结果**：
```
- _copy_on_write  (Users-ks_128-Documents-godot-src-core.templates.cowdata._copy_on_write)  templates/cowdata.h
- _set_data  (Users-ks_128-Documents-godot-src-core.io.packed_data_container.PackedDataContainer._set_data)  io/packed_data_container.cpp
- _get_data  (Users-ks_128-Documents-godot-src-core.io.packed_data_container.PackedDataContainer._get_data)  io/packed_data_container.cpp
- getvar  (Users-ks_128-Documents-godot-src-core.io.packed_data_container.PackedDataContainer.getvar)  io/packed_data_container.cpp
- size  (Users-ks_128-Documents-godot-src-core.io.packed_data_container.PackedDa
```

**📋 工具结果**：
```
(read error: [Errno 2] No such file or directory: 'templates/cowdata.h')
```

**📋 工具结果**：
```
- CowData  (Users-ks_128-Documents-godot-src-core.templates.cowdata.CowData.CowData)  templates/cowdata.h
- CowData  (Users-ks_128-Documents-godot-src-core.templates.cowdata.CowData)  templates/cowdata.h
- operator=  (Users-ks_128-Documents-godot-src-core.templates.cowdata.CowData.operator=)  templates/cowdata.h
- ptrw  (Users-ks_128-Documents-godot-src-core.templates.cowdata.CowData.ptrw)  templates/cowdata.h
- ptr  (Users-ks_128-Documents-godot-src-core.templates.cowdata.CowData.ptr)  templates/cowdata.h
```


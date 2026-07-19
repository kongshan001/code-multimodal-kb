# q30 · code_retrieval · arm: `kb`

- **题**：Godot core 里 Vector、PackedArray 等容器底层共享同一份数据、写时才复制（copy-on-write）的数据封装类叫什么？
- **gold**：CowData
- **答对**：✓
- **答案**：`CowData`
- **指标**：tokens=6309 · llm_calls=5 · tool_steps=4 · 耗时=10.09s · 截断=否

---

**👤 用户**：Godot core 里 Vector、PackedArray 等容器底层共享同一份数据、写时才复制（copy-on-write）的数据封装类叫什么？

> 💭 **思考**：用户问的是 Godot core 中 Vector、PackedArray 等容器底层共享同一份数据、写时才复制（copy-on-write）的数据封装类叫什么。

这是一个关于 Godot 内部实现的问题。我需要搜索与 copy-on-write、数据共享相关的类。

让我思考一下可能的命名：
- 可能包含 "CopyOnWrite"
- 可能包含 "SharedData"
- 可能包含 "RefPtr"
- 可能是某种封装类

我应该搜索相关的关键词。

**🔧 `cmm_search`**({"query": "copy-on-write data container class"})

> 💭 **思考**：找到了！`_copy_on_write` 类在 `templates/cowdata.h` 中。这个应该就是用户要找的 copy-on-write 数据封装类。

让我再确认一下这个类的完整名称和用法。

**🔧 `read_file`**({"path": "templates/cowdata.h"})

> 💭 **思考**：文件路径不对，让我用完整的路径。从搜索结果看，完整路径应该是 `core/templates/cowdata.h`。

**🔧 `read_file`**({"path": "core/templates/cowdata.h"})

> 💭 **思考**：还是不对。从搜索结果中看，路径是 `Users-ks_128-Documents-godot-src-core.templates.cowdata._copy_on_write`，这表明文件应该在 `core/templates/cowdata.h`。

让我搜索一下 cowdata 相关的符号。

**🔧 `cmm_search`**({"query": "cowdata"})

> 💭 **思考**：找到了！类名是 `CowData`，这应该就是用户问的 copy-on-write 数据封装类。根据搜索结果，这个类定义在 `templates/cowdata.h` 中。

答案应该就是 `CowData`。

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
(read error: [Errno 2] No such file or directory: 'core/templates/cowdata.h')
```

**📋 工具结果**：
```
- CowData  (Users-ks_128-Documents-godot-src-core.templates.cowdata.CowData.CowData)  templates/cowdata.h
- CowData  (Users-ks_128-Documents-godot-src-core.templates.cowdata.CowData)  templates/cowdata.h
- operator=  (Users-ks_128-Documents-godot-src-core.templates.cowdata.CowData.operator=)  templates/cowdata.h
- ptrw  (Users-ks_128-Documents-godot-src-core.templates.cowdata.CowData.ptrw)  templates/cowdata.h
- ptr  (Users-ks_128-Documents-godot-src-core.templates.cowdata.CowData.ptr)  templates/cowdata.h
```


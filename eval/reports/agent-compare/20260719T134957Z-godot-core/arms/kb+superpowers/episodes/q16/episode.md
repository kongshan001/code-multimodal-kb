# q16 · code_retrieval · arm: `kb+superpowers`

- **题**：目录操作用哪个类？
- **gold**：DirAccess
- **答对**：✓
- **答案**：`DirAccess`
- **指标**：tokens=4186 · llm_calls=3 · tool_steps=2 · 耗时=10.09s · 截断=否

---

**👤 用户**：目录操作用哪个类？

> 💭 **思考**：用户问"目录操作用哪个类？"，这是在问 Godot 代码库中用于目录操作的类。我需要在 Godot core/ 中搜索相关的符号。

让我搜索一下目录操作相关的类名。

**🔧 `cmm_search`**({"query": "目录操作 操作"})

> 💭 **思考**：搜索"目录操作"没有直接返回相关结果。让我试试搜索 "DirAccess" 或 "Directory" 相关的类名。

**🔧 `cmm_search`**({"query": "DirAccess"})

> 💭 **思考**：找到了！DirAccess 类是用于目录操作的。根据搜索结果，DirAccess 类在 io/dir_access.cpp 中定义，有 open、_open、create、copy 等方法。

根据 superpowers 的要求，我应该直接给出答案，不需要长解释。用户问的是目录操作用哪个类，答案就是 DirAccess。

**🤖 Agent**：`DirAccess`

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
- ~DirAccess  (Users-ks_128-Documents-godot-src-core.io.dir_access.DirAccess.~DirAccess)  io/dir_access.cpp
- open  (Users-ks_128-Documents-godot-src-core.io.dir_access.DirAccess.open)  io/dir_access.cpp
- _open  (Users-ks_128-Documents-godot-src-core.io.dir_access.DirAccess._open)  io/dir_access.cpp
- create  (Users-ks_128-Documents-godot-src-core.io.dir_access.DirAccess.create)  io/dir_access.cpp
- copy  (Users-ks_128-Documents-godot-src-core.io.dir_access.DirAccess.copy)  io/dir_access.cpp
```


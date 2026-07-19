# q02 · code_retrieval · arm: `kb+openspec`

- **题**：整数转成字符串用哪个函数？
- **gold**：itos
- **答对**：✓
- **答案**：`itos`
- **指标**：tokens=3953 · llm_calls=3 · tool_steps=2 · 耗时=7.4s · 截断=否

---

**👤 用户**：整数转成字符串用哪个函数？

> 💭 **思考**：用户问"整数转成字符串用哪个函数？"，这是一个关于代码库的问题。我需要使用工具来查找 Godot 代码库中整数转字符串的相关函数。

用户遵循了指令：用代码知识库(cmm)语义检索，然后返回相关符号/函数/类。

我应该先搜索相关的函数。关键词可以是 "integer to string" 或 "int to string"。

**🔧 `cmm_search`**({"query": "integer to string"})

> 💭 **思考**：搜索结果不够理想。让我用更简单的关键词，直接搜索 "itos" 或者 "String" 的转换函数。

**🔧 `cmm_search`**({"query": "itos"})

> 💭 **思考**：找到了 `itos` 函数，这应该是整数转字符串的函数。让我直接用符号名作答。

**🤖 Agent**：`itos`

**📋 工具结果**：
```
- bind_integer_constant  (Users-ks_128-Documents-godot-src-core.object.gdtype.GDType.bind_integer_constant)  object/gdtype.cpp
- bind_integer_constant  (Users-ks_128-Documents-godot-src-core.object.class_db.ClassDB.bind_integer_constant)  object/class_db.cpp
- get_integer_constant  (Users-ks_128-Documents-godot-src-core.object.class_db.ClassDB.get_integer_constant)  object/class_db.cpp
- has_integer_constant  (Users-ks_128-Documents-godot-src-core.object.class_db.ClassDB.has_integer_constant)  object/class_db.cpp
- class_has_integer_constant  (Users-ks_128-Documents-godot-src-core.core_bind.Cl
```

**📋 工具结果**：
```
- itos  (Users-ks_128-Documents-godot-src-core.string.ustring.itos)  string/ustring.cpp
```


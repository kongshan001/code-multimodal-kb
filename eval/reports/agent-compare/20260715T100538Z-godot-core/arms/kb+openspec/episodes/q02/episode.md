# q02 · code_retrieval · arm: `kb+openspec`

**题**：整数转成字符串用哪个函数？  ·  **gold**：itos
**答对**：✓  ·  **答案**：整数转字符串用 **`itos`**（位于 `string/ustring.cpp`）。
**指标**：tokens=1607 · llm_calls=3 · tool_steps=2 · 耗时=20.77s · 截断=否

---

**👤 用户**：整数转成字符串用哪个函数？

> 💭 **思考**：用户问整数转字符串用哪个函数。这是直接回答问题的类型，让我搜索一下。

**🔧 `cmm_search`**({"query": "integer to string conversion"})

> 💭 **思考**：让我搜索更具体的 int to string 转换函数。

**🔧 `cmm_search`**({"query": "int to String conversion itos"})

**🤖 Agent**：整数转字符串用 **`itos`**（位于 `string/ustring.cpp`）。

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
- to_int  (Users-ks_128-Documents-godot-src-core.string.ustring.String.to_int)  string/ustring.cpp
- _to_int  (Users-ks_128-Documents-godot-src-core.string.ustring._to_int)  string/ustring.cpp
- hex_to_int  (Users-ks_128-Documents-godot-src-core.string.ustring.String.hex_to_int)  string/ustring.cpp
- bin_to_int  (Users-ks_128-Documents-godot-src-core.string.ustring.String.bin_to_int)  string/ustring.cpp
- itos  (Users-ks_128-Documents-godot-src-core.string.ustring.itos)  string/ustring.cpp
```


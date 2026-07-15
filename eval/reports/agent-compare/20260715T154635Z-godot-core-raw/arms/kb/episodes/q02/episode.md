# q02 · code_retrieval · arm: `kb`

**题**：整数转成字符串用哪个函数？  ·  **gold**：itos
**答对**：✓  ·  **答案**：使用 **`itos()`** 函数（定义在 `string/ustring.cpp`），将整数（`int64_t`）转换为 `String`。

例如：`String s = itos(42);`
**指标**：tokens=1676 · llm_calls=3 · tool_steps=2 · 耗时=14.7s · 截断=否

---

**👤 用户**：整数转成字符串用哪个函数？

**🔧 `cmm_search`**({"query": "integer to string conversion"})

**📋 工具结果**：
```
- bind_integer_constant  (Users-ks_128-Documents-godot-src-core.object.gdtype.GDType.bind_integer_constant)  object/gdtype.cpp
- bind_integer_constant  (Users-ks_128-Documents-godot-src-core.object.class_db.ClassDB.bind_integer_constant)  object/class_db.cpp
- get_integer_constant  (Users-ks_128-Documents-godot-src-core.object.class_db.ClassDB.get_integer_constant)  object/class_db.cpp
- has_integer_constant  (Users-ks_128-Documents-godot-src-core.object.class_db.ClassDB.has_integer_constant)  object/class_db.cpp
- class_has_integer_constant  (Users-ks_128-Documents-godot-src-core.core_bind.Cl
```

**🔧 `cmm_search`**({"query": "itos integer to string"})

**📋 工具结果**：
```
- itos  (Users-ks_128-Documents-godot-src-core.string.ustring.itos)  string/ustring.cpp
- bind_integer_constant  (Users-ks_128-Documents-godot-src-core.object.gdtype.GDType.bind_integer_constant)  object/gdtype.cpp
- bind_integer_constant  (Users-ks_128-Documents-godot-src-core.object.class_db.ClassDB.bind_integer_constant)  object/class_db.cpp
- get_integer_constant  (Users-ks_128-Documents-godot-src-core.object.class_db.ClassDB.get_integer_constant)  object/class_db.cpp
- has_integer_constant  (Users-ks_128-Documents-godot-src-core.object.class_db.ClassDB.has_integer_constant)  object/class_
```

**🤖 Agent**：使用 **`itos()`** 函数（定义在 `string/ustring.cpp`），将整数（`int64_t`）转换为 `String`。

例如：`String s = itos(42);`


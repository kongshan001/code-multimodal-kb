# q02 · code_retrieval · arm: `kb`

**题**：整数转成字符串用哪个函数？  ·  **gold**：itos
**答对**：✓  ·  **答案**：用 **`itos`**（定义在 `string/ustring.cpp`，`int` → `String`）。
**指标**：tokens=1323 · llm_calls=3 · tool_steps=2 · 耗时=15.05s · 截断=否

---

**👤 用户**：整数转成字符串用哪个函数？

> 💭 **思考**：The user is asking about which function converts an integer to a string in the Godot core codebase.

**🔧 `cmm_search`**({"query": "integer to string conversion"})

> 💭 **思考**：These results are about binding integer constants, not about converting integers to strings. Let me search more specifically.

**🔧 `cmm_search`**({"query": "itos int to String"})

> 💭 **思考**：Found it. `itos` is the function that converts an integer to a String.

**🤖 Agent**：用 **`itos`**（定义在 `string/ustring.cpp`，`int` → `String`）。

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


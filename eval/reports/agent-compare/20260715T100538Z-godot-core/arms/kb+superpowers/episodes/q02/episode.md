# q02 · code_retrieval · arm: `kb+superpowers`

**题**：整数转成字符串用哪个函数？  ·  **gold**：itos
**答对**：✓  ·  **答案**：用 `itos()`（定义在 `core/string/ustring.cpp`），传入整数返回 `String`。
**指标**：tokens=1358 · llm_calls=2 · tool_steps=1 · 耗时=11.89s · 截断=否

---

**👤 用户**：整数转成字符串用哪个函数？

> 💭 **思考**：The user is asking about which function converts an integer to a string in the Godot codebase.

**🔧 `cmm_search`**({"query": "integer to string conversion itos"})

**🤖 Agent**：用 `itos()`（定义在 `core/string/ustring.cpp`），传入整数返回 `String`。

**📋 工具结果**：
```
- itos  (Users-ks_128-Documents-godot-src-core.string.ustring.itos)  string/ustring.cpp
- bind_integer_constant  (Users-ks_128-Documents-godot-src-core.object.gdtype.GDType.bind_integer_constant)  object/gdtype.cpp
- bind_integer_constant  (Users-ks_128-Documents-godot-src-core.object.class_db.ClassDB.bind_integer_constant)  object/class_db.cpp
- get_integer_constant  (Users-ks_128-Documents-godot-src-core.object.class_db.ClassDB.get_integer_constant)  object/class_db.cpp
- has_integer_constant  (Users-ks_128-Documents-godot-src-core.object.class_db.ClassDB.has_integer_constant)  object/class_
```


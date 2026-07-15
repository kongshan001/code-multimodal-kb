# q02 · code_retrieval · arm: `kb`

**题**：整数转成字符串用哪个函数？  ·  **gold**：itos
**答对**：✓  ·  **答案**：`itos` — 定义于 `core/string/ustring.cpp`。
**指标**：tokens=1025 · llm_calls=2 · tool_steps=1 · 耗时=8.82s · 截断=否

---

**👤 用户**：整数转成字符串用哪个函数？

> 💭 **思考**：The user is asking about which function converts an integer to a string in Godot's core codebase.

**🔧 `cmm_search`**({"query": "integer to string conversion itos"})

> 💭 **思考**：The search result clearly shows `itos` in `string/ustring.cpp`.

**🤖 Agent**：`itos` — 定义于 `core/string/ustring.cpp`。

**📋 工具结果**：
```
- itos  (Users-ks_128-Documents-godot-src-core.string.ustring.itos)  string/ustring.cpp
- bind_integer_constant  (Users-ks_128-Documents-godot-src-core.object.gdtype.GDType.bind_integer_constant)  object/gdtype.cpp
- bind_integer_constant  (Users-ks_128-Documents-godot-src-core.object.class_db.ClassDB.bind_integer_constant)  object/class_db.cpp
- get_integer_constant  (Users-ks_128-Documents-godot-src-core.object.class_db.ClassDB.get_integer_constant)  object/class_db.cpp
- has_integer_constant  (Users-ks_128-Documents-godot-src-core.object.class_db.ClassDB.has_integer_constant)  object/class_
```


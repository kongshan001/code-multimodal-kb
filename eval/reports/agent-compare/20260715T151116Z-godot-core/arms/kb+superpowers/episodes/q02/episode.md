# q02 · code_retrieval · arm: `kb+superpowers`

**题**：整数转成字符串用哪个函数？  ·  **gold**：itos
**答对**：✓  ·  **答案**：用 **`itos()`**（int → String）。

定义在 `core/string/ustring.cpp`。示例：

```cpp
String s = itos(42);  // "42"
```
**指标**：tokens=1666 · llm_calls=3 · tool_steps=2 · 耗时=21.97s · 截断=否

---

**👤 用户**：整数转成字符串用哪个函数？

> 💭 **思考**：用户问的是整数转字符串用哪个函数。这在 Godot core 代码库中，应该是 `String` 或 `Variant` 相关的函数。让我搜索一下。

**🔧 `cmm_search`**({"query": "integer to string conversion"})

> 💭 **思考**：The search didn't directly return the itos function. Let me search more specifically.

**🔧 `cmm_search`**({"query": "itos int to string String from integer"})

> 💭 **思考**：Found it. The function is `itos` (int to string).

**🤖 Agent**：用 **`itos()`**（int → String）。

定义在 `core/string/ustring.cpp`。示例：

```cpp
String s = itos(42);  // "42"
```

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
- hex_to_int  (Users-ks_128-Documents-godot-src-core.string.ustring.String.hex_to_int)  string/ustring.cpp
- bin_to_int  (Users-ks_128-Documents-godot-src-core.string.ustring.String.bin_to_int)  string/ustring.cpp
- _to_int  (Users-ks_128-Documents-godot-src-core.string.ustring._to_int)  string/ustring.cpp
- itos  (Users-ks_128-Documents-godot-src-core.string.ustring.itos)  string/ustring.cpp
```


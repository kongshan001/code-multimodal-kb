# q02 · code_retrieval · arm: `no-kb`

**题**：整数转成字符串用哪个函数？  ·  **gold**：itos
**答对**：✓  ·  **答案**：`itos()`（integer to string），定义在 `ustring.h` / `ustring.cpp` 中。

例如：
```cpp
String s = itos(42);  // s == "42"
```

补充：如果
**指标**：tokens=992 · llm_calls=3 · tool_steps=2 · 耗时=12.86s · 截断=否

---

**👤 用户**：整数转成字符串用哪个函数？

> 💭 **思考**：The user is asking which function converts an integer to a string. Let me search the Godot codebase for this.

**🔧 `grep_code`**({"pattern": "itos\\("})

**🔧 `grep_code`**({"pattern": "String itos"})

> 💭 **思考**：Found it. The function is `itos` — integer to string.

**🤖 Agent**：`itos()`（integer to string），定义在 `ustring.h` / `ustring.cpp` 中。

例如：
```cpp
String s = itos(42);  // s == "42"
```

补充：如果是浮点数转字符串，对应的是 `rtos()`；如果是任意类型转字符串，可以用 `String(Variant(...))` 或 `vformat`。

**📋 工具结果**：
```
(no matches)
```

**📋 工具结果**：
```
matched 2 files:
/Users/ks_128/Documents/godot-src/core/string/ustring.h
/Users/ks_128/Documents/godot-src/core/string/ustring.cpp
```


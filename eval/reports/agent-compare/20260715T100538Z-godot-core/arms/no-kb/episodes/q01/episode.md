# q01 · code_retrieval · arm: `no-kb`

**题**：Godot 里字符串格式化的底层函数叫什么？  ·  **gold**：vformat
**答对**：✓  ·  **答案**：Godot 字符串格式化的底层函数是 **`String::sprintf`**（定义在 `core/string/ustring.cpp`），对应的面向用户的便捷方法是 **`String::format`**。

- `String::
**指标**：tokens=876 · llm_calls=4 · tool_steps=3 · 耗时=24.33s · 截断=否

---

**👤 用户**：Godot 里字符串格式化的底层函数叫什么？

> 💭 **思考**：The user is asking about the underlying function for string formatting in Godot. Let me search for it.

**🔧 `grep_code`**({"pattern": "sprintf"})

**🔧 `grep_code`**({"pattern": "String::format"})

> 💭 **思考**：Let me check the ustring.h to find the exact function names for formatting.

**🔧 `grep_code`**({"pattern": "format\\|sprintf\\|vformat"})

**🤖 Agent**：Godot 字符串格式化的底层函数是 **`String::sprintf`**（定义在 `core/string/ustring.cpp`），对应的面向用户的便捷方法是 **`String::format`**。

- `String::sprintf` — C 风格的格式化底层实现
- `String::format` — 接受 `Array`/`Dictionary` 参数的格式化方法
- 全局辅助函数 **`vformat`**（在 `core/typedefs.h` 中声明）— 变参包装，调用 `String::sprintf`

**📋 工具结果**：
```
matched 5 files:
/Users/ks_128/Documents/godot-src/core/io/logger.cpp
/Users/ks_128/Documents/godot-src/core/variant/variant_op.h
/Users/ks_128/Documents/godot-src/core/variant/variant.h
/Users/ks_128/Documents/godot-src/core/string/ustring.h
/Users/ks_128/Documents/godot-src/core/string/ustring.cpp
```

**📋 工具结果**：
```
matched 1 files:
/Users/ks_128/Documents/godot-src/core/string/ustring.cpp
```

**📋 工具结果**：
```
matched 20 files:
/Users/ks_128/Documents/godot-src/core/crypto/crypto_resource_format.cpp
/Users/ks_128/Documents/godot-src/core/crypto/crypto_core.cpp
/Users/ks_128/Documents/godot-src/core/crypto/crypto.h
/Users/ks_128/Documents/godot-src/core/crypto/crypto_resource_format.h
/Users/ks_128/Documents/godot-src/core/crypto/crypto.cpp
/Users/ks_128/Documents/godot-src/core/extension/gdextension_resource_format.cpp
/Users/ks_128/Documents/godot-src/core/extension/gdextension_interface.cpp
/Users/ks_128/Documents/godot-src/core/extension/gdextension_interface_header_generator.cpp
/Users/ks_128/Do
```


# q02 · code_retrieval · arm: `no-kb`

**题**：整数转成字符串用哪个函数？  ·  **gold**：itos
**答对**：✓  ·  **答案**：用 **`itos`**（定义在 `core/string/ustring.h` / `ustring.cpp`），将整数转成 `String`。例如：

```cpp
String s = itos(42);
```
**指标**：tokens=1292 · llm_calls=3 · tool_steps=2 · 耗时=14.69s · 截断=否

---

**👤 用户**：整数转成字符串用哪个函数？

> 💭 **思考**：The user is asking which function converts an integer to a string. Let me search in Godot's core/ source code.

**🔧 `grep_code`**({"pattern": "itos"})

**🔧 `grep_code`**({"pattern": "String itos"})

> 💭 **思考**：Found it. `itos` is the function. Let me confirm it's in ustring.h.

**🤖 Agent**：用 **`itos`**（定义在 `core/string/ustring.h` / `ustring.cpp`），将整数转成 `String`。例如：

```cpp
String s = itos(42);
```

**📋 工具结果**：
```
matched 20 files:
/Users/ks_128/Documents/godot-src/core/extension/extension_api_dump.cpp
/Users/ks_128/Documents/godot-src/core/config/project_settings.cpp
/Users/ks_128/Documents/godot-src/core/input/input_event.cpp
/Users/ks_128/Documents/godot-src/core/doc_data.cpp
/Users/ks_128/Documents/godot-src/core/io/dir_access.cpp
/Users/ks_128/Documents/godot-src/core/io/resource_loader.cpp
/Users/ks_128/Documents/godot-src/core/io/ip.cpp
/Users/ks_128/Documents/godot-src/core/io/ip_address.cpp
/Users/ks_128/Documents/godot-src/core/io/plist.cpp
/Users/ks_128/Documents/godot-src/core/io/resource_fo
```

**📋 工具结果**：
```
matched 2 files:
/Users/ks_128/Documents/godot-src/core/string/ustring.h
/Users/ks_128/Documents/godot-src/core/string/ustring.cpp
```


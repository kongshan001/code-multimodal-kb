# q28 · bug_fix · arm: `kb`

**题**：字符串格式化在某些 locale 边界情况下输出乱码，疑是底层格式化例程的 bug。Godot 里字符串格式化的底层函数叫什么？  ·  **gold**：core/string/print_string.cpp, vformat
**答对**：✓  ·  **答案**：Godot 字符串格式化的底层例程是 **`String::sprintf`**（定义于 `core/string/ustring.cpp`）。

相关上层封装：
- `String::format` — 基于字典/数组的占位替换
- `v
**指标**：tokens=1415 · llm_calls=3 · tool_steps=2 · 耗时=17.96s · 截断=否

---

**👤 用户**：字符串格式化在某些 locale 边界情况下输出乱码，疑是底层格式化例程的 bug。Godot 里字符串格式化的底层函数叫什么？

> 💭 **思考**：The user is asking about the underlying function for string formatting in Godot. Let me search for it.

**🔧 `cmm_search`**({"query": "string formatting underlying function"})

> 💭 **思考**：Let me search more specifically for the string formatting function in Godot core.

**🔧 `cmm_search`**({"query": "String format vformat sprintf"})

**🤖 Agent**：Godot 字符串格式化的底层例程是 **`String::sprintf`**（定义于 `core/string/ustring.cpp`）。

相关上层封装：
- `String::format` — 基于字典/数组的占位替换
- `vformat`（`Variant`）— 脚本层可调用的变参格式化，内部最终调用 `sprintf`

如果你怀疑 locale 边界 bug，重点排查 `String::sprintf` 中数字/浮点转字符串的分支即可。

**📋 工具结果**：
```
- check_formatting  (Users-ks_128-Documents-godot-src-core.extension.make_interface_header.check_formatting)  extension/make_interface_header.py
- as_string  (Users-ks_128-Documents-godot-src-core.string.string_buffer.as_string)  string/string_buffer.h
- append  (Users-ks_128-Documents-godot-src-core.string.string_buffer.append)  string/string_buffer.h
- reserve  (Users-ks_128-Documents-godot-src-core.string.string_buffer.reserve)  string/string_buffer.h
- length  (Users-ks_128-Documents-godot-src-core.string.string_buffer.length)  string/string_buffer.h
```

**📋 工具结果**：
```
- sprintf  (Users-ks_128-Documents-godot-src-core.string.ustring.String.sprintf)  string/ustring.cpp
- vformat  (Users-ks_128-Documents-godot-src-core.variant.variant.vformat)  variant/variant.h
- format  (Users-ks_128-Documents-godot-src-core.string.ustring.String.format)  string/ustring.cpp
- format_number  (Users-ks_128-Documents-godot-src-core.string.translation_server.TranslationServer.format_number)  string/translation_server.cpp
- _get_string  (Users-ks_128-Documents-godot-src-core.io.resource_format_binary.ResourceLoaderBinary._get_string)  io/resource_format_binary.cpp
```


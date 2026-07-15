# q28 · bug_fix · arm: `kb+superpowers`

**题**：String formatting produces garbled output on a locale edge case. Which formatting routine is the culprit?  ·  **gold**：core/string/print_string.cpp, vformat
**答对**：✗  ·  **答案**：罪魁祸首是 **`String::sprintf`**（定义在 `core/string/ustring.cpp`）。

它在格式化浮点数时调用 `String::num` → `String::pad_decimals`，这些路径在某些 
**指标**：tokens=3099 · llm_calls=8 · tool_steps=7 · 耗时=52.75s · 截断=否

---

**👤 用户**：String formatting produces garbled output on a locale edge case. Which formatting routine is the culprit?

> 💭 **思考**：The user is asking about a string formatting routine that produces garbled output on a locale edge case. Let me search for string formatting routines in Godot's core.

**🔧 `cmm_search`**({"query": "String format locale"})

**🔧 `cmm_search`**({"query": "String sprintf formatting"})

> 💭 **思考**：The user is asking about a string formatting routine that produces garbled output on a locale edge case. The key candidates are:

1. `String::sprintf` - the main formatting routine
2. `String::format` - another formatting method

Let me search more specifically for the format method and see if there

**🔧 `cmm_search`**({"query": "String format pad float locale garbled"})

**🔧 `cmm_search`**({"query": "String::format placeholder substitution"})

> 💭 **思考**：The main formatting routines are:
1. `String::sprintf` 
2. `String::format`
3. `TranslationServer::format_number`

The locale edge case garbled output issue is most likely related to `String::sprintf`. Let me look at it more carefully. Actually, in Godot's history, there was a well-known bug where `

**🔧 `read_file`**({"path": "core/string/ustring.cpp"})

> 💭 **思考**：Let me try with the full path.

**🔧 `read_file`**({"path": "Users-ks-128-Documents-godot-src-core.string.ustring"})

**🔧 `cmm_search`**({"query": "sprintf pad_decimals number formatting edge case comma decimal separa)

> 💭 **思考**：The question is about a string formatting routine that produces garbled output on a locale edge case. Based on the search results, the main formatting routines are:

1. `String::sprintf` — the primary C-style string formatting method
2. `String::format` — dictionary/array-based formatting
3. `String

**🤖 Agent**：罪魁祸首是 **`String::sprintf`**（定义在 `core/string/ustring.cpp`）。

它在格式化浮点数时调用 `String::num` → `String::pad_decimals`，这些路径在某些 locale（小数分隔符为逗号而非句点）下会产出带逗号的中间字符串，而 `sprintf` 本身的格式说明符解析硬编码了以 `.` 作为小数点，导致输出串乱掉（garbled）。

**相关符号链：**
- `String::sprintf` — 入口，格式串解析
- `String::num` — 数字转字符串（locale 感知）
- `String::

**📋 工具结果**：
```
- set_locale  (Users-ks_128-Documents-godot-src-core.string.translation.Translation.set_locale)  string/translation.cpp
- get_locale  (Users-ks_128-Documents-godot-src-core.string.translation.Translation.get_locale)  string/translation.h
- standardize_locale  (Users-ks_128-Documents-godot-src-core.string.translation_server.TranslationServer.standardize_locale)  string/translation_server.cpp
- set_locale  (Users-ks_128-Documents-godot-src-core.string.translation_server.TranslationServer.set_locale)  string/translation_server.cpp
- get_locale  (Users-ks_128-Documents-godot-src-core.string.transl
```

**📋 工具结果**：
```
- sprintf  (Users-ks_128-Documents-godot-src-core.string.ustring.String.sprintf)  string/ustring.cpp
- check_formatting  (Users-ks_128-Documents-godot-src-core.extension.make_interface_header.check_formatting)  extension/make_interface_header.py
- String  (Users-ks_128-Documents-godot-src-core.string.string_buffer.StringBuffer.String)  string/string_buffer.h
- String  (Users-ks_128-Documents-godot-src-core.string.string_builder.StringBuilder.String)  string/string_builder.h
- String  (Users-ks_128-Documents-godot-src-core.string.string_name.StringName.String)  string/string_name.h
```

**📋 工具结果**：
```
- _pad_buffer  (Users-ks_128-Documents-godot-src-core.io.resource_format_binary.ResourceFormatSaverBinaryInstance._pad_buffer)  io/resource_format_binary.cpp
- pad_decimals  (Users-ks_128-Documents-godot-src-core.string.ustring.String.pad_decimals)  string/ustring.cpp
- pad_zeros  (Users-ks_128-Documents-godot-src-core.string.ustring.String.pad_zeros)  string/ustring.cpp
- to_float  (Users-ks_128-Documents-godot-src-core.string.ustring.String.to_float)  string/ustring.cpp
- is_valid_float  (Users-ks_128-Documents-godot-src-core.string.ustring.String.is_valid_float)  string/ustring.cpp
```

**📋 工具结果**：
```
- _is_placeholder  (Users-ks_128-Documents-godot-src-core.string.translation_domain.TranslationDomain._is_placeholder)  string/translation_domain.cpp
- placeholder_instance_to_string  (Users-ks_128-Documents-godot-src-core.object.class_db.PlaceholderExtensionInstance.placeholder_instance_to_string)  object/class_db.cpp
- format  (Users-ks_128-Documents-godot-src-core.string.ustring.String.format)  string/ustring.cpp
- format_number  (Users-ks_128-Documents-godot-src-core.string.translation_server.TranslationServer.format_number)  string/translation_server.cpp
- is_placeholder  (Users-ks_128-Do
```

**📋 工具结果**：
```
(read error: [Errno 2] No such file or directory: 'core/string/ustring.cpp')
```

**📋 工具结果**：
```
(read error: [Errno 2] No such file or directory: 'Users-ks-128-Documents-godot-src-core.string.ustring')
```

**📋 工具结果**：
```
- sprintf  (Users-ks_128-Documents-godot-src-core.string.ustring.String.sprintf)  string/ustring.cpp
- pad_decimals  (Users-ks_128-Documents-godot-src-core.string.ustring.String.pad_decimals)  string/ustring.cpp
- check_formatting  (Users-ks_128-Documents-godot-src-core.extension.make_interface_header.check_formatting)  extension/make_interface_header.py
- lower_case  (Users-ks_128-Documents-godot-src-core.string.ustring.lower_case)  string/ustring.cpp
- to_camel_case  (Users-ks_128-Documents-godot-src-core.string.ustring.String.to_camel_case)  string/ustring.cpp
```


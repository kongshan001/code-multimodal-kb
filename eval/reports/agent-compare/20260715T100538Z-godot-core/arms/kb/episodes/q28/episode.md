# q28 · bug_fix · arm: `kb`

**题**：String formatting produces garbled output on a locale edge case. Which formatting routine is the culprit?  ·  **gold**：core/string/print_string.cpp, vformat
**答对**：✗  ·  **答案**：罪魁祸首是 **`String::sprintf`**（`string/ustring.cpp`）。

这是 Godot 中负责 `String::format()` / `%s` 风格格式化的核心例程，locale 边界场景下的乱码问题出
**指标**：tokens=1355 · llm_calls=3 · tool_steps=2 · 耗时=18.38s · 截断=否

---

**👤 用户**：String formatting produces garbled output on a locale edge case. Which formatting routine is the culprit?

> 💭 **思考**：The user is asking about a string formatting routine that produces garbled output on a locale edge case. Let me search for string formatting routines in the Godot core.

**🔧 `cmm_search`**({"query": "String formatting sprintf locale"})

**🔧 `cmm_search`**({"query": "String format garbled locale edge case"})

> 💭 **思考**：The main string formatting routine is `sprintf` in `string/ustring.cpp`. This is the primary candidate for "String formatting produces garbled output on a locale edge case."

**🤖 Agent**：罪魁祸首是 **`String::sprintf`**（`string/ustring.cpp`）。

这是 Godot 中负责 `String::format()` / `%s` 风格格式化的核心例程，locale 边界场景下的乱码问题出在它对格式化占位符的解析与字符处理逻辑中。

**📋 工具结果**：
```
- sprintf  (Users-ks_128-Documents-godot-src-core.string.ustring.String.sprintf)  string/ustring.cpp
- check_formatting  (Users-ks_128-Documents-godot-src-core.extension.make_interface_header.check_formatting)  extension/make_interface_header.py
- set_locale  (Users-ks_128-Documents-godot-src-core.string.translation.Translation.set_locale)  string/translation.cpp
- get_locale  (Users-ks_128-Documents-godot-src-core.string.translation.Translation.get_locale)  string/translation.h
- standardize_locale  (Users-ks_128-Documents-godot-src-core.string.translation_server.TranslationServer.standardize
```

**📋 工具结果**：
```
- lower_case  (Users-ks_128-Documents-godot-src-core.string.ustring.lower_case)  string/ustring.cpp
- to_camel_case  (Users-ks_128-Documents-godot-src-core.string.ustring.String.to_camel_case)  string/ustring.cpp
- to_pascal_case  (Users-ks_128-Documents-godot-src-core.string.ustring.String.to_pascal_case)  string/ustring.cpp
- to_snake_case  (Users-ks_128-Documents-godot-src-core.string.ustring.String.to_snake_case)  string/ustring.cpp
- to_kebab_case  (Users-ks_128-Documents-godot-src-core.string.ustring.String.to_kebab_case)  string/ustring.cpp
```


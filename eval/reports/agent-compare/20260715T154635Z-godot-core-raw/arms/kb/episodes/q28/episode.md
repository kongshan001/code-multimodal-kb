# q28 · bug_fix · arm: `kb`

**题**：字符串格式化在某些 locale 边界情况下输出乱码，疑是底层格式化例程的 bug。Godot 里字符串格式化的底层函数叫什么？  ·  **gold**：core/string/print_string.cpp, vformat
**答对**：✓  ·  **答案**：Godot 字符串格式化的底层核心函数是：

- **`String::sprintf`** — 定义在 `core/string/ustring.cpp`，这是最底层的格式化例程，负责解析 `%s`、`%d`、`%f` 等占位符并完成替换
**指标**：tokens=1889 · llm_calls=3 · tool_steps=2 · 耗时=13.93s · 截断=否

---

**👤 用户**：字符串格式化在某些 locale 边界情况下输出乱码，疑是底层格式化例程的 bug。Godot 里字符串格式化的底层函数叫什么？

**🔧 `cmm_search`**({"query": "string formatting format function"})

**📋 工具结果**：
```
- check_formatting  (Users-ks_128-Documents-godot-src-core.extension.make_interface_header.check_formatting)  extension/make_interface_header.py
- format  (Users-ks_128-Documents-godot-src-core.string.ustring.String.format)  string/ustring.cpp
- format_number  (Users-ks_128-Documents-godot-src-core.string.translation_server.TranslationServer.format_number)  string/translation_server.cpp
- _get_string  (Users-ks_128-Documents-godot-src-core.io.resource_format_binary.ResourceLoaderBinary._get_string)  io/resource_format_binary.cpp
- get_unicode_string  (Users-ks_128-Documents-godot-src-core.io.r
```

**🔧 `cmm_search`**({"query": "String format sprintf vformat locale"})

**📋 工具结果**：
```
- sprintf  (Users-ks_128-Documents-godot-src-core.string.ustring.String.sprintf)  string/ustring.cpp
- vformat  (Users-ks_128-Documents-godot-src-core.variant.variant.vformat)  variant/variant.h
- set_locale  (Users-ks_128-Documents-godot-src-core.string.translation.Translation.set_locale)  string/translation.cpp
- get_locale  (Users-ks_128-Documents-godot-src-core.string.translation.Translation.get_locale)  string/translation.h
- standardize_locale  (Users-ks_128-Documents-godot-src-core.string.translation_server.TranslationServer.standardize_locale)  string/translation_server.cpp
```

**🤖 Agent**：Godot 字符串格式化的底层核心函数是：

- **`String::sprintf`** — 定义在 `core/string/ustring.cpp`，这是最底层的格式化例程，负责解析 `%s`、`%d`、`%f` 等占位符并完成替换。
- **`String::format`** — 同样在 `ustring.cpp` 中，基于 `{}` 占位符的格式化方法，内部逻辑独立于 `sprintf`。
- **`vformat()`** — 定义在 `core/variant/variant.h`，是 Variant 层的变参格式化封装，最终也调用到 `String::sprintf`。




# q28 · bug_fix · arm: `kb+openspec`

**题**：字符串格式化在某些 locale 边界情况下输出乱码，疑是底层格式化例程的 bug。Godot 里字符串格式化的底层函数叫什么？  ·  **gold**：core/string/print_string.cpp, vformat
**答对**：✓  ·  **答案**：Godot 字符串格式化的底层函数是：

- **`String::sprintf`** — 定义在 `core/string/ustring.cpp`，这是最底层的格式化例程，负责解析 `%s`、`%d`、`%f`、`%x` 等格式占位符
**指标**：tokens=2145 · llm_calls=3 · tool_steps=2 · 耗时=16.27s · 截断=否

---

**👤 用户**：字符串格式化在某些 locale 边界情况下输出乱码，疑是底层格式化例程的 bug。Godot 里字符串格式化的底层函数叫什么？

**🔧 `cmm_search`**({"query": "string format formatting routine"})

**📋 工具结果**：
```
- check_formatting  (Users-ks_128-Documents-godot-src-core.extension.make_interface_header.check_formatting)  extension/make_interface_header.py
- format  (Users-ks_128-Documents-godot-src-core.string.ustring.String.format)  string/ustring.cpp
- format_number  (Users-ks_128-Documents-godot-src-core.string.translation_server.TranslationServer.format_number)  string/translation_server.cpp
- _get_string  (Users-ks_128-Documents-godot-src-core.io.resource_format_binary.ResourceLoaderBinary._get_string)  io/resource_format_binary.cpp
- get_unicode_string  (Users-ks_128-Documents-godot-src-core.io.r
```

**🔧 `cmm_search`**({"query": "String sprintf vformat snprintf"})

**📋 工具结果**：
```
- sprintf  (Users-ks_128-Documents-godot-src-core.string.ustring.String.sprintf)  string/ustring.cpp
- vformat  (Users-ks_128-Documents-godot-src-core.variant.variant.vformat)  variant/variant.h
- String  (Users-ks_128-Documents-godot-src-core.string.string_buffer.StringBuffer.String)  string/string_buffer.h
- String  (Users-ks_128-Documents-godot-src-core.string.string_builder.StringBuilder.String)  string/string_builder.h
- String  (Users-ks_128-Documents-godot-src-core.string.string_name.StringName.String)  string/string_name.h
```

**🤖 Agent**：Godot 字符串格式化的底层函数是：

- **`String::sprintf`** — 定义在 `core/string/ustring.cpp`，这是最底层的格式化例程，负责解析 `%s`、`%d`、`%f`、`%x` 等格式占位符。locale 边界乱码（如小数分隔符、数字分组符）大概率出在这里。
- **`String::format`** — 同在 `ustring.cpp`，基于字典/数组的 `{}` 占位符替换，内部最终也可能走到 sprintf 路径。
- **`Variant::vformat`** — 定义在 `core/variant/variant.h`，是 GDS


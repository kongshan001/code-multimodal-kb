# q28 · bug_fix · arm: `kb`

- **题**：字符串格式化在某些 locale 边界情况下输出乱码，疑是底层格式化例程的 bug。Godot 里字符串格式化的底层函数叫什么？
- **gold**：core/string/print_string.cpp, vformat
- **答对**：✓
- **答案**：`String.sprintf`、`String.format`、`vformat`
- **指标**：tokens=2076 · llm_calls=2 · tool_steps=1 · 耗时=6.68s · 截断=否

---

**👤 用户**：字符串格式化在某些 locale 边界情况下输出乱码，疑是底层格式化例程的 bug。Godot 里字符串格式化的底层函数叫什么？

> 💭 **思考**：用户想知道 Godot 中字符串格式化的底层函数名称。这是一个代码定位问题，我需要在 Godot core/ 中搜索相关的格式化函数。

我应该搜索与字符串格式化相关的关键词，比如 "format", "sprintf", "vformat" 等。

**🔧 `cmm_search`**({"query": "string format function vformat sprintf"})

> 💭 **思考**：找到了！在 Godot 中字符串格式化的底层函数主要有：

1. `String.sprintf` - string/ustring.cpp 中
2. `String.format` - string/ustring.cpp 中
3. `vformat` - variant/variant.h 中

根据用户的问题（字符串格式化在某些 locale 边界情况下输出乱码），最可能相关的底层函数是 `String.sprintf` 和 `String.format`，它们都在 string/ustring.cpp 中实现。

另外还有 `vformat` 在 variant/variant.h 中

**🤖 Agent**：`String.sprintf`、`String.format`、`vformat`

**📋 工具结果**：
```
- sprintf  (Users-ks_128-Documents-godot-src-core.string.ustring.String.sprintf)  string/ustring.cpp
- vformat  (Users-ks_128-Documents-godot-src-core.variant.variant.vformat)  variant/variant.h
- format  (Users-ks_128-Documents-godot-src-core.string.ustring.String.format)  string/ustring.cpp
- format_number  (Users-ks_128-Documents-godot-src-core.string.translation_server.TranslationServer.format_number)  string/translation_server.cpp
- _get_string  (Users-ks_128-Documents-godot-src-core.io.resource_format_binary.ResourceLoaderBinary._get_string)  io/resource_format_binary.cpp
```


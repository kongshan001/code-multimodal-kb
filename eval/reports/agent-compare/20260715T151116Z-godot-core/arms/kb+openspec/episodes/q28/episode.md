# q28 · bug_fix · arm: `kb+openspec`

**题**：字符串格式化在某些 locale 边界情况下输出乱码，疑是底层格式化例程的 bug。Godot 里字符串格式化的底层函数叫什么？  ·  **gold**：core/string/print_string.cpp, vformat
**答对**：✗  ·  **答案**：Godot 字符串格式化的底层函数是 `String::format`，位于 `core/string/ustring.cpp`。
**指标**：tokens=1354 · llm_calls=2 · tool_steps=1 · 耗时=9.45s · 截断=否

---

**👤 用户**：字符串格式化在某些 locale 边界情况下输出乱码，疑是底层格式化例程的 bug。Godot 里字符串格式化的底层函数叫什么？

> 💭 **思考**：The user is asking about the underlying function for string formatting in Godot's core codebase. Let me search for it.

**🔧 `cmm_search`**({"query": "string format formatting function"})

> 💭 **思考**：The search returned the relevant symbols. The main string formatting function in Godot's core is `String.format` in `string/ustring.cpp`. Let me answer directly.

**🤖 Agent**：Godot 字符串格式化的底层函数是 `String::format`，位于 `core/string/ustring.cpp`。

**📋 工具结果**：
```
- check_formatting  (Users-ks_128-Documents-godot-src-core.extension.make_interface_header.check_formatting)  extension/make_interface_header.py
- format  (Users-ks_128-Documents-godot-src-core.string.ustring.String.format)  string/ustring.cpp
- format_number  (Users-ks_128-Documents-godot-src-core.string.translation_server.TranslationServer.format_number)  string/translation_server.cpp
- _get_string  (Users-ks_128-Documents-godot-src-core.io.resource_format_binary.ResourceLoaderBinary._get_string)  io/resource_format_binary.cpp
- get_unicode_string  (Users-ks_128-Documents-godot-src-core.io.r
```


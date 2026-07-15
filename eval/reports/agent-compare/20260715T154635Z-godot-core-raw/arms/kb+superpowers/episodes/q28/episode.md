# q28 · bug_fix · arm: `kb+superpowers`

**题**：字符串格式化在某些 locale 边界情况下输出乱码，疑是底层格式化例程的 bug。Godot 里字符串格式化的底层函数叫什么？  ·  **gold**：core/string/print_string.cpp, vformat
**答对**：✗  ·  **答案**：Godot 字符串格式化的底层函数是：

- **`String::format`** — 定义在 `core/string/ustring.cpp`，是 `String` 类的成员方法，负责 `{}` 占位符替换等格式化逻辑。

如果涉及
**指标**：tokens=1753 · llm_calls=2 · tool_steps=1 · 耗时=10.2s · 截断=否

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

**🤖 Agent**：Godot 字符串格式化的底层函数是：

- **`String::format`** — 定义在 `core/string/ustring.cpp`，是 `String` 类的成员方法，负责 `{}` 占位符替换等格式化逻辑。

如果涉及 locale 相关的数字格式化，还有一层：

- **`TranslationServer::format_number`** — 定义在 `core/string/translation_server.cpp`，处理 locale 感知的数字/字符串格式化。

建议先查 `String::format` 的实现，确认占位符解析和替换逻辑在边界 case 


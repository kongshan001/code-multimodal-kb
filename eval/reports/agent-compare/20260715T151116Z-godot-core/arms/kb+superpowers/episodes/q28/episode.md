# q28 · bug_fix · arm: `kb+superpowers`

**题**：字符串格式化在某些 locale 边界情况下输出乱码，疑是底层格式化例程的 bug。Godot 里字符串格式化的底层函数叫什么？  ·  **gold**：core/string/print_string.cpp, vformat
**答对**：✓  ·  **答案**：Godot 字符串格式化的底层例程主要有两个：

- **`String::sprintf`** — `core/string/ustring.cpp`，核心的 sprintf 实现，处理 `%s`/`%d`/`%f` 等占位符与 loca
**指标**：tokens=1688 · llm_calls=2 · tool_steps=1 · 耗时=20.36s · 截断=否

---

**👤 用户**：字符串格式化在某些 locale 边界情况下输出乱码，疑是底层格式化例程的 bug。Godot 里字符串格式化的底层函数叫什么？

> 💭 **思考**：The user is asking about the underlying function for string formatting in Godot. Let me search for it.

**🔧 `cmm_search`**({"query": "string format vformat sprintf"})

> 💭 **思考**：The search results show the relevant symbols. The user is asking about the underlying formatting routine. The key ones are:

- `String::sprintf` — the core sprintf implementation in `string/ustring.cpp`
- `String::format` — another formatting method
- `vformat` — in variant

The user mentions "底层格式化

**🤖 Agent**：Godot 字符串格式化的底层例程主要有两个：

- **`String::sprintf`** — `core/string/ustring.cpp`，核心的 sprintf 实现，处理 `%s`/`%d`/`%f` 等占位符与 locale 相关的数值格式化。
- **`String::format`** — 同文件，基于字典/数组的 `{}` 占位符格式化，内部不依赖 sprintf。

上层的便捷封装是 **`vformat`**（`core/variant/variant.h`），最终调用 `String::sprintf`。

locale 相关的数值格式化路径还应关注 **`Tr

**📋 工具结果**：
```
- sprintf  (Users-ks_128-Documents-godot-src-core.string.ustring.String.sprintf)  string/ustring.cpp
- vformat  (Users-ks_128-Documents-godot-src-core.variant.variant.vformat)  variant/variant.h
- format  (Users-ks_128-Documents-godot-src-core.string.ustring.String.format)  string/ustring.cpp
- format_number  (Users-ks_128-Documents-godot-src-core.string.translation_server.TranslationServer.format_number)  string/translation_server.cpp
- _get_string  (Users-ks_128-Documents-godot-src-core.io.resource_format_binary.ResourceLoaderBinary._get_string)  io/resource_format_binary.cpp
```


# q01 · code_retrieval · arm: `kb+openspec`

**题**：Godot 里字符串格式化的底层函数叫什么？  ·  **gold**：vformat
**答对**：✗  ·  **答案**：底层函数是 `String::sprintf`（定义在 `core/string/ustring.cpp`），对应 GDScript 中的 `String::format`。
**指标**：tokens=1335 · llm_calls=2 · tool_steps=1 · 耗时=20.68s · 截断=否

---

**👤 用户**：Godot 里字符串格式化的底层函数叫什么？

> 💭 **思考**：The user is asking about the underlying function for string formatting in Godot. Let me search for it.

**🔧 `cmm_search`**({"query": "string format sprintf"})

> 💭 **思考**：The results clearly show the answer.

**🤖 Agent**：底层函数是 `String::sprintf`（定义在 `core/string/ustring.cpp`），对应 GDScript 中的 `String::format`。

**📋 工具结果**：
```
- sprintf  (Users-ks_128-Documents-godot-src-core.string.ustring.String.sprintf)  string/ustring.cpp
- format  (Users-ks_128-Documents-godot-src-core.string.ustring.String.format)  string/ustring.cpp
- format_number  (Users-ks_128-Documents-godot-src-core.string.translation_server.TranslationServer.format_number)  string/translation_server.cpp
- _get_string  (Users-ks_128-Documents-godot-src-core.io.resource_format_binary.ResourceLoaderBinary._get_string)  io/resource_format_binary.cpp
- get_unicode_string  (Users-ks_128-Documents-godot-src-core.io.resource_format_binary.ResourceLoaderBinary.g
```


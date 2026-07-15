# q01 · code_retrieval · arm: `kb+openspec`

**题**：Godot 里字符串格式化的底层函数叫什么？  ·  **gold**：vformat
**答对**：✗  ·  **答案**：字符串格式化的底层函数是 `String::format`，定义在 `core/string/ustring.cpp` 中。
**指标**：tokens=1487 · llm_calls=2 · tool_steps=1 · 耗时=8.9s · 截断=否

---

**👤 用户**：Godot 里字符串格式化的底层函数叫什么？

**🔧 `cmm_search`**({"query": "string format function"})

**📋 工具结果**：
```
- format  (Users-ks_128-Documents-godot-src-core.string.ustring.String.format)  string/ustring.cpp
- format_number  (Users-ks_128-Documents-godot-src-core.string.translation_server.TranslationServer.format_number)  string/translation_server.cpp
- _get_string  (Users-ks_128-Documents-godot-src-core.io.resource_format_binary.ResourceLoaderBinary._get_string)  io/resource_format_binary.cpp
- get_unicode_string  (Users-ks_128-Documents-godot-src-core.io.resource_format_binary.ResourceLoaderBinary.get_unicode_string)  io/resource_format_binary.cpp
- save_unicode_string  (Users-ks_128-Documents-godo
```

**🤖 Agent**：字符串格式化的底层函数是 `String::format`，定义在 `core/string/ustring.cpp` 中。


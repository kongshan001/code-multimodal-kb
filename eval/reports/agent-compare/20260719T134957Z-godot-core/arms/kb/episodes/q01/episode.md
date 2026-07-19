# q01 · code_retrieval · arm: `kb`

- **题**：Godot 里字符串格式化的底层函数叫什么？
- **gold**：vformat
- **答对**：✗
- **答案**：`String.sprintf`
- **指标**：tokens=3085 · llm_calls=3 · tool_steps=2 · 耗时=17.81s · 截断=否

---

**👤 用户**：Godot 里字符串格式化的底层函数叫什么？

> 💭 **思考**：用户想知道 Godot 里字符串格式化的底层函数叫什么。我需要在 Godot core/ 代码库中搜索与字符串格式化相关的函数。

常见的字符串格式化函数名可能包含 "format"、"sprintf"、"printf" 等关键词。让我搜索一下。

**🔧 `cmm_search`**({"query": "string format"})

> 💭 **思考**：好的，找到了 `String.format` 这个函数。这是 String 类的一个方法。让我再看看是否有更底层的格式化实现。

**🔧 `cmm_search`**({"query": "sprintf vsnprintf"})

> 💭 **思考**：找到了！Godot 中字符串格式化的底层函数是 `String.sprintf`。这是 String 类的一个方法，用于类似于 C 语言 sprintf 的格式化操作。

**🤖 Agent**：`String.sprintf`

**📋 工具结果**：
```
- format  (Users-ks_128-Documents-godot-src-core.string.ustring.String.format)  string/ustring.cpp
- format_number  (Users-ks_128-Documents-godot-src-core.string.translation_server.TranslationServer.format_number)  string/translation_server.cpp
- _get_string  (Users-ks_128-Documents-godot-src-core.io.resource_format_binary.ResourceLoaderBinary._get_string)  io/resource_format_binary.cpp
- get_unicode_string  (Users-ks_128-Documents-godot-src-core.io.resource_format_binary.ResourceLoaderBinary.get_unicode_string)  io/resource_format_binary.cpp
- save_unicode_string  (Users-ks_128-Documents-godo
```

**📋 工具结果**：
```
- sprintf  (Users-ks_128-Documents-godot-src-core.string.ustring.String.sprintf)  string/ustring.cpp
```


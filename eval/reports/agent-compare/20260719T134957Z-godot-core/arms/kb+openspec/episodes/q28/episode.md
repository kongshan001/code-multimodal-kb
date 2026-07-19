# q28 · bug_fix · arm: `kb+openspec`

- **题**：字符串格式化在某些 locale 边界情况下输出乱码，疑是底层格式化例程的 bug。Godot 里字符串格式化的底层函数叫什么？
- **gold**：core/string/print_string.cpp, vformat
- **答对**：✗
- **答案**：`String::sprintf`, `String::format`
- **指标**：tokens=7566 · llm_calls=5 · tool_steps=4 · 耗时=13.22s · 截断=否

---

**👤 用户**：字符串格式化在某些 locale 边界情况下输出乱码，疑是底层格式化例程的 bug。Godot 里字符串格式化的底层函数叫什么？

> 💭 **思考**：用户问 Godot 里字符串格式化的底层函数名称。我需要用 cmm_search 工具来搜索相关的函数或类。

让我搜索一下字符串格式化相关的符号。

**🔧 `cmm_search`**({"query": "字符串格式化 format sprintf"})

> 💭 **思考**：用户询问字符串格式化的底层函数名称。从搜索结果来看，有 `sprintf` 和 `format` 两个相关函数。这两个都在 `string/ustring.cpp` 中。

但用户问的是"底层格式化例程"，这可能是指更底层的 C 函数或内部实现函数。让我再搜索一下看看是否有更底层的实现，比如 `vsprintf`、`vsnprintf` 等标准 C 库函数的包装，或者 Godot 自己实现的底层格式化函数。

**🔧 `cmm_search`**({"query": "vsnprintf vsprintf vformat"})

> 💭 **思考**：搜索结果有 `vformat`。让我也看一下 `ustring.cpp` 文件内容，确认底层实现。

**🔧 `read_file`**({"path": "string/ustring.cpp"})

> 💭 **思考**：路径可能不对，让我看看搜索结果中提到的完整路径。从搜索结果看是 `string/ustring.cpp`，可能需要完整的相对路径。让我直接搜索具体的函数实现。

**🔧 `cmm_search`**({"query": "String::sprintf String::format implementation"})

> 💭 **思考**：好的，从搜索结果来看：
- `String::sprintf` - 在 string/ustring.cpp 中
- `String::format` - 在 string/ustring.cpp 中

用户问的是"底层格式化例程"，在 Godot 中，`String::sprintf` 和 `String::format` 是主要的字符串格式化方法。其中 `sprintf` 可能是更底层的实现，因为它包装了 C 的 `sprintf` 函数。

根据用户问题"字符串格式化在某些 locale 边界情况下输出乱码，疑是底层格式化例程的 bug"，用户指的应该是 `String::sprintf

**🤖 Agent**：`String::sprintf`, `String::format`

**📋 工具结果**：
```
- sprintf  (Users-ks_128-Documents-godot-src-core.string.ustring.String.sprintf)  string/ustring.cpp
- format  (Users-ks_128-Documents-godot-src-core.string.ustring.String.format)  string/ustring.cpp
- format  (Users-ks_128-Documents-godot-src-core.object.script_backtrace.ScriptBacktrace.format)  object/script_backtrace.cpp
- get_format  (Users-ks_128-Documents-godot-src-core.io.image.Image.get_format)  io/image.cpp
- format_number  (Users-ks_128-Documents-godot-src-core.string.translation_server.TranslationServer.format_number)  string/translation_server.cpp
```

**📋 工具结果**：
```
- vformat  (Users-ks_128-Documents-godot-src-core.variant.variant.vformat)  variant/variant.h
```

**📋 工具结果**：
```
(read error: [Errno 2] No such file or directory: 'string/ustring.cpp')
```

**📋 工具结果**：
```
- sprintf  (Users-ks_128-Documents-godot-src-core.string.ustring.String.sprintf)  string/ustring.cpp
- format  (Users-ks_128-Documents-godot-src-core.string.ustring.String.format)  string/ustring.cpp
- format_number  (Users-ks_128-Documents-godot-src-core.string.translation_server.TranslationServer.format_number)  string/translation_server.cpp
- _get_string  (Users-ks_128-Documents-godot-src-core.io.resource_format_binary.ResourceLoaderBinary._get_string)  io/resource_format_binary.cpp
- get_unicode_string  (Users-ks_128-Documents-godot-src-core.io.resource_format_binary.ResourceLoaderBinary.g
```


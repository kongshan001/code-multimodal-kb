# q01 · code_retrieval · arm: `kb+openspec`

- **题**：Godot 里字符串格式化的底层函数叫什么？
- **gold**：vformat
- **答对**：✓
- **答案**：`vformat`
- **指标**：tokens=6399 · llm_calls=6 · tool_steps=5 · 耗时=19.34s · 截断=否

---

**👤 用户**：Godot 里字符串格式化的底层函数叫什么？

> 💭 **思考**：用户问的是 Godot 里字符串格式化的底层函数叫什么。我需要在 Godot core/ 代码库中搜索相关的字符串格式化函数。

让我搜索一下。

**🔧 `cmm_search`**({"query": "字符串格式化 格式化 string format"})

**🔧 `cmm_search`**({"query": "vformat sprintf format"})

> 💭 **思考**：从搜索结果看，Godot 里有几个字符串格式化相关的函数：

1. `vformat` - 在 variant/variant.h 中定义
2. `sprintf` - 在 String 类中 (string/ustring.cpp)
3. `format` - 也在 String 类中 (string/ustring.cpp)

用户问的是"底层函数"，我需要看一下这些函数哪个是真正的底层实现。让我读取一下相关文件。

**🔧 `read_file`**({"path": "variant/variant.h"})

**🔧 `read_file`**({"path": "string/ustring.cpp"})

> 💭 **思考**：看起来直接读取文件失败了，可能路径不对。让我再搜索一下，看看哪个是真正的底层函数。

从搜索结果来看，有几个候选：
- `vformat` - 在 variant/variant.h 中
- `sprintf` - 在 String 类中
- `format` - 在 String 类中

`vformat` 看起来是底层的 C++ 函数，而 `sprintf` 和 `format` 是 String 类的方法。通常 `vformat`（variable arguments format）是更底层的实现。

让我再确认一下。

**🔧 `cmm_search`**({"query": "vformat implementation"})

> 💭 **思考**：看起来 vformat 是在 variant/variant.h 中定义的。这应该是 Godot 中字符串格式化的底层函数。

根据搜索结果，Godot 中字符串格式化的底层函数是 `vformat`，它位于 variant 模块中。String 类的 `format` 和 `sprintf` 方法可能都是基于这个底层函数实现的。

用户问的是"底层函数"，所以答案应该是 `vformat`。

**🤖 Agent**：`vformat`

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
- vformat  (Users-ks_128-Documents-godot-src-core.variant.variant.vformat)  variant/variant.h
- sprintf  (Users-ks_128-Documents-godot-src-core.string.ustring.String.sprintf)  string/ustring.cpp
- format  (Users-ks_128-Documents-godot-src-core.string.ustring.String.format)  string/ustring.cpp
- format  (Users-ks_128-Documents-godot-src-core.object.script_backtrace.ScriptBacktrace.format)  object/script_backtrace.cpp
- get_format  (Users-ks_128-Documents-godot-src-core.io.image.Image.get_format)  io/image.cpp
```

**📋 工具结果**：
```
(read error: [Errno 2] No such file or directory: 'variant/variant.h')
```

**📋 工具结果**：
```
(read error: [Errno 2] No such file or directory: 'string/ustring.cpp')
```

**📋 工具结果**：
```
- vformat  (Users-ks_128-Documents-godot-src-core.variant.variant.vformat)  variant/variant.h
```


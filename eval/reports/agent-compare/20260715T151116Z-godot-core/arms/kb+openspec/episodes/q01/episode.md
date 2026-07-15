# q01 · code_retrieval · arm: `kb+openspec`

**题**：Godot 里字符串格式化的底层函数叫什么？  ·  **gold**：vformat
**答对**：✗  ·  **答案**：底层有两个核心函数（定义在 `core/string/ustring.cpp`）：

- **`String::sprintf`** — C 风格格式化（`%s`/`%d`/`%x` 等占位符）
- **`String::format`**
**指标**：tokens=2401 · llm_calls=2 · tool_steps=1 · 耗时=10.8s · 截断=否

---

**👤 用户**：Godot 里字符串格式化的底层函数叫什么？

> 💭 **思考**：The user is asking about the underlying function for string formatting in Godot. Let me search for it.

**🔧 `cmm_search`**({"query": "string format sprintf"})

> 💭 **思考**：The search results clearly show the relevant functions. Let me answer directly.

**🤖 Agent**：底层有两个核心函数（定义在 `core/string/ustring.cpp`）：

- **`String::sprintf`** — C 风格格式化（`%s`/`%d`/`%x` 等占位符）
- **`String::format`** — Godot 风格占位符替换（`{0}`/`{name}` 字典/数组方式）

GDScript 里的 `"text %d" % 42` 走的是 `sprintf`，`"text {0}".format(["val"])` 走的是 `format`。

**📋 工具结果**：
```
- sprintf  (Users-ks_128-Documents-godot-src-core.string.ustring.String.sprintf)  string/ustring.cpp
- format  (Users-ks_128-Documents-godot-src-core.string.ustring.String.format)  string/ustring.cpp
- format_number  (Users-ks_128-Documents-godot-src-core.string.translation_server.TranslationServer.format_number)  string/translation_server.cpp
- _get_string  (Users-ks_128-Documents-godot-src-core.io.resource_format_binary.ResourceLoaderBinary._get_string)  io/resource_format_binary.cpp
- get_unicode_string  (Users-ks_128-Documents-godot-src-core.io.resource_format_binary.ResourceLoaderBinary.g
```


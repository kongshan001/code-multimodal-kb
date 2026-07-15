# q11 · code_retrieval · arm: `kb+superpowers`

**题**：JSON 解析用哪个类？  ·  **gold**：JSON
**答对**：✓  ·  **答案**：`JSON`（定义在 `core/io/json.cpp`）。核心方法：

- **`JSON::parse`** — 解析 JSON 字符串
- **`JSON::stringify`** — 序列化为 JSON 字符串
**指标**：tokens=1040 · llm_calls=2 · tool_steps=1 · 耗时=12.35s · 截断=否

---

**👤 用户**：JSON 解析用哪个类？

> 💭 **思考**：The user is asking which class is used for JSON parsing in Godot's core/.

**🔧 `cmm_search`**({"query": "JSON parsing class"})

> 💭 **思考**：The answer is the `JSON` class.

**🤖 Agent**：`JSON`（定义在 `core/io/json.cpp`）。核心方法：

- **`JSON::parse`** — 解析 JSON 字符串
- **`JSON::stringify`** — 序列化为 JSON 字符串

**📋 工具结果**：
```
- _stringify  (Users-ks_128-Documents-godot-src-core.io.json.JSON._stringify)  io/json.cpp
- parse  (Users-ks_128-Documents-godot-src-core.io.json.JSON.parse)  io/json.cpp
- stringify  (Users-ks_128-Documents-godot-src-core.io.json.JSON.stringify)  io/json.cpp
- _add_indent  (Users-ks_128-Documents-godot-src-core.io.json.JSON._add_indent)  io/json.cpp
- _get_token  (Users-ks_128-Documents-godot-src-core.io.json.JSON._get_token)  io/json.cpp
```


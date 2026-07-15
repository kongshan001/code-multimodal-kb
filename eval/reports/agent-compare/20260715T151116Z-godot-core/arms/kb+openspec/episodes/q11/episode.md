# q11 · code_retrieval · arm: `kb+openspec`

**题**：JSON 解析用哪个类？  ·  **gold**：JSON
**答对**：✓  ·  **答案**：JSON 解析用 `JSON` 类（`core/io/json.cpp`），核心方法：

- **`JSON::parse`** — 解析 JSON 字符串
- **`JSON::stringify`** — 序列化为 JSON 字符串
-
**指标**：tokens=1345 · llm_calls=2 · tool_steps=1 · 耗时=16.07s · 截断=否

---

**👤 用户**：JSON 解析用哪个类？

> 💭 **思考**：The user is asking which class is used for JSON parsing in Godot core/. Let me search for it.

**🔧 `cmm_search`**({"query": "JSON parsing class"})

**🤖 Agent**：JSON 解析用 `JSON` 类（`core/io/json.cpp`），核心方法：

- **`JSON::parse`** — 解析 JSON 字符串
- **`JSON::stringify`** — 序列化为 JSON 字符串
- 内部辅助：`_get_token`（词法分析）、`_stringify`

**📋 工具结果**：
```
- _stringify  (Users-ks_128-Documents-godot-src-core.io.json.JSON._stringify)  io/json.cpp
- parse  (Users-ks_128-Documents-godot-src-core.io.json.JSON.parse)  io/json.cpp
- stringify  (Users-ks_128-Documents-godot-src-core.io.json.JSON.stringify)  io/json.cpp
- _add_indent  (Users-ks_128-Documents-godot-src-core.io.json.JSON._add_indent)  io/json.cpp
- _get_token  (Users-ks_128-Documents-godot-src-core.io.json.JSON._get_token)  io/json.cpp
```


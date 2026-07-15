# q11 · code_retrieval · arm: `kb`

**题**：JSON 解析用哪个类？  ·  **gold**：JSON
**答对**：✓  ·  **答案**：JSON 解析使用 **`JSON`** 类（`core/io/json.cpp`），主要方法：

- `JSON::parse` — 解析 JSON 字符串
- `JSON::stringify` — 将数据序列化为 JSON 字符串
**指标**：tokens=919 · llm_calls=2 · tool_steps=1 · 耗时=7.85s · 截断=否

---

**👤 用户**：JSON 解析用哪个类？

**🔧 `cmm_search`**({"query": "JSON parsing class"})

**📋 工具结果**：
```
- _stringify  (Users-ks_128-Documents-godot-src-core.io.json.JSON._stringify)  io/json.cpp
- parse  (Users-ks_128-Documents-godot-src-core.io.json.JSON.parse)  io/json.cpp
- stringify  (Users-ks_128-Documents-godot-src-core.io.json.JSON.stringify)  io/json.cpp
- _add_indent  (Users-ks_128-Documents-godot-src-core.io.json.JSON._add_indent)  io/json.cpp
- _get_token  (Users-ks_128-Documents-godot-src-core.io.json.JSON._get_token)  io/json.cpp
```

**🤖 Agent**：JSON 解析使用 **`JSON`** 类（`core/io/json.cpp`），主要方法：

- `JSON::parse` — 解析 JSON 字符串
- `JSON::stringify` — 将数据序列化为 JSON 字符串


# q11 · code_retrieval · arm: `kb+openspec`

**题**：JSON 解析用哪个类？  ·  **gold**：JSON
**答对**：✓  ·  **答案**：用 `JSON` 类（`core/io/json.cpp`），主要方法：

- `JSON.parse(str)` — 解析字符串，返回结果
- `JSON.stringify(variant)` — 序列化为 JSON 字符串
**指标**：tokens=1301 · llm_calls=2 · tool_steps=1 · 耗时=13.55s · 截断=否

---

**👤 用户**：JSON 解析用哪个类？

> 💭 **思考**：The user is asking which class is used for JSON parsing in Godot.

**🔧 `cmm_search`**({"query": "JSON parsing"})

**🤖 Agent**：用 `JSON` 类（`core/io/json.cpp`），主要方法：

- `JSON.parse(str)` — 解析字符串，返回结果
- `JSON.stringify(variant)` — 序列化为 JSON 字符串

**📋 工具结果**：
```
- _stringify  (Users-ks_128-Documents-godot-src-core.io.json.JSON._stringify)  io/json.cpp
- parse  (Users-ks_128-Documents-godot-src-core.io.json.JSON.parse)  io/json.cpp
- stringify  (Users-ks_128-Documents-godot-src-core.io.json.JSON.stringify)  io/json.cpp
- _add_indent  (Users-ks_128-Documents-godot-src-core.io.json.JSON._add_indent)  io/json.cpp
- _get_token  (Users-ks_128-Documents-godot-src-core.io.json.JSON._get_token)  io/json.cpp
```


# q11 · code_retrieval · arm: `kb`

**题**：JSON 解析用哪个类？  ·  **gold**：JSON
**答对**：✓  ·  **答案**：`JSON` 类（`core/io/json.cpp`）。核心方法是 `JSON::parse()`，内部由 `_parse_value`、`_parse_array`、`_parse_object`、`_parse_string` 等私有
**指标**：tokens=1007 · llm_calls=2 · tool_steps=1 · 耗时=16.54s · 截断=否

---

**👤 用户**：JSON 解析用哪个类？

> 💭 **思考**：用户问 JSON 解析用哪个类。让我搜索一下。

**🔧 `cmm_search`**({"query": "JSON parse class"})

**🤖 Agent**：`JSON` 类（`core/io/json.cpp`）。核心方法是 `JSON::parse()`，内部由 `_parse_value`、`_parse_array`、`_parse_object`、`_parse_string` 等私有方法支撑。

**📋 工具结果**：
```
- parse  (Users-ks_128-Documents-godot-src-core.io.json.JSON.parse)  io/json.cpp
- _parse_value  (Users-ks_128-Documents-godot-src-core.io.json.JSON._parse_value)  io/json.cpp
- _parse_array  (Users-ks_128-Documents-godot-src-core.io.json.JSON._parse_array)  io/json.cpp
- _parse_object  (Users-ks_128-Documents-godot-src-core.io.json.JSON._parse_object)  io/json.cpp
- _parse_string  (Users-ks_128-Documents-godot-src-core.io.json.JSON._parse_string)  io/json.cpp
```


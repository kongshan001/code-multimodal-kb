# q11 · code_retrieval · arm: `kb+superpowers`

**题**：JSON 解析用哪个类？  ·  **gold**：JSON
**答对**：✓  ·  **答案**：`JSON` 类（核心方法：`JSON::parse`，定义在 `core/io/json.cpp`）。
**指标**：tokens=339 · llm_calls=2 · tool_steps=1 · 耗时=13.96s · 截断=否

---

**👤 用户**：JSON 解析用哪个类？

> 💭 **思考**：用户问的是 Godot 中 JSON 解析用哪个类。这个问题很直接，答案是 `JSON` 类。让我用工具确认一下。

**🔧 `cmm_search`**({"query": "JSON parse class"})

> 💭 **思考**：答案很明确，就是 `JSON` 类。

**🤖 Agent**：`JSON` 类（核心方法：`JSON::parse`，定义在 `core/io/json.cpp`）。

**📋 工具结果**：
```
- parse  (Users-ks_128-Documents-godot-src-core.io.json.JSON.parse)  io/json.cpp
- _parse_value  (Users-ks_128-Documents-godot-src-core.io.json.JSON._parse_value)  io/json.cpp
- _parse_array  (Users-ks_128-Documents-godot-src-core.io.json.JSON._parse_array)  io/json.cpp
- _parse_object  (Users-ks_128-Documents-godot-src-core.io.json.JSON._parse_object)  io/json.cpp
- _parse_string  (Users-ks_128-Documents-godot-src-core.io.json.JSON._parse_string)  io/json.cpp
```


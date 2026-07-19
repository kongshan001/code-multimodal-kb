# q11 · code_retrieval · arm: `kb+openspec`

- **题**：JSON 解析用哪个类？
- **gold**：JSON
- **答对**：✓
- **答案**：`JSON`
- **指标**：tokens=2531 · llm_calls=2 · tool_steps=1 · 耗时=7.66s · 截断=否

---

**👤 用户**：JSON 解析用哪个类？

> 💭 **思考**：用户问"JSON 解析用哪个类？"，这是一个关于 Godot 代码库的问题。我需要使用 cmm_search 工具来查找 JSON 解析相关的类。

根据工具说明，我应该使用 mcp__bench__cmm_search 来搜索 JSON 解析相关的符号。

让我搜索 "JSON parse" 或 "JSON" 相关的内容。

**🔧 `cmm_search`**({"query": "JSON parse"})

> 💭 **思考**：搜索结果显示 JSON 解析使用的是 `JSON` 类，位于 `io/json.cpp` 中。搜索结果还显示了相关的解析方法：
- parse
- _parse_value
- _parse_array
- _parse_object
- _parse_string

用户问的是"JSON 解析用哪个类？"，答案应该是 `JSON` 类。

根据指令，我应该直接给出符号名，不需要长篇解释。

**🤖 Agent**：`JSON`

**📋 工具结果**：
```
- parse  (Users-ks_128-Documents-godot-src-core.io.json.JSON.parse)  io/json.cpp
- _parse_value  (Users-ks_128-Documents-godot-src-core.io.json.JSON._parse_value)  io/json.cpp
- _parse_array  (Users-ks_128-Documents-godot-src-core.io.json.JSON._parse_array)  io/json.cpp
- _parse_object  (Users-ks_128-Documents-godot-src-core.io.json.JSON._parse_object)  io/json.cpp
- _parse_string  (Users-ks_128-Documents-godot-src-core.io.json.JSON._parse_string)  io/json.cpp
```


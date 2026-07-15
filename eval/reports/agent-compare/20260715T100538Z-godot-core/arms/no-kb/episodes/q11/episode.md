# q11 · code_retrieval · arm: `no-kb`

**题**：JSON 解析用哪个类？  ·  **gold**：JSON
**答对**：✓  ·  **答案**：`JSON`（定义在 `core/io/json.h`）。

用法示例：
```cpp
JSON json;
Error err = json.parse(json_string);
if (err == OK) {
    Variant
**指标**：tokens=905 · llm_calls=2 · tool_steps=1 · 耗时=13.39s · 截断=否

---

**👤 用户**：JSON 解析用哪个类？

> 💭 **思考**：用户问 JSON 解析用哪个类。让我在 Godot core/ 源码里搜索一下。

**🔧 `grep_code`**({"pattern": "class JSON"})

> 💭 **思考**：找到了。JSON 解析用的是 `JSON` 类，定义在 `core/io/json.h`。

**🤖 Agent**：`JSON`（定义在 `core/io/json.h`）。

用法示例：
```cpp
JSON json;
Error err = json.parse(json_string);
if (err == OK) {
    Variant result = json.get_data();
}
```

**📋 工具结果**：
```
matched 1 files:
/Users/ks_128/Documents/godot-src/core/io/json.h
```


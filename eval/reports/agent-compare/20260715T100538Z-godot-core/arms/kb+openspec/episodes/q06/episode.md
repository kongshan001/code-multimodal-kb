# q06 · code_retrieval · arm: `kb+openspec`

**题**：表示颜色的类叫什么？  ·  **gold**：Color
**答对**：✓  ·  **答案**：`Color`（定义于 `core/math/color.h`）。
**指标**：tokens=1296 · llm_calls=2 · tool_steps=1 · 耗时=13.99s · 截断=否

---

**👤 用户**：表示颜色的类叫什么？

> 💭 **思考**：The user is asking what the class for representing colors is called. Let me search for it.

**🔧 `cmm_search`**({"query": "color representation class"})

> 💭 **思考**：The answer is clear: the class is `Color`.

**🤖 Agent**：`Color`（定义于 `core/math/color.h`）。

**📋 工具结果**：
```
- Color  (Users-ks_128-Documents-godot-src-core.math.color.Color.Color)  math/color.h
- find_named_color  (Users-ks_128-Documents-godot-src-core.math.color.Color.find_named_color)  math/color.cpp
- get_named_color  (Users-ks_128-Documents-godot-src-core.math.color.Color.get_named_color)  math/color.cpp
- get_named_color_count  (Users-ks_128-Documents-godot-src-core.math.color.Color.get_named_color_count)  math/color.cpp
- get_named_color_name  (Users-ks_128-Documents-godot-src-core.math.color.Color.get_named_color_name)  math/color.cpp
```


# q22 · code_retrieval · arm: `kb+openspec`

**题**：字符串名（优化版字符串）用哪个类？  ·  **gold**：StringName
**答对**：✓  ·  **答案**：用 **`StringName`**（定义在 `core/string/string_name.h`）。它是 Godot 的优化版字符串，内部做全局唯一化（interning），适合用作键名、信号名、属性名等高频比较的场景。
**指标**：tokens=1380 · llm_calls=2 · tool_steps=1 · 耗时=18.08s · 截断=否

---

**👤 用户**：字符串名（优化版字符串）用哪个类？

> 💭 **思考**：用户问的是 Godot 中字符串名（优化版字符串）用哪个类。这应该是指 `StringName` 类。让我用工具确认一下。

**🔧 `cmm_search`**({"query": "StringName optimized string class"})

**🤖 Agent**：用 **`StringName`**（定义在 `core/string/string_name.h`）。它是 Godot 的优化版字符串，内部做全局唯一化（interning），适合用作键名、信号名、属性名等高频比较的场景。

**📋 工具结果**：
```
- StringName  (Users-ks_128-Documents-godot-src-core.string.string_name.StringName.StringName)  string/string_name.h
- ~StringName  (Users-ks_128-Documents-godot-src-core.string.string_name.StringName.~StringName)  string/string_name.h
- generate  (Users-ks_128-Documents-godot-src-core.string.optimized_translation.OptimizedTranslation.generate)  string/optimized_translation.cpp
- _set  (Users-ks_128-Documents-godot-src-core.string.optimized_translation.OptimizedTranslation._set)  string/optimized_translation.cpp
- _get  (Users-ks_128-Documents-godot-src-core.string.optimized_translation.Optimi
```


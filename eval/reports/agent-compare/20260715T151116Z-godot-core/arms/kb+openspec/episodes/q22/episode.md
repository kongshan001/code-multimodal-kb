# q22 · code_retrieval · arm: `kb+openspec`

**题**：字符串名（优化版字符串）用哪个类？  ·  **gold**：StringName
**答对**：✓  ·  **答案**：`StringName`（定义在 `core/string/string_name.h`）。它是 Godot 的驻留/优化版字符串类，所有相同内容的字符串共享一个唯一指针，适合做高频比较和查找的键值（如节点名、属性名、信号名等）。
**指标**：tokens=1390 · llm_calls=2 · tool_steps=1 · 耗时=17.09s · 截断=否

---

**👤 用户**：字符串名（优化版字符串）用哪个类？

> 💭 **思考**：用户问的是 Godot 中字符串名（优化版字符串）用哪个类。这应该是 `StringName` 类。让我确认一下。

**🔧 `cmm_search`**({"query": "StringName optimized interned string"})

> 💭 **思考**：The answer is `StringName`.

**🤖 Agent**：`StringName`（定义在 `core/string/string_name.h`）。它是 Godot 的驻留/优化版字符串类，所有相同内容的字符串共享一个唯一指针，适合做高频比较和查找的键值（如节点名、属性名、信号名等）。

**📋 工具结果**：
```
- StringName  (Users-ks_128-Documents-godot-src-core.string.string_name.StringName.StringName)  string/string_name.h
- ~StringName  (Users-ks_128-Documents-godot-src-core.string.string_name.StringName.~StringName)  string/string_name.h
- generate  (Users-ks_128-Documents-godot-src-core.string.optimized_translation.OptimizedTranslation.generate)  string/optimized_translation.cpp
- _set  (Users-ks_128-Documents-godot-src-core.string.optimized_translation.OptimizedTranslation._set)  string/optimized_translation.cpp
- _get  (Users-ks_128-Documents-godot-src-core.string.optimized_translation.Optimi
```


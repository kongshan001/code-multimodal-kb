# q22 · code_retrieval · arm: `kb+superpowers`

**题**：字符串名（优化版字符串）用哪个类？  ·  **gold**：StringName
**答对**：✓  ·  **答案**：`StringName`

定义在 `core/string/string_name.h`，是一种内部驻留（interned）的优化字符串，适合做键名/标识符（如节点名、属性名、信号名），比较时只比指针而非逐字符，代价是创建时有一次哈希查表
**指标**：tokens=432 · llm_calls=2 · tool_steps=1 · 耗时=14.53s · 截断=否

---

**👤 用户**：字符串名（优化版字符串）用哪个类？

> 💭 **思考**：用户问的是 Godot 中优化版字符串（字符串名）用哪个类。这个问题很直接——Godot 中优化的字符串就是 `StringName`。让我搜索确认一下。

**🔧 `cmm_search`**({"query": "optimized string name interned string"})

> 💭 **思考**：确认了，就是 `StringName`。

**🤖 Agent**：`StringName`

定义在 `core/string/string_name.h`，是一种内部驻留（interned）的优化字符串，适合做键名/标识符（如节点名、属性名、信号名），比较时只比指针而非逐字符，代价是创建时有一次哈希查表开销。

**📋 工具结果**：
```
- generate  (Users-ks_128-Documents-godot-src-core.string.optimized_translation.OptimizedTranslation.generate)  string/optimized_translation.cpp
- _set  (Users-ks_128-Documents-godot-src-core.string.optimized_translation.OptimizedTranslation._set)  string/optimized_translation.cpp
- _get  (Users-ks_128-Documents-godot-src-core.string.optimized_translation.OptimizedTranslation._get)  string/optimized_translation.cpp
- hash  (Users-ks_128-Documents-godot-src-core.string.optimized_translation.OptimizedTranslation.hash)  string/optimized_translation.h
- StringName  (Users-ks_128-Documents-godot-sr
```


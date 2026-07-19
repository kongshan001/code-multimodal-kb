# q22 · code_retrieval · arm: `kb+superpowers`

- **题**：字符串名（优化版字符串）用哪个类？
- **gold**：StringName
- **答对**：✓
- **答案**：`StringName`
- **指标**：tokens=2643 · llm_calls=2 · tool_steps=1 · 耗时=8.71s · 截断=否

---

**👤 用户**：字符串名（优化版字符串）用哪个类？

> 💭 **思考**：用户在问"字符串名（优化版字符串）用哪个类？"，这应该是在问 Godot 代码库中用于表示字符串名称（优化版字符串）的类。

在 Godot 中，通常有一个 `StringName` 类用于优化字符串存储，它是一个哈希化的字符串标识符。

让我搜索一下 Godot core/ 中的相关代码。

**🔧 `cmm_search`**({"query": "StringName"})

> 💭 **思考**：很好，搜索结果直接找到了 `StringName` 类。这是 Godot 中用于优化字符串存储的类，它通过哈希化字符串来提供高效的比较和查找。

根据系统提示，我需要直接用符号名作答，不需要长解释。

**🤖 Agent**：`StringName`

**📋 工具结果**：
```
- StringName  (Users-ks_128-Documents-godot-src-core.string.string_name.StringName.StringName)  string/string_name.h
- ~StringName  (Users-ks_128-Documents-godot-src-core.string.string_name.StringName.~StringName)  string/string_name.h
- operator StringName() const  (Users-ks_128-Documents-godot-src-core.variant.variant.Variant.operator StringName() const)  variant/variant.cpp
- operator Vector<StringName>() const  (Users-ks_128-Documents-godot-src-core.variant.variant.Variant.operator Vector<StringName>() const)  variant/variant.cpp
- setup  (Users-ks_128-Documents-godot-src-core.string.strin
```


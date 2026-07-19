# q22 · code_retrieval · arm: `kb`

- **题**：字符串名（优化版字符串）用哪个类？
- **gold**：StringName
- **答对**：✓
- **答案**：`StringName`
- **指标**：tokens=1963 · llm_calls=2 · tool_steps=1 · 耗时=12.81s · 截断=否

---

**👤 用户**：字符串名（优化版字符串）用哪个类？

> 💭 **思考**：用户问"字符串名（优化版字符串）用哪个类？"

这是在问 Godot 代码库中的字符串相关类。用户说的"优化版字符串"可能是指 Godot 的字符串类。

让我搜索一下 Godot core/ 中的字符串类。

**🔧 `cmm_search`**({"query": "优化版字符串 StringName"})

> 💭 **思考**：搜索结果找到了 `StringName` 类。在 Godot 中，`StringName` 是优化版的字符串类，用于频繁比较的字符串标识符。它使用字符串哈希化来优化比较性能。

根据用户的描述"字符串名（优化版字符串）"，这正是 `StringName` 类的用途。

我应该直接回答这个符号名称。

**🤖 Agent**：`StringName`

**📋 工具结果**：
```
- StringName  (Users-ks_128-Documents-godot-src-core.string.string_name.StringName.StringName)  string/string_name.h
- ~StringName  (Users-ks_128-Documents-godot-src-core.string.string_name.StringName.~StringName)  string/string_name.h
- operator StringName() const  (Users-ks_128-Documents-godot-src-core.variant.variant.Variant.operator StringName() const)  variant/variant.cpp
- operator Vector<StringName>() const  (Users-ks_128-Documents-godot-src-core.variant.variant.Variant.operator Vector<StringName>() const)  variant/variant.cpp
- setup  (Users-ks_128-Documents-godot-src-core.string.strin
```


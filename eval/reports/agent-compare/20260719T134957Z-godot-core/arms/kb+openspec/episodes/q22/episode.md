# q22 · code_retrieval · arm: `kb+openspec`

- **题**：字符串名（优化版字符串）用哪个类？
- **gold**：StringName
- **答对**：✓
- **答案**：StringName
- **指标**：tokens=2658 · llm_calls=2 · tool_steps=1 · 耗时=9.46s · 截断=否

---

**👤 用户**：字符串名（优化版字符串）用哪个类？

> 💭 **思考**：用户在问"字符串名（优化版字符串）用哪个类？"

这是在问 Godot 代码库中的类。听起来是在问某种优化过的字符串类。在 Godot 中，有几个字符串相关的类：
- String
- StringName
- CharString
- Char16String

"字符串名"很可能指的是 StringName 类，它是 Godot 中用于优化的字符串标识符类型。StringName 是对字符串的优化版本，使用哈希表来避免重复分配相同的字符串。

让我用代码搜索工具来确认一下。

**🔧 `cmm_search`**({"query": "StringName"})

> 💭 **思考**：搜索结果确认了 StringName 类确实存在。从名称和描述来看，StringName 是 Godot 中的字符串名/优化版字符串类。

根据我的知识，StringName 是 Godot 中用于唯一标识符的优化字符串类型，它使用全局字符串池来避免重复分配相同的字符串，提高性能。

用户问"字符串名（优化版字符串）用哪个类？"，答案应该是 StringName。

按照指示，我应该直接给符号名作答，不要长解释。

**🤖 Agent**：StringName

**📋 工具结果**：
```
- StringName  (Users-ks_128-Documents-godot-src-core.string.string_name.StringName.StringName)  string/string_name.h
- ~StringName  (Users-ks_128-Documents-godot-src-core.string.string_name.StringName.~StringName)  string/string_name.h
- operator StringName() const  (Users-ks_128-Documents-godot-src-core.variant.variant.Variant.operator StringName() const)  variant/variant.cpp
- operator Vector<StringName>() const  (Users-ks_128-Documents-godot-src-core.variant.variant.Variant.operator Vector<StringName>() const)  variant/variant.cpp
- setup  (Users-ks_128-Documents-godot-src-core.string.strin
```


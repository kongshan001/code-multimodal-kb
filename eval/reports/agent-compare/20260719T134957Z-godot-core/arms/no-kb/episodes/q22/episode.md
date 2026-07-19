# q22 · code_retrieval · arm: `no-kb`

- **题**：字符串名（优化版字符串）用哪个类？
- **gold**：StringName
- **答对**：✓
- **答案**：`StringName`
- **指标**：tokens=1857 · llm_calls=2 · tool_steps=1 · 耗时=7.63s · 截断=否

---

**👤 用户**：字符串名（优化版字符串）用哪个类？

> 💭 **思考**：用户问"字符串名（优化版字符串）用哪个类？"这是在问 Godot 引擎中用于字符串名的优化版本的类。

在 Godot 中，有一个 `StringName` 类，它是优化版的字符串，用于频繁使用的字符串标识符（如节点名称、信号名称等）。StringName 使用哈希表和指针比较来优化性能，避免重复的字符串分配和比较。

让我搜索一下来确认这个类名。

**🔧 `grep_code`**({"pattern": "class StringName"})

> 💭 **思考**：搜索结果显示了几个包含 "class StringName" 的文件。让我确认 StringName 类的定义位置。

**🤖 Agent**：`StringName`

**📋 工具结果**：
```
matched 3 files:
/Users/ks_128/Documents/godot-src/core/variant/dictionary.h
/Users/ks_128/Documents/godot-src/core/variant/array.h
/Users/ks_128/Documents/godot-src/core/templates/a_hash_map.h
```


# q14 · code_retrieval · arm: `no-kb`

**题**：保存资源用哪个类？  ·  **gold**：ResourceSaver
**答对**：✓  ·  **答案**：`ResourceSaver`
**指标**：tokens=1031 · llm_calls=3 · tool_steps=2 · 耗时=19.61s · 截断=否

---

**👤 用户**：保存资源用哪个类？

> 💭 **思考**：用户问保存资源用哪个类。让我搜索一下。

**🔧 `grep_code`**({"pattern": "save_resource"})

> 💭 **思考**：Let me try a different search pattern.

**🔧 `grep_code`**({"pattern": "ResourceSaver"})

**🤖 Agent**：`ResourceSaver`

**📋 工具结果**：
```
(no matches)
```

**📋 工具结果**：
```
matched 7 files:
/Users/ks_128/Documents/godot-src/core/extension/gdextension_special_compat_hashes.cpp
/Users/ks_128/Documents/godot-src/core/io/resource_saver.h
/Users/ks_128/Documents/godot-src/core/io/resource_saver.cpp
/Users/ks_128/Documents/godot-src/core/io/resource_format_binary.cpp
/Users/ks_128/Documents/godot-src/core/core_bind.cpp
/Users/ks_128/Documents/godot-src/core/core_bind.h
/Users/ks_128/Documents/godot-src/core/register_core_types.cpp
```


# q14 · code_retrieval · arm: `kb+superpowers`

- **题**：保存资源用哪个类？
- **gold**：ResourceSaver
- **答对**：✓
- **答案**：`ResourceSaver`
- **指标**：tokens=2649 · llm_calls=2 · tool_steps=1 · 耗时=8.32s · 截断=否

---

**👤 用户**：保存资源用哪个类？

> 💭 **思考**：用户问的是"保存资源用哪个类？"，这是在问 Godot 引擎中保存资源使用的类。

让我思考一下在 Godot 中保存资源相关的类：
- `ResourceSaver` - 这是保存资源的主要类
- `ResourceLoader` - 这是加载资源的类

用户问的是"保存资源"，所以应该是 `ResourceSaver`。

让我先用搜索工具确认一下。

**🔧 `cmm_search`**({"query": "ResourceSaver save resource"})

> 💭 **思考**：好的，搜索结果清楚地显示是 `ResourceSaver` 类，它有一个 `save` 方法用于保存资源。这正是用户问的答案。

根据我的指示，我应该直接给出符号名作答，不要长解释。

**🤖 Agent**：`ResourceSaver`

**📋 工具结果**：
```
- save  (Users-ks_128-Documents-godot-src-core.io.resource_saver.ResourceSaver.save)  io/resource_saver.cpp
- set_save_callback  (Users-ks_128-Documents-godot-src-core.io.resource_saver.ResourceSaver.set_save_callback)  io/resource_saver.cpp
- set_timestamp_on_save  (Users-ks_128-Documents-godot-src-core.io.resource_saver.ResourceSaver.set_timestamp_on_save)  io/resource_saver.h
- get_timestamp_on_save  (Users-ks_128-Documents-godot-src-core.io.resource_saver.ResourceSaver.get_timestamp_on_save)  io/resource_saver.h
- save  (Users-ks_128-Documents-godot-src-core.core_bind.ResourceSaver.save)  
```


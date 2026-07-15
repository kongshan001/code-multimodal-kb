# q13 · code_retrieval · arm: `kb+superpowers`

**题**：加载资源用哪个类？  ·  **gold**：ResourceLoader
**答对**：✓  ·  **答案**：`ResourceLoader`
**指标**：tokens=316 · llm_calls=2 · tool_steps=1 · 耗时=15.64s · 截断=否

---

**👤 用户**：加载资源用哪个类？

> 💭 **思考**：用户问的是加载资源用哪个类。让我搜索一下。

**🔧 `cmm_search`**({"query": "load resource"})

> 💭 **思考**：The user is asking about which class to use for loading resources. The answer is `ResourceLoader`.

**🤖 Agent**：`ResourceLoader`

**📋 工具结果**：
```
- load_gdextension_resource  (Users-ks_128-Documents-godot-src-core.extension.gdextension_resource_format.GDExtensionResourceLoader.load_gdextension_resource)  extension/gdextension_resource_format.cpp
- load  (Users-ks_128-Documents-godot-src-core.io.resource_importer.ResourceFormatImporter.load)  io/resource_importer.cpp
- load  (Users-ks_128-Documents-godot-src-core.io.resource_loader.ResourceFormatLoader.load)  io/resource_loader.cpp
- _load  (Users-ks_128-Documents-godot-src-core.io.resource_loader.ResourceLoader._load)  io/resource_loader.cpp
- load  (Users-ks_128-Documents-godot-src-cor
```


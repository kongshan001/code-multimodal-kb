# q13 · code_retrieval · arm: `kb+openspec`

- **题**：加载资源用哪个类？
- **gold**：ResourceLoader
- **答对**：✓
- **答案**：`ResourceLoader`
- **指标**：tokens=2456 · llm_calls=2 · tool_steps=1 · 耗时=8.43s · 截断=否

---

**👤 用户**：加载资源用哪个类？

> 💭 **思考**：用户问"加载资源用哪个类？"，这是在问 Godot 代码库中用于资源加载的类。

根据我的知识，在 Godot 中加载资源通常使用 `ResourceLoader` 类。让我先用语义搜索确认一下。

**🔧 `cmm_search`**({"query": "load resource"})

> 💭 **思考**：搜索结果显示有 `ResourceLoader` 类及其 `load` 方法。这正是用于加载资源的类。根据收敛纪律，我应该立刻用符号名作答。

**🤖 Agent**：`ResourceLoader`

**📋 工具结果**：
```
- load_gdextension_resource  (Users-ks_128-Documents-godot-src-core.extension.gdextension_resource_format.GDExtensionResourceLoader.load_gdextension_resource)  extension/gdextension_resource_format.cpp
- load  (Users-ks_128-Documents-godot-src-core.io.resource_importer.ResourceFormatImporter.load)  io/resource_importer.cpp
- load  (Users-ks_128-Documents-godot-src-core.io.resource_loader.ResourceFormatLoader.load)  io/resource_loader.cpp
- _load  (Users-ks_128-Documents-godot-src-core.io.resource_loader.ResourceLoader._load)  io/resource_loader.cpp
- load  (Users-ks_128-Documents-godot-src-cor
```


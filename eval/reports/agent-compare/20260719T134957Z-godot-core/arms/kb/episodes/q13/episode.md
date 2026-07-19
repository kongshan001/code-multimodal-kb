# q13 · code_retrieval · arm: `kb`

- **题**：加载资源用哪个类？
- **gold**：ResourceLoader
- **答对**：✓
- **答案**：`ResourceLoader`
- **指标**：tokens=1901 · llm_calls=2 · tool_steps=1 · 耗时=7.69s · 截断=否

---

**👤 用户**：加载资源用哪个类？

> 💭 **思考**：用户问"加载资源用哪个类？"，这是在问 Godot 代码库中负责资源加载的类。我需要在 Godot core/ 中搜索相关的符号。

常见的答案可能是 `ResourceLoader`，但我应该用搜索工具来确认。

**🔧 `cmm_search`**({"query": "load resource"})

> 💭 **思考**：搜索结果显示了 `ResourceLoader` 类，它有 `load` 方法。这正是用于加载资源的主要类。根据结果，我应该直接给出答案。

**🤖 Agent**：`ResourceLoader`

**📋 工具结果**：
```
- load_gdextension_resource  (Users-ks_128-Documents-godot-src-core.extension.gdextension_resource_format.GDExtensionResourceLoader.load_gdextension_resource)  extension/gdextension_resource_format.cpp
- load  (Users-ks_128-Documents-godot-src-core.io.resource_importer.ResourceFormatImporter.load)  io/resource_importer.cpp
- load  (Users-ks_128-Documents-godot-src-core.io.resource_loader.ResourceFormatLoader.load)  io/resource_loader.cpp
- _load  (Users-ks_128-Documents-godot-src-core.io.resource_loader.ResourceLoader._load)  io/resource_loader.cpp
- load  (Users-ks_128-Documents-godot-src-cor
```


# q13 · code_retrieval · arm: `kb`

**题**：加载资源用哪个类？  ·  **gold**：ResourceLoader
**答对**：✓  ·  **答案**：加载资源使用 **`ResourceLoader`** 类（核心静态方法 `ResourceLoader::load`）。底层由 `ResourceFormatLoader` 提供具体格式支持。
**指标**：tokens=605 · llm_calls=2 · tool_steps=1 · 耗时=11.7s · 截断=否

---

**👤 用户**：加载资源用哪个类？

**🔧 `cmm_search`**({"query": "load resource"})

**📋 工具结果**：
```
- load_gdextension_resource  (Users-ks_128-Documents-godot-src-core.extension.gdextension_resource_format.GDExtensionResourceLoader.load_gdextension_resource)  extension/gdextension_resource_format.cpp
- load  (Users-ks_128-Documents-godot-src-core.io.resource_importer.ResourceFormatImporter.load)  io/resource_importer.cpp
- load  (Users-ks_128-Documents-godot-src-core.io.resource_loader.ResourceFormatLoader.load)  io/resource_loader.cpp
- _load  (Users-ks_128-Documents-godot-src-core.io.resource_loader.ResourceLoader._load)  io/resource_loader.cpp
- load  (Users-ks_128-Documents-godot-src-cor
```

**🤖 Agent**：加载资源使用 **`ResourceLoader`** 类（核心静态方法 `ResourceLoader::load`）。底层由 `ResourceFormatLoader` 提供具体格式支持。


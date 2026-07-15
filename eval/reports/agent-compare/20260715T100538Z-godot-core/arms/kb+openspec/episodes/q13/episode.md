# q13 · code_retrieval · arm: `kb+openspec`

**题**：加载资源用哪个类？  ·  **gold**：ResourceLoader
**答对**：✓  ·  **答案**：加载资源用 `ResourceLoader`（类），通过其静态方法 `load()` 或内部 `_load()` 完成。各格式由 `ResourceFormatLoader` 子类实现具体加载逻辑。

核心路径：`io/resource_l
**指标**：tokens=1340 · llm_calls=2 · tool_steps=1 · 耗时=21.28s · 截断=否

---

**👤 用户**：加载资源用哪个类？

> 💭 **思考**：用户问"加载资源用哪个类？"，这是一个简单的问题，我可以用搜索工具快速查找。

**🔧 `cmm_search`**({"query": "load resource"})

**🤖 Agent**：加载资源用 `ResourceLoader`（类），通过其静态方法 `load()` 或内部 `_load()` 完成。各格式由 `ResourceFormatLoader` 子类实现具体加载逻辑。

核心路径：`io/resource_loader.cpp`

**📋 工具结果**：
```
- load_gdextension_resource  (Users-ks_128-Documents-godot-src-core.extension.gdextension_resource_format.GDExtensionResourceLoader.load_gdextension_resource)  extension/gdextension_resource_format.cpp
- load  (Users-ks_128-Documents-godot-src-core.io.resource_importer.ResourceFormatImporter.load)  io/resource_importer.cpp
- load  (Users-ks_128-Documents-godot-src-core.io.resource_loader.ResourceFormatLoader.load)  io/resource_loader.cpp
- _load  (Users-ks_128-Documents-godot-src-core.io.resource_loader.ResourceLoader._load)  io/resource_loader.cpp
- load  (Users-ks_128-Documents-godot-src-cor
```


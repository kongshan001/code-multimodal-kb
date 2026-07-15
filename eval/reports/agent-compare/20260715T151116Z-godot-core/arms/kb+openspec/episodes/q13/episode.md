# q13 · code_retrieval · arm: `kb+openspec`

**题**：加载资源用哪个类？  ·  **gold**：ResourceLoader
**答对**：✓  ·  **答案**：加载资源用 **`ResourceLoader`**（核心类，位于 `core/io/resource_loader.cpp`）。

主要 API：
- `ResourceLoader::load(path)` — 加载指定路径的资源
- 
**指标**：tokens=1377 · llm_calls=2 · tool_steps=1 · 耗时=15.43s · 截断=否

---

**👤 用户**：加载资源用哪个类？

> 💭 **思考**：用户问的是Godot中加载资源用哪个类。让我搜索一下。

**🔧 `cmm_search`**({"query": "load resource"})

**🤖 Agent**：加载资源用 **`ResourceLoader`**（核心类，位于 `core/io/resource_loader.cpp`）。

主要 API：
- `ResourceLoader::load(path)` — 加载指定路径的资源
- `ResourceLoader::_load()` — 内部加载逻辑
- `ResourceFormatLoader` — 资源格式加载器的抽象基类，具体格式（如 `ResourceFormatImporter`、`GDExtensionResourceLoader`）继承它实现 `load()`

**📋 工具结果**：
```
- load_gdextension_resource  (Users-ks_128-Documents-godot-src-core.extension.gdextension_resource_format.GDExtensionResourceLoader.load_gdextension_resource)  extension/gdextension_resource_format.cpp
- load  (Users-ks_128-Documents-godot-src-core.io.resource_importer.ResourceFormatImporter.load)  io/resource_importer.cpp
- load  (Users-ks_128-Documents-godot-src-core.io.resource_loader.ResourceFormatLoader.load)  io/resource_loader.cpp
- _load  (Users-ks_128-Documents-godot-src-core.io.resource_loader.ResourceLoader._load)  io/resource_loader.cpp
- load  (Users-ks_128-Documents-godot-src-cor
```


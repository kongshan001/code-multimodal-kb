# q14 · code_retrieval · arm: `kb+superpowers`

**题**：保存资源用哪个类？  ·  **gold**：ResourceSaver
**答对**：✓  ·  **答案**：`ResourceSaver`（core_bind 版 / 静态 API 版）。核心方法是 `ResourceSaver::save`，定义在 `core/io/resource_saver.h`。
**指标**：tokens=628 · llm_calls=3 · tool_steps=2 · 耗时=13.07s · 截断=否

---

**👤 用户**：保存资源用哪个类？

> 💭 **思考**：用户问保存资源用哪个类。让我搜索一下。

**🔧 `cmm_search`**({"query": "save resource to file"})

> 💭 **思考**：让我更具体地搜索资源保存。ResourceSaver 应该是答案。

**🔧 `cmm_search`**({"query": "ResourceSaver save resource"})

**🤖 Agent**：`ResourceSaver`（core_bind 版 / 静态 API 版）。核心方法是 `ResourceSaver::save`，定义在 `core/io/resource_saver.h`。

**📋 工具结果**：
```
- save_to_cache  (Users-ks_128-Documents-godot-src-core.io.resource_uid.ResourceUID.save_to_cache)  io/resource_uid.cpp
- save_png_to_buffer  (Users-ks_128-Documents-godot-src-core.io.image.Image.save_png_to_buffer)  io/image.cpp
- save_jpg_to_buffer  (Users-ks_128-Documents-godot-src-core.io.image.Image.save_jpg_to_buffer)  io/image.cpp
- save_exr_to_buffer  (Users-ks_128-Documents-godot-src-core.io.image.Image.save_exr_to_buffer)  io/image.cpp
- save_dds_to_buffer  (Users-ks_128-Documents-godot-src-core.io.image.Image.save_dds_to_buffer)  io/image.cpp
```

**📋 工具结果**：
```
- save  (Users-ks_128-Documents-godot-src-core.io.resource_saver.ResourceSaver.save)  io/resource_saver.cpp
- set_save_callback  (Users-ks_128-Documents-godot-src-core.io.resource_saver.ResourceSaver.set_save_callback)  io/resource_saver.cpp
- set_timestamp_on_save  (Users-ks_128-Documents-godot-src-core.io.resource_saver.ResourceSaver.set_timestamp_on_save)  io/resource_saver.h
- get_timestamp_on_save  (Users-ks_128-Documents-godot-src-core.io.resource_saver.ResourceSaver.get_timestamp_on_save)  io/resource_saver.h
- save  (Users-ks_128-Documents-godot-src-core.core_bind.ResourceSaver.save)  
```


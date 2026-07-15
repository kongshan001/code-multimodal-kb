# q14 · code_retrieval · arm: `kb+openspec`

**题**：保存资源用哪个类？  ·  **gold**：ResourceSaver
**答对**：✓  ·  **答案**：保存资源用 **`ResourceSaver`**（核心方法 `ResourceSaver.save`，定义在 `core/io/resource_saver.cpp`）。
**指标**：tokens=1648 · llm_calls=3 · tool_steps=2 · 耗时=20.89s · 截断=否

---

**👤 用户**：保存资源用哪个类？

> 💭 **思考**：用户问的是Godot中保存资源用哪个类。这是一个简单的问题，让我搜索一下。

**🔧 `cmm_search`**({"query": "save resource to file"})

> 💭 **思考**：搜索结果不太对，让我再搜一下 ResourceSaver 相关的。

**🔧 `cmm_search`**({"query": "ResourceSaver save resource to file"})

**🤖 Agent**：保存资源用 **`ResourceSaver`**（核心方法 `ResourceSaver.save`，定义在 `core/io/resource_saver.cpp`）。

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
- save_to_cache  (Users-ks_128-Documents-godot-src-core.io.resource_uid.ResourceUID.save_to_cache)  io/resource_uid.cpp
- set_save_callback  (Users-ks_128-Documents-godot-src-core.io.resource_saver.ResourceSaver.set_save_callback)  io/resource_saver.cpp
- set_timestamp_on_save  (Users-ks_128-Documents-godot-src-core.io.resource_saver.ResourceSaver.set_timestamp_on_save)  io/resource_saver.h
- get_timestamp_on_save  (Users-ks_128-Documents-godot-src-core.io.resource_saver.ResourceSaver.ge
```


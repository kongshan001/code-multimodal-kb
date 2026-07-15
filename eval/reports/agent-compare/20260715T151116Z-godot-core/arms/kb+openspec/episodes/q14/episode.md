# q14 · code_retrieval · arm: `kb+openspec`

**题**：保存资源用哪个类？  ·  **gold**：ResourceSaver
**答对**：✓  ·  **答案**：用 **`ResourceSaver`**，核心方法是 `ResourceSaver::save()`，定义在 `core/io/resource_saver.cpp` / `resource_saver.h`。
**指标**：tokens=1656 · llm_calls=3 · tool_steps=2 · 耗时=17.28s · 截断=否

---

**👤 用户**：保存资源用哪个类？

> 💭 **思考**：The user is asking which class is used to save resources in Godot. Let me search for this.

**🔧 `cmm_search`**({"query": "save resource to file"})

> 💭 **思考**：The search didn't directly return the main ResourceSaver class. Let me search more specifically.

**🔧 `cmm_search`**({"query": "ResourceSaver save resource"})

**🤖 Agent**：用 **`ResourceSaver`**，核心方法是 `ResourceSaver::save()`，定义在 `core/io/resource_saver.cpp` / `resource_saver.h`。

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


# q14 · code_retrieval · arm: `kb`

**题**：保存资源用哪个类？  ·  **gold**：ResourceSaver
**答对**：✓  ·  **答案**：保存资源使用 **`ResourceSaver`** 类（核心方法：`ResourceSaver::save`），定义在 `io/resource_saver.cpp` / `io/resource_saver.h`。
**指标**：tokens=1681 · llm_calls=3 · tool_steps=2 · 耗时=15.45s · 截断=否

---

**👤 用户**：保存资源用哪个类？

**🔧 `cmm_search`**({"query": "save resource to file"})

**📋 工具结果**：
```
- save_to_cache  (Users-ks_128-Documents-godot-src-core.io.resource_uid.ResourceUID.save_to_cache)  io/resource_uid.cpp
- save_png_to_buffer  (Users-ks_128-Documents-godot-src-core.io.image.Image.save_png_to_buffer)  io/image.cpp
- save_jpg_to_buffer  (Users-ks_128-Documents-godot-src-core.io.image.Image.save_jpg_to_buffer)  io/image.cpp
- save_exr_to_buffer  (Users-ks_128-Documents-godot-src-core.io.image.Image.save_exr_to_buffer)  io/image.cpp
- save_dds_to_buffer  (Users-ks_128-Documents-godot-src-core.io.image.Image.save_dds_to_buffer)  io/image.cpp
```

**🔧 `cmm_search`**({"query": "ResourceSaver save resource"})

**📋 工具结果**：
```
- save  (Users-ks_128-Documents-godot-src-core.io.resource_saver.ResourceSaver.save)  io/resource_saver.cpp
- set_save_callback  (Users-ks_128-Documents-godot-src-core.io.resource_saver.ResourceSaver.set_save_callback)  io/resource_saver.cpp
- set_timestamp_on_save  (Users-ks_128-Documents-godot-src-core.io.resource_saver.ResourceSaver.set_timestamp_on_save)  io/resource_saver.h
- get_timestamp_on_save  (Users-ks_128-Documents-godot-src-core.io.resource_saver.ResourceSaver.get_timestamp_on_save)  io/resource_saver.h
- save  (Users-ks_128-Documents-godot-src-core.core_bind.ResourceSaver.save)  
```

**🤖 Agent**：保存资源使用 **`ResourceSaver`** 类（核心方法：`ResourceSaver::save`），定义在 `io/resource_saver.cpp` / `io/resource_saver.h`。


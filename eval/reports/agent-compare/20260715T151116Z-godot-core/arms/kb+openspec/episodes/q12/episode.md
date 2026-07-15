# q12 · code_retrieval · arm: `kb+openspec`

**题**：图像数据用哪个类？  ·  **gold**：Image
**答对**：✓  ·  **答案**：图像数据用 **`Image`** 类（`core/io/image.h`）。
**指标**：tokens=1277 · llm_calls=2 · tool_steps=1 · 耗时=8.55s · 截断=否

---

**👤 用户**：图像数据用哪个类？

> 💭 **思考**：The user is asking which class is used for image data in Godot.

**🔧 `cmm_search`**({"query": "image data class"})

**🤖 Agent**：图像数据用 **`Image`** 类（`core/io/image.h`）。

**📋 工具结果**：
```
- get_image_data_size  (Users-ks_128-Documents-godot-src-core.io.image.Image.get_image_data_size)  io/image.cpp
- get_data  (Users-ks_128-Documents-godot-src-core.io.image.Image.get_data)  io/image.cpp
- set_data  (Users-ks_128-Documents-godot-src-core.io.image.Image.set_data)  io/image.cpp
- initialize_data  (Users-ks_128-Documents-godot-src-core.io.image.Image.initialize_data)  io/image.cpp
- _set_data  (Users-ks_128-Documents-godot-src-core.io.image.Image._set_data)  io/image.cpp
```


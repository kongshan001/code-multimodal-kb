# q12 · code_retrieval · arm: `kb+superpowers`

**题**：图像数据用哪个类？  ·  **gold**：Image
**答对**：✓  ·  **答案**：`Image`（core/io/image.h, image.cpp）。图像数据就存在 `Image` 类里。
**指标**：tokens=300 · llm_calls=2 · tool_steps=1 · 耗时=15.0s · 截断=否

---

**👤 用户**：图像数据用哪个类？

> 💭 **思考**：用户问的是 Godot 中图像数据用哪个类。让我搜索一下。

**🔧 `cmm_search`**({"query": "image data class"})

**🤖 Agent**：`Image`（core/io/image.h, image.cpp）。图像数据就存在 `Image` 类里。

**📋 工具结果**：
```
- get_image_data_size  (Users-ks_128-Documents-godot-src-core.io.image.Image.get_image_data_size)  io/image.cpp
- get_data  (Users-ks_128-Documents-godot-src-core.io.image.Image.get_data)  io/image.cpp
- set_data  (Users-ks_128-Documents-godot-src-core.io.image.Image.set_data)  io/image.cpp
- initialize_data  (Users-ks_128-Documents-godot-src-core.io.image.Image.initialize_data)  io/image.cpp
- _set_data  (Users-ks_128-Documents-godot-src-core.io.image.Image._set_data)  io/image.cpp
```


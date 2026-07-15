# q12 · code_retrieval · arm: `kb+openspec`

**题**：图像数据用哪个类？  ·  **gold**：Image
**答对**：✓  ·  **答案**：图像数据使用 `Image` 类（`core/io/image.cpp`）。相关方法包括 `Image::get_data()`、`Image::set_data()`、`Image::get_image_data_size()` 等。
**指标**：tokens=1470 · llm_calls=2 · tool_steps=1 · 耗时=14.22s · 截断=否

---

**👤 用户**：图像数据用哪个类？

**🔧 `cmm_search`**({"query": "image data class"})

**📋 工具结果**：
```
- get_image_data_size  (Users-ks_128-Documents-godot-src-core.io.image.Image.get_image_data_size)  io/image.cpp
- get_data  (Users-ks_128-Documents-godot-src-core.io.image.Image.get_data)  io/image.cpp
- set_data  (Users-ks_128-Documents-godot-src-core.io.image.Image.set_data)  io/image.cpp
- initialize_data  (Users-ks_128-Documents-godot-src-core.io.image.Image.initialize_data)  io/image.cpp
- _set_data  (Users-ks_128-Documents-godot-src-core.io.image.Image._set_data)  io/image.cpp
```

**🤖 Agent**：图像数据使用 `Image` 类（`core/io/image.cpp`）。相关方法包括 `Image::get_data()`、`Image::set_data()`、`Image::get_image_data_size()` 等。


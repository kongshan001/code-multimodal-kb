# q12 · code_retrieval · arm: `kb+superpowers`

**题**：图像数据用哪个类？  ·  **gold**：Image
**答对**：✓  ·  **答案**：图像数据用 **`Image`** 类（`core/io/image.cpp`）。常用方法如 `Image::get_data()`、`Image::set_data()`。
**指标**：tokens=1344 · llm_calls=2 · tool_steps=1 · 耗时=14.85s · 截断=否

---

**👤 用户**：图像数据用哪个类？

> 💭 **思考**：用户问图像数据用哪个类。让我搜索一下 Godot core 中关于图像数据的类。

**🔧 `cmm_search`**({"query": "image data class"})

**🤖 Agent**：图像数据用 **`Image`** 类（`core/io/image.cpp`）。常用方法如 `Image::get_data()`、`Image::set_data()`。

**📋 工具结果**：
```
- get_image_data_size  (Users-ks_128-Documents-godot-src-core.io.image.Image.get_image_data_size)  io/image.cpp
- get_data  (Users-ks_128-Documents-godot-src-core.io.image.Image.get_data)  io/image.cpp
- set_data  (Users-ks_128-Documents-godot-src-core.io.image.Image.set_data)  io/image.cpp
- initialize_data  (Users-ks_128-Documents-godot-src-core.io.image.Image.initialize_data)  io/image.cpp
- _set_data  (Users-ks_128-Documents-godot-src-core.io.image.Image._set_data)  io/image.cpp
```


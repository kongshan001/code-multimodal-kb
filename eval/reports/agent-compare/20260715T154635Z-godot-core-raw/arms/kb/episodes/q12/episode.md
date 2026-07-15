# q12 · code_retrieval · arm: `kb`

**题**：图像数据用哪个类？  ·  **gold**：Image
**答对**：✓  ·  **答案**：图像数据使用 `Image` 类（定义在 `core/io/image.cpp` / `image.h`）。
**指标**：tokens=904 · llm_calls=2 · tool_steps=1 · 耗时=6.85s · 截断=否

---

**👤 用户**：图像数据用哪个类？

**🔧 `cmm_search`**({"query": "image data pixel storage"})

**📋 工具结果**：
```
- get_pixel  (Users-ks_128-Documents-godot-src-core.io.image.Image.get_pixel)  io/image.cpp
- set_pixel  (Users-ks_128-Documents-godot-src-core.io.image.Image.set_pixel)  io/image.cpp
- get_format_pixel_size  (Users-ks_128-Documents-godot-src-core.io.image.Image.get_format_pixel_size)  io/image.cpp
- get_format_pixel_rshift  (Users-ks_128-Documents-godot-src-core.io.image.Image.get_format_pixel_rshift)  io/image.cpp
- get_format_min_pixel_size  (Users-ks_128-Documents-godot-src-core.io.image.Image.get_format_min_pixel_size)  io/image.cpp
```

**🤖 Agent**：图像数据使用 `Image` 类（定义在 `core/io/image.cpp` / `image.h`）。


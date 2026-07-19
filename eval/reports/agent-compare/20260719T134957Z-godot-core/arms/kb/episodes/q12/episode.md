# q12 · code_retrieval · arm: `kb`

- **题**：图像数据用哪个类？
- **gold**：Image
- **答对**：✓
- **答案**：`Image`
- **指标**：tokens=1931 · llm_calls=2 · tool_steps=1 · 耗时=8.7s · 截断=否

---

**👤 用户**：图像数据用哪个类？

> 💭 **思考**：用户在问"图像数据用哪个类？"，这是在问 Godot 代码库中用于表示图像数据的类。

我需要在 Godot core/ 代码库中搜索相关的类。最可能的答案是 `Image` 类，但我应该用搜索工具来确认。

让我搜索一下图像相关的类。

**🔧 `cmm_search`**({"query": "image data class"})

> 💭 **思考**：搜索结果显示 `Image` 类有多个与数据相关的方法，如 `get_image_data_size`、`get_data`、`set_data` 等。这确认了 `Image` 就是用于表示图像数据的类。

根据指示，我应该直接用符号名作答，不需要长解释。

**🤖 Agent**：`Image`

**📋 工具结果**：
```
- get_image_data_size  (Users-ks_128-Documents-godot-src-core.io.image.Image.get_image_data_size)  io/image.cpp
- get_data  (Users-ks_128-Documents-godot-src-core.io.image.Image.get_data)  io/image.cpp
- set_data  (Users-ks_128-Documents-godot-src-core.io.image.Image.set_data)  io/image.cpp
- initialize_data  (Users-ks_128-Documents-godot-src-core.io.image.Image.initialize_data)  io/image.cpp
- _set_data  (Users-ks_128-Documents-godot-src-core.io.image.Image._set_data)  io/image.cpp
```


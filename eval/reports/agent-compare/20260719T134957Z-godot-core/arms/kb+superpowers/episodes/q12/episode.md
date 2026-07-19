# q12 · code_retrieval · arm: `kb+superpowers`

- **题**：图像数据用哪个类？
- **gold**：Image
- **答对**：✓
- **答案**：`Image`
- **指标**：tokens=4252 · llm_calls=3 · tool_steps=2 · 耗时=10.65s · 截断=否

---

**👤 用户**：图像数据用哪个类？

> 💭 **思考**：用户问"图像数据用哪个类？"，这是在问 Godot 4.7 core/ 代码库中用于表示图像数据的类。

我需要使用语义搜索工具来查找相关的类。让我搜索一下与图像数据相关的类。

常见的图像数据类可能包括：
- Image
- ImageData
- Texture
- ImageTexture

让我先搜索一下。

**🔧 `cmm_search`**({"query": "图像数据 Image data"})

> 💭 **思考**：从搜索结果来看，似乎都是与 `Image` 类相关的方法。让我再搜索一下看看是否有专门的图像数据类，或者 `Image` 本身就是用来表示图像数据的类。

**🔧 `cmm_search`**({"query": "Image class"})

> 💭 **思考**：搜索结果显示 `Image` 类就是核心的图像数据类。用户问"图像数据用哪个类？"，答案应该是 `Image` 类。

根据指令，我需要简洁地回答，直接给出类名，不要长解释。查到即答。

**🤖 Agent**：`Image`

**📋 工具结果**：
```
- get_image_data_size  (Users-ks_128-Documents-godot-src-core.io.image.Image.get_image_data_size)  io/image.cpp
- get_data  (Users-ks_128-Documents-godot-src-core.io.image.Image.get_data)  io/image.cpp
- set_data  (Users-ks_128-Documents-godot-src-core.io.image.Image.set_data)  io/image.cpp
- initialize_data  (Users-ks_128-Documents-godot-src-core.io.image.Image.initialize_data)  io/image.cpp
- _set_data  (Users-ks_128-Documents-godot-src-core.io.image.Image._set_data)  io/image.cpp
```

**📋 工具结果**：
```
- Image  (Users-ks_128-Documents-godot-src-core.io.image.Image.Image)  io/image.cpp
- validate_3d_image  (Users-ks_128-Documents-godot-src-core.io.image.Image.validate_3d_image)  io/image.cpp
- compute_image_metrics  (Users-ks_128-Documents-godot-src-core.io.image.Image.compute_image_metrics)  io/image.cpp
- _get_dst_image_size  (Users-ks_128-Documents-godot-src-core.io.image.Image._get_dst_image_size)  io/image.cpp
- get_image_data_size  (Users-ks_128-Documents-godot-src-core.io.image.Image.get_image_data_size)  io/image.cpp
```


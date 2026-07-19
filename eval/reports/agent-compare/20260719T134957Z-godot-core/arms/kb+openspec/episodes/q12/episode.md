# q12 · code_retrieval · arm: `kb+openspec`

- **题**：图像数据用哪个类？
- **gold**：Image
- **答对**：✓
- **答案**：`Image`
- **指标**：tokens=2448 · llm_calls=2 · tool_steps=1 · 耗时=7.39s · 截断=否

---

**👤 用户**：图像数据用哪个类？

> 💭 **思考**：用户问"图像数据用哪个类？"，这是在询问Godot代码库中用于表示图像数据的类。我需要使用工具来查找相关的符号。

让我使用cmm_search来查找与图像数据相关的类。

**🔧 `cmm_search`**({"query": "图像数据 image data class"})

> 💭 **思考**：好的，搜索结果显示Image类有很多与图像数据相关的方法，如get_data、set_data等。看起来Image类就是用于图像数据的类。

根据系统指令，我需要简短回答，直接给出符号名，不要长解释。

**🤖 Agent**：`Image`

**📋 工具结果**：
```
- get_image_data_size  (Users-ks_128-Documents-godot-src-core.io.image.Image.get_image_data_size)  io/image.cpp
- get_data  (Users-ks_128-Documents-godot-src-core.io.image.Image.get_data)  io/image.cpp
- set_data  (Users-ks_128-Documents-godot-src-core.io.image.Image.set_data)  io/image.cpp
- initialize_data  (Users-ks_128-Documents-godot-src-core.io.image.Image.initialize_data)  io/image.cpp
- _set_data  (Users-ks_128-Documents-godot-src-core.io.image.Image._set_data)  io/image.cpp
```


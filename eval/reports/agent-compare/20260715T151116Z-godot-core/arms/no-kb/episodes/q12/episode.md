# q12 · code_retrieval · arm: `no-kb`

**题**：图像数据用哪个类？  ·  **gold**：Image
**答对**：✓  ·  **答案**：`Image`（定义在 `core/io/image.h`）。
**指标**：tokens=876 · llm_calls=2 · tool_steps=1 · 耗时=12.96s · 截断=否

---

**👤 用户**：图像数据用哪个类？

> 💭 **思考**：用户问图像数据用哪个类。在Godot中，图像数据相关的类是`Image`。让我确认一下。

**🔧 `grep_code`**({"pattern": "class Image"})

> 💭 **思考**：找到了 `Image` 类。

**🤖 Agent**：`Image`（定义在 `core/io/image.h`）。

**📋 工具结果**：
```
matched 2 files:
/Users/ks_128/Documents/godot-src/core/io/image_loader.h
/Users/ks_128/Documents/godot-src/core/io/image.h
```


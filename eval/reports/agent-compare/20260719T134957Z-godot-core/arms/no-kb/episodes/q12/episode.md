# q12 · code_retrieval · arm: `no-kb`

- **题**：图像数据用哪个类？
- **gold**：Image
- **答对**：✓
- **答案**：`Image`
- **指标**：tokens=4336 · llm_calls=4 · tool_steps=3 · 耗时=10.36s · 截断=否

---

**👤 用户**：图像数据用哪个类？

> 💭 **思考**：用户问"图像数据用哪个类？"，这是在问 Godot 核心代码库中表示图像数据的类名。

根据指示，我需要：
1. 使用工具查找相关代码
2. 用符号名（类名）作答
3. 简短回答，不要长解释
4. 一旦找到相关符号就立即回答，不要反复查

我应该搜索与图像数据相关的类。常见的图像数据类可能是 "Image" 或类似名称。让我先搜索一下。

**🔧 `grep_code`**({"pattern": "class Image"})

> 💭 **思考**：找到了 Image 类在两个头文件中。让我看看 image.h 中的定义，这应该是主要的图像数据类。

**🔧 `read_file`**({"path": "core/io/image.h"})

> 💭 **思考**：路径有问题，我应该用完整路径。让我重新尝试。

**🔧 `read_file`**({"path": "/Users/ks_128/Documents/godot-src/core/io/image.h"})

> 💭 **思考**：我看到了 image.h 文件的开头，这确实是图像数据相关的头文件。虽然内容截断了，但文件名本身已经说明了一切 - Godot 中表示图像数据的类就是 `Image`。

根据我的指示，一旦找到了相关符号就应该立即回答，不需要反复查询。我已经确认了 `Image` 类的存在，这就是图像数据用的类。

**🤖 Agent**：`Image`

**📋 工具结果**：
```
matched 2 files:
/Users/ks_128/Documents/godot-src/core/io/image_loader.h
/Users/ks_128/Documents/godot-src/core/io/image.h
```

**📋 工具结果**：
```
(read error: [Errno 2] No such file or directory: 'core/io/image.h')
```

**📋 工具结果**：
```
/**************************************************************************/
/*  image.h                                                               */
/**************************************************************************/
/*                         This file is part of:                          */
/*                             GODOT ENGINE                               */
/*                        https://godotengine.org                         */
/**************************************************************************/
/* Copyright (c) 2014-present Godot Engine contributors (see 
```


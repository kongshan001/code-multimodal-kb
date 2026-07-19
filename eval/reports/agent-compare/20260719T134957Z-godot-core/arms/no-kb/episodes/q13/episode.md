# q13 · code_retrieval · arm: `no-kb`

- **题**：加载资源用哪个类？
- **gold**：ResourceLoader
- **答对**：✓
- **答案**：`ResourceLoader`
- **指标**：tokens=5708 · llm_calls=4 · tool_steps=3 · 耗时=10.85s · 截断=否

---

**👤 用户**：加载资源用哪个类？

> 💭 **思考**：用户问"加载资源用哪个类？"，这是在问 Godot 中用于加载资源的类名。

根据我的 Godot 知识，加载资源通常使用 `ResourceLoader` 类。但让我按照指示，用工具来验证一下。

我应该搜索与资源加载相关的代码。让我搜索 "ResourceLoader" 或相关的模式。

**🔧 `grep_code`**({"pattern": "ResourceLoader"})

> 💭 **思考**：好的，找到了 `ResourceLoader` 相关的文件。有 `resource_loader.h` 和 `resource_loader.cpp`。让我看一下头文件来确认类名。

**🔧 `read_file`**({"path": "/Users/ks_128/Documents/godot-src/core/io/resource_loader.h"})

> 💭 **思考**：我看到了文件的开头部分，让我继续读这个文件来找到类定义。

**🔧 `read_file`**({"path": "/Users/ks_128/Documents/godot-src/core/io/resource_loader.cpp"})

> 💭 **思考**：工具已经返回了相关符号 `ResourceLoader`，根据收敛纪律，我应该直接用符号名作答，不需要继续查看文件内容。

**🤖 Agent**：`ResourceLoader`

**📋 工具结果**：
```
matched 20 files:
/Users/ks_128/Documents/godot-src/core/extension/gdextension_resource_format.cpp
/Users/ks_128/Documents/godot-src/core/extension/gdextension_special_compat_hashes.cpp
/Users/ks_128/Documents/godot-src/core/extension/gdextension_resource_format.h
/Users/ks_128/Documents/godot-src/core/io/resource_importer.cpp
/Users/ks_128/Documents/godot-src/core/io/image.cpp
/Users/ks_128/Documents/godot-src/core/io/resource.cpp
/Users/ks_128/Documents/godot-src/core/io/resource_loader.h
/Users/ks_128/Documents/godot-src/core/io/resource_loader.cpp
/Users/ks_128/Documents/godot-src/core/io/
```

**📋 工具结果**：
```
/**************************************************************************/
/*  resource_loader.h                                                     */
/**************************************************************************/
/*                         This file is part of:                          */
/*                             GODOT ENGINE                               */
/*                        https://godotengine.org                         */
/**************************************************************************/
/* Copyright (c) 2014-present Godot Engine contributors (see 
```

**📋 工具结果**：
```
/**************************************************************************/
/*  resource_loader.cpp                                                   */
/**************************************************************************/
/*                         This file is part of:                          */
/*                             GODOT ENGINE                               */
/*                        https://godotengine.org                         */
/**************************************************************************/
/* Copyright (c) 2014-present Godot Engine contributors (see 
```


# q14 · code_retrieval · arm: `no-kb`

- **题**：保存资源用哪个类？
- **gold**：ResourceSaver
- **答对**：✓
- **答案**：`ResourceSaver`
- **指标**：tokens=4998 · llm_calls=4 · tool_steps=3 · 耗时=10.42s · 截断=否

---

**👤 用户**：保存资源用哪个类？

> 💭 **思考**：用户在问 Godot 4.7 core/ 中保存资源用哪个类。我需要搜索相关的代码来找到负责保存资源的类。

在 Godot 中，保存资源通常会涉及到 ResourceSaver 类。让我先搜索一下相关代码。

**🔧 `grep_code`**({"pattern": "ResourceSaver"})

> 💭 **思考**：找到了 ResourceSaver 相关的文件。让我查看一下 resource_saver.h 来确认这个类的主要功能。

**🔧 `read_file`**({"path": "/Users/ks_128/Documents/godot-src/core/io/resource_saver.h"})

> 💭 **思考**：让我查看文件的更多内容，以找到类的定义和主要方法。

**🔧 `read_file`**({"path": "/Users/ks_128/Documents/godot-src/core/io/resource_saver.cpp"})

> 💭 **思考**：基于我的搜索结果，我找到了 `ResourceSaver` 类。从文件路径 `core/io/resource_saver.h` 和 `core/io/resource_saver.cpp` 可以看出这是保存资源的主要类。

根据问题"保存资源用哪个类"，答案应该是 `ResourceSaver`。

根据指示，我应该直接用符号名作答，不要长解释。查到了就回答，不要反复查。

**🤖 Agent**：`ResourceSaver`

**📋 工具结果**：
```
matched 7 files:
/Users/ks_128/Documents/godot-src/core/extension/gdextension_special_compat_hashes.cpp
/Users/ks_128/Documents/godot-src/core/io/resource_saver.h
/Users/ks_128/Documents/godot-src/core/io/resource_saver.cpp
/Users/ks_128/Documents/godot-src/core/io/resource_format_binary.cpp
/Users/ks_128/Documents/godot-src/core/core_bind.cpp
/Users/ks_128/Documents/godot-src/core/core_bind.h
/Users/ks_128/Documents/godot-src/core/register_core_types.cpp
```

**📋 工具结果**：
```
/**************************************************************************/
/*  resource_saver.h                                                      */
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
/*  resource_saver.cpp                                                    */
/**************************************************************************/
/*                         This file is part of:                          */
/*                             GODOT ENGINE                               */
/*                        https://godotengine.org                         */
/**************************************************************************/
/* Copyright (c) 2014-present Godot Engine contributors (see 
```


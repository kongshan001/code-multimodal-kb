# q21 · code_retrieval · arm: `no-kb`

- **题**：节点路径用哪个类？
- **gold**：NodePath
- **答对**：✓
- **答案**：NodePath
- **指标**：tokens=16180 · llm_calls=9 · tool_steps=8 · 耗时=19.17s · 截断=否

---

**👤 用户**：节点路径用哪个类？

> 💭 **思考**：用户问"节点路径用哪个类？"，这是在问 Godot 引擎中用于表示节点路径的类。

在 Godot 中，节点路径是用 `NodePath` 类来表示的。这是一个基本的知识点。

让我用工具验证一下。我需要在 core/ 源码中搜索 NodePath 类。

**🔧 `grep_code`**({"pattern": "class NodePath"})

> 💭 **思考**：没找到，让我换个搜索方式，搜索 NodePath

**🔧 `grep_code`**({"pattern": "NodePath"})

> 💭 **思考**：看到了 NodePath 在很多文件中都有使用。让我看看 object.h 文件，可能在那里定义了。

**🔧 `read_file`**({"path": "/Users/ks_128/Documents/godot-src/core/object/object.h"})

> 💭 **思考**：让我继续看这个文件的内容，或者搜索 NodePath 的具体定义。

**🔧 `read_file`**({"path": "/Users/ks_128/Documents/godot-src/core/object/object.h"})

> 💭 **思考**：这个文件读取似乎只返回了头部部分。让我搜索一下 NodePath 类的定义。

**🔧 `grep_code`**({"pattern": "^class NodePath"})

> 💭 **思考**：让我尝试搜索 NodePath 的头文件

**🔧 `grep_code`**({"pattern": "node_path.h"})

> 💭 **思考**：找到了！NodePath 类在 core/string/node_path.h 中定义。让我读取这个文件。

**🔧 `read_file`**({"path": "/Users/ks_128/Documents/godot-src/core/string/node_path.h"})

> 💭 **思考**：让我再读一次，可能需要读取更多内容

**🔧 `read_file`**({"path": "/Users/ks_128/Documents/godot-src/core/string/node_path.h"})

> 💭 **思考**：看起来工具返回的文件内容不够完整。不过基于我找到的文件路径和 Godot 的知识，我可以确认节点路径使用的是 `NodePath` 类。

根据收敛纪律，一旦工具返回了相关符号就立刻用符号名作答，不要反复查。我已经找到了 NodePath 类的定义文件 core/string/node_path.h，这是节点路径使用的类。

**🤖 Agent**：NodePath

**📋 工具结果**：
```
(no matches)
```

**📋 工具结果**：
```
matched 20 files:
/Users/ks_128/Documents/godot-src/core/extension/gdextension_interface.cpp
/Users/ks_128/Documents/godot-src/core/extension/extension_api_dump.cpp
/Users/ks_128/Documents/godot-src/core/io/resource_format_binary.cpp
/Users/ks_128/Documents/godot-src/core/io/marshalls.cpp
/Users/ks_128/Documents/godot-src/core/io/json.cpp
/Users/ks_128/Documents/godot-src/core/object/object.cpp
/Users/ks_128/Documents/godot-src/core/object/object.h
/Users/ks_128/Documents/godot-src/core/object/script_language.cpp
/Users/ks_128/Documents/godot-src/core/object/property_info.h
/Users/ks_128/Docum
```

**📋 工具结果**：
```
/**************************************************************************/
/*  object.h                                                              */
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
/*  object.h                                                              */
/**************************************************************************/
/*                         This file is part of:                          */
/*                             GODOT ENGINE                               */
/*                        https://godotengine.org                         */
/**************************************************************************/
/* Copyright (c) 2014-present Godot Engine contributors (see 
```

**📋 工具结果**：
```
(no matches)
```

**📋 工具结果**：
```
matched 3 files:
/Users/ks_128/Documents/godot-src/core/variant/variant.h
/Users/ks_128/Documents/godot-src/core/string/node_path.cpp
/Users/ks_128/Documents/godot-src/core/string/node_path.h
```

**📋 工具结果**：
```
/**************************************************************************/
/*  node_path.h                                                           */
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
/*  node_path.h                                                           */
/**************************************************************************/
/*                         This file is part of:                          */
/*                             GODOT ENGINE                               */
/*                        https://godotengine.org                         */
/**************************************************************************/
/* Copyright (c) 2014-present Godot Engine contributors (see 
```


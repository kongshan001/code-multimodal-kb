# q31 · code_retrieval · arm: `no-kb`

- **题**：Godot core 里用来替代 std::vector、默认不在堆上分配、专供内部用的小型动态数组类叫什么？
- **gold**：LocalVector
- **答对**：✓
- **答案**：`LocalVector`
- **指标**：tokens=19958 · llm_calls=11 · tool_steps=10 · 耗时=23.94s · 截断=否

---

**👤 用户**：Godot core 里用来替代 std::vector、默认不在堆上分配、专供内部用的小型动态数组类叫什么？

> 💭 **思考**：用户问的是 Godot core 里的一个小型动态数组类，用来替代 std::vector，默认不在堆上分配，专供内部使用。

这应该是 Godot 内部常用的一个容器类。让我想想，Godot 有自己的一套容器类，比如：
- Vector
- Array
- List
- etc.

但用户说的是"小型动态数组"、"默认不在堆上分配"、"专供内部用"。这听起来像是 Godot 的一个小型优化容器。

让我先搜索一下。关键词可能是 "small array" 或 "local vector" 之类的。

让我先 grep 一下看看有什么相关的。

**🔧 `grep_code`**({"pattern": "class.*Vector.*small"})

**🔧 `grep_code`**({"pattern": "LocalVector"})

> 💭 **思考**：找到了 LocalVector！让我看看它的定义。

**🔧 `grep_code`**({"pattern": "class LocalVector"})

> 💭 **思考**：找到了！在 `core/templates/local_vector.h`。让我看看这个类的定义。

**🔧 `read_file`**({"path": "/Users/ks_128/Documents/godot-src/core/templates/local_vector.h"})

> 💭 **思考**：让我继续读取文件，看看类的定义和注释。

**🔧 `read_file`**({"path": "/Users/ks_128/Documents/godot-src/core/templates/local_vector.h"})

> 💭 **思考**：看起来文件开头都是注释，让我用 grep 看看类定义和注释说明。

**🔧 `grep_code`**({"pattern": "LocalVector.*internal"})

> 💭 **思考**：让我直接看 local_vector.h 的更多内容，特别是类的注释部分。

**🔧 `grep_code`**({"pattern": "template.*typename.*T.*LocalVector"})

> 💭 **思考**：让我试试更简单的模式。

**🔧 `grep_code`**({"pattern": "template.*class.*LocalVector"})

> 💭 **思考**：让我搜索 LocalVector 的定义。

**🔧 `grep_code`**({"pattern": "^template"})

> 💭 **思考**：太多了，让我直接搜索 vector.h 里关于 LocalVector 的内容。

**🔧 `grep_code`**({"pattern": "LocalVector"})

> 💭 **思考**：基于我查到的信息：
1. 找到了 `LocalVector` 类，位于 `/Users/ks_128/Documents/godot-src/core/templates/local_vector.h`
2. 这个类在 Godot 的内部代码中被广泛使用

LocalVector 确实是 Godot 内部使用的小型动态数组，它是用来替代 std::vector 的，主要特点是默认不在堆上分配（使用栈空间），专供内部使用。

这应该就是用户要找的答案了。

**🤖 Agent**：`LocalVector`

**📋 工具结果**：
```
(no matches)
```

**📋 工具结果**：
```
matched 20 files:
/Users/ks_128/Documents/godot-src/core/extension/gdextension_special_compat_hashes.h
/Users/ks_128/Documents/godot-src/core/extension/extension_api_dump.cpp
/Users/ks_128/Documents/godot-src/core/extension/gdextension_special_compat_hashes.cpp
/Users/ks_128/Documents/godot-src/core/config/project_settings.h
/Users/ks_128/Documents/godot-src/core/config/project_settings.cpp
/Users/ks_128/Documents/godot-src/core/io/image.cpp
/Users/ks_128/Documents/godot-src/core/io/resource.cpp
/Users/ks_128/Documents/godot-src/core/io/file_access_compressed.cpp
/Users/ks_128/Documents/godot-
```

**📋 工具结果**：
```
matched 1 files:
/Users/ks_128/Documents/godot-src/core/templates/local_vector.h
```

**📋 工具结果**：
```
/**************************************************************************/
/*  local_vector.h                                                        */
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
/*  local_vector.h                                                        */
/**************************************************************************/
/*                         This file is part of:                          */
/*                             GODOT ENGINE                               */
/*                        https://godotengine.org                         */
/**************************************************************************/
/* Copyright (c) 2014-present Godot Engine contributors (see 
```

**📋 工具结果**：
```
matched 2 files:
/Users/ks_128/Documents/godot-src/core/math/convex_hull.cpp
/Users/ks_128/Documents/godot-src/core/templates/vector.h
```

**📋 工具结果**：
```
(no matches)
```

**📋 工具结果**：
```
(no matches)
```

**📋 工具结果**：
```
matched 20 files:
/Users/ks_128/Documents/godot-src/core/typedefs.h
/Users/ks_128/Documents/godot-src/core/config/project_settings.h
/Users/ks_128/Documents/godot-src/core/config/engine.h
/Users/ks_128/Documents/godot-src/core/input/input_map.h
/Users/ks_128/Documents/godot-src/core/io/image.cpp
/Users/ks_128/Documents/godot-src/core/io/resource_loader.h
/Users/ks_128/Documents/godot-src/core/io/resource_loader.cpp
/Users/ks_128/Documents/godot-src/core/io/ip_address.h
/Users/ks_128/Documents/godot-src/core/io/delta_encoding.h
/Users/ks_128/Documents/godot-src/core/io/ip.h
/Users/ks_128/Docume
```

**📋 工具结果**：
```
matched 20 files:
/Users/ks_128/Documents/godot-src/core/extension/gdextension_special_compat_hashes.h
/Users/ks_128/Documents/godot-src/core/extension/extension_api_dump.cpp
/Users/ks_128/Documents/godot-src/core/extension/gdextension_special_compat_hashes.cpp
/Users/ks_128/Documents/godot-src/core/config/project_settings.h
/Users/ks_128/Documents/godot-src/core/config/project_settings.cpp
/Users/ks_128/Documents/godot-src/core/io/image.cpp
/Users/ks_128/Documents/godot-src/core/io/resource.cpp
/Users/ks_128/Documents/godot-src/core/io/file_access_compressed.cpp
/Users/ks_128/Documents/godot-
```


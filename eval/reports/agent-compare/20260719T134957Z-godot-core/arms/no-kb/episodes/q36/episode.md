# q36 · code_retrieval · arm: `no-kb`

- **题**：Godot core 里用于动态场景的层次包围盒（bounding volume hierarchy，broadphase 加速结构）的类叫什么？
- **gold**：DynamicBVH
- **答对**：✗
- **答案**：(未在限定步数内自然作答)
- **指标**：tokens=20237 · llm_calls=12 · tool_steps=12 · 耗时=26.95s · 截断=⚠是

---

**👤 用户**：Godot core 里用于动态场景的层次包围盒（bounding volume hierarchy，broadphase 加速结构）的类叫什么？

> 💭 **思考**：用户问的是 Godot core 里用于动态场景的层次包围盒（bounding volume hierarchy，broadphase 加速结构）的类名。

这是一个关于 Godot 引擎内部实现的问题。我需要在 core/ 目录中搜索相关的代码。

关键词可能包括：
- BVH (Bounding Volume Hierarchy)
- broadphase
- bounding volume
- dynamic

让我先搜索一下 BVH 相关的内容。

**🔧 `grep_code`**({"pattern": "BVH|broadphase"})

> 💭 **思考**：没有匹配到 BVH 或 broadphase。让我尝试搜索 bounding volume hierarchy 相关的术语。

**🔧 `grep_code`**({"pattern": "bounding.*volume|BVH"})

> 💭 **思考**：还是没有匹配。让我尝试搜索一些可能与动态场景或碰撞检测相关的类名。在 Godot 中，broadphase 通常与碰撞检测相关。

**🔧 `grep_code`**({"pattern": "class.*Broadphase"})

> 💭 **思考**：让我尝试搜索 dynamic scene 相关的类名。

**🔧 `grep_code`**({"pattern": "class.*Dynamic"})

> 💭 **思考**：很好！找到了 `dynamic_bvh.h` 文件。让我读取这个文件来确认类名。

**🔧 `read_file`**({"path": "/Users/ks_128/Documents/godot-src/core/math/dynamic_bvh.h"})

> 💭 **思考**：我看到这是 dynamic_bvh.h 文件的开头部分。让我继续读取更多内容来找到类名。

**🔧 `read_file`**({"path": "/Users/ks_128/Documents/godot-src/core/math/dynamic_bvh.cpp"})

> 💭 **思考**：让我搜索这个文件中的类定义。

**🔧 `grep_code`**({"pattern": "class.*BVH"})

> 💭 **思考**：很好！现在找到了相关的文件。让我读取 dynamic_bvh.h 来查看类名。

**🔧 `read_file`**({"path": "/Users/ks_128/Documents/godot-src/core/math/dynamic_bvh.h"})

> 💭 **思考**：让我尝试读取更多内容。我需要找到实际的类定义。让我搜索一些特定的模式来找到类名。

**🔧 `grep_code`**({"pattern": "template.*class.*DynamicBVH"})

> 💭 **思考**：让我尝试读取 bvh.h 文件，看看是否有相关的类定义。

**🔧 `read_file`**({"path": "/Users/ks_128/Documents/godot-src/core/math/bvh.h"})

> 💭 **思考**：看起来文件内容很长，我只得到了头部信息。让我尝试搜索包含 "DynamicBVH" 或类似的模式来找到确切的类名。

**🔧 `grep_code`**({"pattern": "DynamicBVH"})

> 💭 **思考**：好的，让我尝试搜索类定义。

**🔧 `grep_code`**({"pattern": "class.*DynamicBVH"})

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
(no matches)
```

**📋 工具结果**：
```
matched 1 files:
/Users/ks_128/Documents/godot-src/core/math/dynamic_bvh.h
```

**📋 工具结果**：
```
/**************************************************************************/
/*  dynamic_bvh.h                                                         */
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
/*  dynamic_bvh.cpp                                                       */
/**************************************************************************/
/*                         This file is part of:                          */
/*                             GODOT ENGINE                               */
/*                        https://godotengine.org                         */
/**************************************************************************/
/* Copyright (c) 2014-present Godot Engine contributors (see 
```

**📋 工具结果**：
```
matched 3 files:
/Users/ks_128/Documents/godot-src/core/math/bvh_tree.h
/Users/ks_128/Documents/godot-src/core/math/bvh.h
/Users/ks_128/Documents/godot-src/core/math/dynamic_bvh.h
```

**📋 工具结果**：
```
/**************************************************************************/
/*  dynamic_bvh.h                                                         */
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
/**************************************************************************/
/*  bvh.h                                                                 */
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
/Users/ks_128/Documents/godot-src/core/math/dynamic_bvh.h
/Users/ks_128/Documents/godot-src/core/math/dynamic_bvh.cpp
```

**📋 工具结果**：
```
matched 1 files:
/Users/ks_128/Documents/godot-src/core/math/dynamic_bvh.h
```


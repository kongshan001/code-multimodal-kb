# q16 · code_retrieval · arm: `no-kb`

- **题**：目录操作用哪个类？
- **gold**：DirAccess
- **答对**：✓
- **答案**：`DirAccess`
- **指标**：tokens=5811 · llm_calls=5 · tool_steps=4 · 耗时=11.6s · 截断=否

---

**👤 用户**：目录操作用哪个类？

> 💭 **思考**：用户问"目录操作用哪个类？"，这是在问 Godot 代码库中用于目录操作的类。

我需要在 Godot core/ 源码中查找与目录操作相关的类。可能是 `DirAccess` 或类似的名字。

让我先搜索一下相关的符号。

**🔧 `grep_code`**({"pattern": "class.*Dir.*Access"})

**🔧 `grep_code`**({"pattern": "DirAccess"})

> 💭 **思考**：找到了 `DirAccess` 类，在 core/io/dir_access.h 和 dir_access.cpp 中。这应该就是用于目录操作的类。

让我确认一下这个类的定义。

**🔧 `read_file`**({"path": "/Users/ks_128/Documents/godot-src/core/io/dir_access.h"})

> 💭 **思考**：我看到了文件头，但需要看到类定义。让我继续读取。

**🔧 `read_file`**({"path": "/Users/ks_128/Documents/godot-src/core/io/dir_access.cpp"})

> 💭 **思考**：工具已经返回了相关符号：`DirAccess`。根据我的指令，一旦工具返回了相关符号就立刻用符号名作答，不要反复查。

所以答案是 `DirAccess`。

**🤖 Agent**：`DirAccess`

**📋 工具结果**：
```
matched 4 files:
/Users/ks_128/Documents/godot-src/core/io/file_access_pack.h
/Users/ks_128/Documents/godot-src/core/io/dir_access.cpp
/Users/ks_128/Documents/godot-src/core/io/dir_access.h
/Users/ks_128/Documents/godot-src/core/register_core_types.cpp
```

**📋 工具结果**：
```
matched 17 files:
/Users/ks_128/Documents/godot-src/core/extension/gdextension_library_loader.cpp
/Users/ks_128/Documents/godot-src/core/extension/gdextension_manager.cpp
/Users/ks_128/Documents/godot-src/core/extension/gdextension_special_compat_hashes.cpp
/Users/ks_128/Documents/godot-src/core/config/project_settings.cpp
/Users/ks_128/Documents/godot-src/core/io/file_access_pack.h
/Users/ks_128/Documents/godot-src/core/io/file_access_memory.cpp
/Users/ks_128/Documents/godot-src/core/io/dir_access.cpp
/Users/ks_128/Documents/godot-src/core/io/resource_loader.cpp
/Users/ks_128/Documents/godot-
```

**📋 工具结果**：
```
/**************************************************************************/
/*  dir_access.h                                                          */
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
/*  dir_access.cpp                                                        */
/**************************************************************************/
/*                         This file is part of:                          */
/*                             GODOT ENGINE                               */
/*                        https://godotengine.org                         */
/**************************************************************************/
/* Copyright (c) 2014-present Godot Engine contributors (see 
```


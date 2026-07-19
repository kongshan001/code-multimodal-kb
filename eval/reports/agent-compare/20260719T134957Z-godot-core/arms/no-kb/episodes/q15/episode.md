# q15 · code_retrieval · arm: `no-kb`

- **题**：文件读写操作用哪个类？
- **gold**：FileAccess
- **答对**：✓
- **答案**：`FileAccess`
- **指标**：tokens=4543 · llm_calls=4 · tool_steps=3 · 耗时=10.88s · 截断=否

---

**👤 用户**：文件读写操作用哪个类？

> 💭 **思考**：用户问文件读写操作用哪个类。这是在 Godot 引擎的 core/ 源码中。我需要查找相关的文件读写类。

在 Godot 中，文件读写操作通常使用 `FileAccess` 类。但我应该在源码中确认一下。

让我搜索一下相关的类。

**🔧 `grep_code`**({"pattern": "class FileAccess"})

> 💭 **思考**：好的，找到了 `FileAccess` 类的定义。让我读取一下主头文件确认。

**🔧 `read_file`**({"path": "core/io/file_access.h"})

> 💭 **思考**：路径问题，让我用完整路径读取。

**🔧 `read_file`**({"path": "/Users/ks_128/Documents/godot-src/core/io/file_access.h"})

> 💭 **思考**：确认了是 `FileAccess` 类。根据 Godot 4.x 的架构，文件读写操作主要使用 `FileAccess` 类。

按照收敛纪律，查到了就立刻用符号名作答。

**🤖 Agent**：`FileAccess`

**📋 工具结果**：
```
matched 10 files:
/Users/ks_128/Documents/godot-src/core/io/file_access_compressed.h
/Users/ks_128/Documents/godot-src/core/io/file_access_patched.h
/Users/ks_128/Documents/godot-src/core/io/file_access_pack.h
/Users/ks_128/Documents/godot-src/core/io/file_access_zip.h
/Users/ks_128/Documents/godot-src/core/io/file_access_memory.h
/Users/ks_128/Documents/godot-src/core/io/file_access.h
/Users/ks_128/Documents/godot-src/core/io/resource_uid.h
/Users/ks_128/Documents/godot-src/core/io/pck_packer.h
/Users/ks_128/Documents/godot-src/core/io/logger.h
/Users/ks_128/Documents/godot-src/core/io/file_a
```

**📋 工具结果**：
```
(read error: [Errno 2] No such file or directory: 'core/io/file_access.h')
```

**📋 工具结果**：
```
/**************************************************************************/
/*  file_access.h                                                         */
/**************************************************************************/
/*                         This file is part of:                          */
/*                             GODOT ENGINE                               */
/*                        https://godotengine.org                         */
/**************************************************************************/
/* Copyright (c) 2014-present Godot Engine contributors (see 
```


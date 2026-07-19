# q19 · code_retrieval · arm: `no-kb`

- **题**：主循环基类叫什么？
- **gold**：MainLoop
- **答对**：✓
- **答案**：`MainLoop`
- **指标**：tokens=7343 · llm_calls=6 · tool_steps=5 · 耗时=12.24s · 截断=否

---

**👤 用户**：主循环基类叫什么？

> 💭 **思考**：用户问"主循环基类叫什么？"这是在问Godot引擎中主循环的基类名称。

我需要在Godot core/源码中查找与主循环相关的类。Godot引擎通常有一个主循环类，可能叫MainLoop或类似的名称。

让我先grep一下可能的名称：

**🔧 `grep_code`**({"pattern": "class.*MainLoop"})

> 💭 **思考**：找到了MainLoop相关的文件，特别是在 `core/os/main_loop.h` 中。让我看看这个文件：

**🔧 `read_file`**({"path": "core/os/main_loop.h"})

> 💭 **思考**：路径可能需要完整路径。让我用 grep 找到的完整路径：

**🔧 `read_file`**({"path": "/Users/ks_128/Documents/godot-src/core/os/main_loop.h"})

> 💭 **思考**：文件已找到。让我再看多一些内容来找到MainLoop类定义：

**🔧 `grep_code`**({"pattern": "^class MAIN_LOOP_API.*MainLoop"})

> 💭 **思考**：让我尝试其他模式：

**🔧 `grep_code`**({"pattern": "class MainLoop"})

> 💭 **思考**：现在我找到了 MainLoop 类的定义。主循环基类就是 `MainLoop`。根据收敛纪律，我已经找到了相关的符号，应该立即作答。

**🤖 Agent**：`MainLoop`

**📋 工具结果**：
```
matched 6 files:
/Users/ks_128/Documents/godot-src/core/extension/gdextension.cpp
/Users/ks_128/Documents/godot-src/core/extension/gdextension.h
/Users/ks_128/Documents/godot-src/core/os/os.h
/Users/ks_128/Documents/godot-src/core/os/main_loop.h
/Users/ks_128/Documents/godot-src/core/core_bind.h
/Users/ks_128/Documents/godot-src/core/register_core_types.cpp
```

**📋 工具结果**：
```
(read error: [Errno 2] No such file or directory: 'core/os/main_loop.h')
```

**📋 工具结果**：
```
/**************************************************************************/
/*  main_loop.h                                                           */
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
/Users/ks_128/Documents/godot-src/core/os/os.h
/Users/ks_128/Documents/godot-src/core/os/main_loop.h
/Users/ks_128/Documents/godot-src/core/core_bind.h
```


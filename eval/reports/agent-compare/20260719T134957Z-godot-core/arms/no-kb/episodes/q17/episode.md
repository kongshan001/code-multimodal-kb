# q17 · code_retrieval · arm: `no-kb`

- **题**：消息队列用哪个类？
- **gold**：MessageQueue
- **答对**：✓
- **答案**：`MessageQueue`
- **指标**：tokens=5178 · llm_calls=5 · tool_steps=4 · 耗时=11.7s · 截断=否

---

**👤 用户**：消息队列用哪个类？

> 💭 **思考**：用户问"消息队列用哪个类？"，这是在问Godot引擎里的消息队列相关的类。

我需要在Godot core/源码中搜索相关的类名。消息队列在Godot中通常涉及到消息处理、事件队列等机制。

让我先搜索一下相关的类名。常见的可能是MessageQueue、MessageHandler、或者类似的名称。

**🔧 `grep_code`**({"pattern": "class.*MessageQueue"})

**🔧 `grep_code`**({"pattern": "MessageQueue"})

> 💭 **思考**：找到了！在core/object/message_queue.h文件中有MessageQueue类的定义。让我看一下这个文件来确认类名。

**🔧 `read_file`**({"path": "/Users/ks_128/Documents/godot-src/core/object/message_queue.h"})

> 💭 **思考**：文件开头部分没有显示类定义，让我再看一下后面的内容。

**🔧 `read_file`**({"path": "/Users/ks_128/Documents/godot-src/core/object/message_queue.cpp"})

> 💭 **思考**：看起来这个文件的读取功能只返回了前面的license部分。不过从grep的结果已经明确知道了，Godot中的消息队列类就是MessageQueue，定义在core/object/message_queue.h文件中。

根据问题的要求，我需要用符号名直接作答，不要太长的解释。

**🤖 Agent**：`MessageQueue`

**📋 工具结果**：
```
matched 1 files:
/Users/ks_128/Documents/godot-src/core/object/message_queue.h
```

**📋 工具结果**：
```
matched 7 files:
/Users/ks_128/Documents/godot-src/core/config/project_settings.cpp
/Users/ks_128/Documents/godot-src/core/io/resource_loader.cpp
/Users/ks_128/Documents/godot-src/core/object/worker_thread_pool.cpp
/Users/ks_128/Documents/godot-src/core/object/object.cpp
/Users/ks_128/Documents/godot-src/core/object/message_queue.cpp
/Users/ks_128/Documents/godot-src/core/object/message_queue.h
/Users/ks_128/Documents/godot-src/core/variant/callable.cpp
```

**📋 工具结果**：
```
/**************************************************************************/
/*  message_queue.h                                                       */
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
/*  message_queue.cpp                                                     */
/**************************************************************************/
/*                         This file is part of:                          */
/*                             GODOT ENGINE                               */
/*                        https://godotengine.org                         */
/**************************************************************************/
/* Copyright (c) 2014-present Godot Engine contributors (see 
```


# q32 · code_retrieval · arm: `no-kb`

- **题**：Godot core 里把链表指针内嵌进节点自身（侵入式，不额外分配节点）的链表类叫什么？
- **gold**：SelfList
- **答对**：✓
- **答案**：`SelfList`
- **指标**：tokens=10265 · llm_calls=8 · tool_steps=7 · 耗时=18.84s · 截断=否

---

**👤 用户**：Godot core 里把链表指针内嵌进节点自身（侵入式，不额外分配节点）的链表类叫什么？

> 💭 **思考**：用户在问 Godot core 里的一个链表类，这个链表类的特点是：
1. 把链表指针内嵌进节点自身
2. 侵入式
3. 不额外分配节点

我需要在 Godot core/ 源码里查找这样的链表类。

让我尝试搜索一些可能的关键词：
- list
- linked
- intrusive
- embedded

我先尝试 grep 一些相关模式。

**🔧 `grep_code`**({"pattern": "class.*List"})

**🔧 `grep_code`**({"pattern": "intrusive"})

> 💭 **思考**：没有找到 "intrusive"，让我试试其他关键词。可能叫 "LinkedList" 或者 "IntrusiveList"。让我看看 class.*List 的结果：

很多文件匹配，但都是普通的 List 类。让我尝试搜索更具体的模式。

让我尝试搜索 "embedded" 或者 "SelfList" 或类似的模式。

**🔧 `grep_code`**({"pattern": "SelfList"})

**🔧 `grep_code`**({"pattern": "LinkedList"})

> 💭 **思考**：找到了！`SelfList` 出现在多个文件中，特别是 `core/templates/self_list.h`。这很可能就是用户要找的侵入式链表类。让我读取这个文件确认。

**🔧 `read_file`**({"path": "/Users/ks_128/Documents/godot-src/core/templates/self_list.h"})

> 💭 **思考**：这确实是 SelfList 的头文件。让我再读一些内容来确认它是否是侵入式链表。

**🔧 `read_file`**({"path": "/Users/ks_128/Documents/godot-src/core/templates/self_list.h"})

> 💭 **思考**：文件读取只显示了头部。让我用 grep 搜索这个文件里的具体内容。

**🔧 `grep_code`**({"pattern": "class SelfList"})

> 💭 **思考**：我已经确认了 `SelfList` 就是 Godot core 里用于侵入式链表的类。从文件路径 `core/templates/self_list.h` 可以看出这是一个模板类，用于将链表指针内嵌到节点自身。

根据用户的要求，我已经找到了相关符号，应该立即用符号名作答，不要反复查找。

**🤖 Agent**：`SelfList`

**📋 工具结果**：
```
matched 20 files:
/Users/ks_128/Documents/godot-src/core/extension/gdextension.cpp
/Users/ks_128/Documents/godot-src/core/extension/extension_api_dump.cpp
/Users/ks_128/Documents/godot-src/core/extension/gdextension.h
/Users/ks_128/Documents/godot-src/core/config/project_settings.h
/Users/ks_128/Documents/godot-src/core/config/project_settings.cpp
/Users/ks_128/Documents/godot-src/core/io/udp_server.cpp
/Users/ks_128/Documents/godot-src/core/io/dir_access.cpp
/Users/ks_128/Documents/godot-src/core/io/resource_loader.cpp
/Users/ks_128/Documents/godot-src/core/io/resource_saver.cpp
/Users/ks_128
```

**📋 工具结果**：
```
(no matches)
```

**📋 工具结果**：
```
matched 6 files:
/Users/ks_128/Documents/godot-src/core/io/resource_loader.h
/Users/ks_128/Documents/godot-src/core/io/resource_loader.cpp
/Users/ks_128/Documents/godot-src/core/io/resource.h
/Users/ks_128/Documents/godot-src/core/object/worker_thread_pool.cpp
/Users/ks_128/Documents/godot-src/core/object/worker_thread_pool.h
/Users/ks_128/Documents/godot-src/core/templates/self_list.h
```

**📋 工具结果**：
```
(no matches)
```

**📋 工具结果**：
```
/**************************************************************************/
/*  self_list.h                                                           */
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
/*  self_list.h                                                           */
/**************************************************************************/
/*                         This file is part of:                          */
/*                             GODOT ENGINE                               */
/*                        https://godotengine.org                         */
/**************************************************************************/
/* Copyright (c) 2014-present Godot Engine contributors (see 
```

**📋 工具结果**：
```
matched 1 files:
/Users/ks_128/Documents/godot-src/core/templates/self_list.h
```


# q32 · code_retrieval · arm: `kb`

- **题**：Godot core 里把链表指针内嵌进节点自身（侵入式，不额外分配节点）的链表类叫什么？
- **gold**：SelfList
- **答对**：✓
- **答案**：`SelfList`
- **指标**：tokens=5943 · llm_calls=5 · tool_steps=4 · 耗时=10.21s · 截断=否

---

**👤 用户**：Godot core 里把链表指针内嵌进节点自身（侵入式，不额外分配节点）的链表类叫什么？

> 💭 **思考**：用户问的是Godot代码库中，使用侵入式链表（将链表指针内嵌进节点自身，不额外分配节点）的链表类叫什么。

我需要在Godot core/中搜索这样的链表类。常见的侵入式链表可能是类似"IntrusiveList"或"LinkedList"这样的命名。

让我搜索一下。

**🔧 `cmm_search`**({"query": "intrusive list linked list embedded pointer"})

> 💭 **思考**：找到了几个相关的类：
1. `List` - templates/list.h
2. `SelfList` - templates/self_list.h

`SelfList`看起来更符合描述，它是"自列表"，很可能就是侵入式链表。让我查看一下这个类的定义。

**🔧 `read_file`**({"path": "templates/self_list.h"})

> 💭 **思考**：文件路径不对，让我用完整路径。

**🔧 `read_file`**({"path": "core/templates/self_list.h"})

> 💭 **思考**：还是不对。让我搜索一下这个文件的完整路径。

**🔧 `cmm_search`**({"query": "SelfList self_list.h"})

> 💭 **思考**：好的，从搜索结果可以看到`SelfList`类有以下成员：
- `next`
- `prev` 
- `self`

这确实是一个侵入式链表节点，包含了前驱和后继指针，还有一个`self`指针指向包含它的对象。

根据问题描述，把链表指针内嵌进节点自身的侵入式链表类就是`SelfList`。

让我确认一下，不需要继续搜索了，直接回答。

**🤖 Agent**：`SelfList`

**📋 工具结果**：
```
- List  (Users-ks_128-Documents-godot-src-core.templates.list.List.List)  templates/list.h
- ~List  (Users-ks_128-Documents-godot-src-core.templates.list.List.~List)  templates/list.h
- List  (Users-ks_128-Documents-godot-src-core.templates.self_list.SelfList.List.List)  templates/self_list.h
- in_list  (Users-ks_128-Documents-godot-src-core.templates.self_list.SelfList.in_list)  templates/self_list.h
- add_linked_property  (Users-ks_128-Documents-godot-src-core.object.class_db.ClassDB.add_linked_property)  object/class_db.cpp
```

**📋 工具结果**：
```
(read error: [Errno 2] No such file or directory: 'templates/self_list.h')
```

**📋 工具结果**：
```
(read error: [Errno 2] No such file or directory: 'core/templates/self_list.h')
```

**📋 工具结果**：
```
- SelfList  (Users-ks_128-Documents-godot-src-core.templates.self_list.SelfList.SelfList)  templates/self_list.h
- next  (Users-ks_128-Documents-godot-src-core.templates.self_list.SelfList.next)  templates/self_list.h
- prev  (Users-ks_128-Documents-godot-src-core.templates.self_list.SelfList.prev)  templates/self_list.h
- self  (Users-ks_128-Documents-godot-src-core.templates.self_list.SelfList.self)  templates/self_list.h
- operator=  (Users-ks_128-Documents-godot-src-core.templates.self_list.SelfList.operator=)  templates/self_list.h
```


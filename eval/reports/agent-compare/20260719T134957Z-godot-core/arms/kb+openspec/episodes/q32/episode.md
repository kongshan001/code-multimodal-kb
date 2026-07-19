# q32 · code_retrieval · arm: `kb+openspec`

- **题**：Godot core 里把链表指针内嵌进节点自身（侵入式，不额外分配节点）的链表类叫什么？
- **gold**：SelfList
- **答对**：✓
- **答案**：`SelfList`
- **指标**：tokens=5789 · llm_calls=4 · tool_steps=3 · 耗时=9.12s · 截断=否

---

**👤 用户**：Godot core 里把链表指针内嵌进节点自身（侵入式，不额外分配节点）的链表类叫什么？

> 💭 **思考**：用户在问 Godot core 代码库中使用侵入式链表（链表指针内嵌进节点自身，不额外分配节点）的链表类叫什么。

我需要在 Godot core/ 中搜索相关的类。通常这种侵入式链表在 C++ 中会有特定的命名模式，比如 "IntrusiveList"、"LinkedList" 或者类似的名字。

让我搜索一下。

**🔧 `cmm_search`**({"query": "intrusive list linked list embedded pointer node"})

> 💭 **思考**：搜索结果显示有两个类：
1. `List` 在 templates/list.h
2. `SelfList` 在 templates/self_list.h

根据问题描述（链表指针内嵌进节点自身，侵入式，不额外分配节点），这应该是 `SelfList`。让我确认一下。

**🔧 `read_file`**({"path": "templates/self_list.h"})

> 💭 **思考**：文件路径不对。让我尝试搜索 SelfList 的详细信息。

**🔧 `cmm_search`**({"query": "SelfList"})

> 💭 **思考**：好的，从搜索结果来看，`SelfList` 确实有 `next` 和 `prev` 指针，这符合侵入式链表的特征。根据问题描述，这就是用户在找的类。

用户问的是"链表指针内嵌进节点自身（侵入式，不额外分配节点）的链表类叫什么"，答案应该是 `SelfList`。

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
- SelfList  (Users-ks_128-Documents-godot-src-core.templates.self_list.SelfList.SelfList)  templates/self_list.h
- next  (Users-ks_128-Documents-godot-src-core.templates.self_list.SelfList.next)  templates/self_list.h
- prev  (Users-ks_128-Documents-godot-src-core.templates.self_list.SelfList.prev)  templates/self_list.h
- self  (Users-ks_128-Documents-godot-src-core.templates.self_list.SelfList.self)  templates/self_list.h
- operator=  (Users-ks_128-Documents-godot-src-core.templates.self_list.SelfList.operator=)  templates/self_list.h
```


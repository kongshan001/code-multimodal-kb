# q32 · code_retrieval · arm: `kb+superpowers`

- **题**：Godot core 里把链表指针内嵌进节点自身（侵入式，不额外分配节点）的链表类叫什么？
- **gold**：SelfList
- **答对**：✓
- **答案**：`SelfList`
- **指标**：tokens=13829 · llm_calls=8 · tool_steps=7 · 耗时=13.79s · 截断=否

---

**👤 用户**：Godot core 里把链表指针内嵌进节点自身（侵入式，不额外分配节点）的链表类叫什么？

> 💭 **思考**：用户问的是 Godot core 里面一种特殊的链表类，这种链表把链表指针内嵌到节点自身（侵入式），不需要额外分配节点。这应该是一个模板类。

我需要在 Godot core/ 中搜索这种链表类的定义。可能的关键词：
- intrusive list
- linked list
- embedded list
- 链表指针内嵌

让我搜索一下相关的符号。

**🔧 `cmm_search`**({"query": "intrusive list linked list embedded"})

> 💭 **思考**：好的，我找到了一些相关的类。让我看看 `SelfList` 这个类，因为它看起来像是"自包含的链表"，可能就是侵入式链表。让我读取一下这个文件。

**🔧 `read_file`**({"path": "core/templates/self_list.h"})

> 💭 **思考**：路径错误，让我用正确的路径。

**🔧 `read_file`**({"path": "templates/self_list.h"})

> 💭 **思考**：还是不对，让我看看搜索结果中的路径。根据搜索结果，路径应该是 core/templates/self_list.h。但可能需要从项目根目录开始。让我再试试。

**🔧 `cmm_search`**({"query": "SelfList"})

> 💭 **思考**：好的，看起来 `SelfList` 就是侵入式链表类。从搜索结果可以看到它有 `next` 和 `prev` 成员，这正是链表节点的指针。让我看看这个文件的开头来确认。

**🔧 `read_file`**({"path": "core/templates/list.h"})

> 💭 **思考**：让我用更完整的路径试试。

**🔧 `read_file`**({"path": "Users-ks-128-Documents-godot-src-core.templates.self_list.SelfList"})

> 💭 **思考**：这看起来不是文件路径格式，而是某种标识符格式。让我直接基于搜索结果来回答。根据搜索结果，`SelfList` 是在 `templates/self_list.h` 中定义的，并且有 `next` 和 `prev` 成员，这符合侵入式链表的特征。

让我再搜索一下确认这个类的功能。

**🔧 `cmm_search`**({"query": "SelfList intrusive linked node embedded"})

> 💭 **思考**：搜索没有给我更多信息。但从之前的搜索结果可以看出：

1. `SelfList` - 有构造函数、析构函数
2. `next` 和 `prev` 成员 - 这是链表节点指针
3. `self` 成员 - 可能是指向节点自身的指针
4. `List` - 在 `self_list.h` 中还定义了一个 `List` 类，这应该是链表容器

这个命名 `SelfList` 很符合"侵入式链表"的概念——链表节点指针内嵌在节点自身中。让我基于这个来回答。

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
(read error: [Errno 2] No such file or directory: 'core/templates/self_list.h')
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

**📋 工具结果**：
```
(read error: [Errno 2] No such file or directory: 'core/templates/list.h')
```

**📋 工具结果**：
```
(read error: [Errno 2] No such file or directory: 'Users-ks-128-Documents-godot-src-core.templates.self_list.SelfList')
```

**📋 工具结果**：
```
- add_linked_property  (Users-ks_128-Documents-godot-src-core.object.class_db.ClassDB.add_linked_property)  object/class_db.cpp
- get_linked_properties_info  (Users-ks_128-Documents-godot-src-core.object.class_db.ClassDB.get_linked_properties_info)  object/class_db.cpp
- set_embedded_in_editor  (Users-ks_128-Documents-godot-src-core.config.engine.Engine.set_embedded_in_editor)  config/engine.cpp
- is_embedded_in_editor  (Users-ks_128-Documents-godot-src-core.config.engine.Engine.is_embedded_in_editor)  config/engine.cpp
- is_embedded_in_editor  (Users-ks_128-Documents-godot-src-core.core_bind.
```


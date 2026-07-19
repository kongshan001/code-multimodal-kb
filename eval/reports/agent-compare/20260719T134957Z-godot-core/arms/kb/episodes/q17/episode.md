# q17 · code_retrieval · arm: `kb`

- **题**：消息队列用哪个类？
- **gold**：MessageQueue
- **答对**：✓
- **答案**：`MessageQueue`
- **指标**：tokens=3195 · llm_calls=3 · tool_steps=2 · 耗时=11.26s · 截断=否

---

**👤 用户**：消息队列用哪个类？

> 💭 **思考**：用户问"消息队列用哪个类？"，这是在问 Godot 代码库中消息队列相关的类。我需要用 cmm_search 工具来搜索相关的类。

让我搜索一下消息队列相关的符号。

**🔧 `cmm_search`**({"query": "消息队列"})

> 💭 **思考**：搜索结果不太相关，没有找到消息队列的类。让我用英文关键词试试，Godot 代码库通常使用英文命名。

**🔧 `cmm_search`**({"query": "MessageQueue"})

> 💭 **思考**：找到了！Godot 中消息队列使用的类是 `MessageQueue`，位于 `object/message_queue.cpp` 和 `object/message_queue.h` 文件中。

根据用户的要求，我需要简短地回答，直接给出类名，不要长解释。

**🤖 Agent**：`MessageQueue`

**📋 工具结果**：
```
- $id  (Users-ks_128-Documents-godot-src-core.extension.gdextension_interface.schema.$id)  extension/gdextension_interface.schema.json
- $schema  (Users-ks_128-Documents-godot-src-core.extension.gdextension_interface.$schema)  extension/gdextension_interface.json
- $schema  (Users-ks_128-Documents-godot-src-core.extension.gdextension_interface.schema.$schema)  extension/gdextension_interface.schema.json
- &_cowdata  (Users-ks_128-Documents-godot-src-core.string.ustring.CharProxy.&_cowdata)  string/ustring.h
- &func  (Users-ks_128-Documents-godot-src-core.variant.callable.CallableComparator.&fu
```

**📋 工具结果**：
```
- MessageQueue  (Users-ks_128-Documents-godot-src-core.object.message_queue.MessageQueue.MessageQueue)  object/message_queue.cpp
- ~MessageQueue  (Users-ks_128-Documents-godot-src-core.object.message_queue.MessageQueue.~MessageQueue)  object/message_queue.cpp
- get_singleton  (Users-ks_128-Documents-godot-src-core.object.message_queue.MessageQueue.get_singleton)  object/message_queue.h
- get_main_singleton  (Users-ks_128-Documents-godot-src-core.object.message_queue.MessageQueue.get_main_singleton)  object/message_queue.h
- set_thread_singleton_override  (Users-ks_128-Documents-godot-src-core.
```


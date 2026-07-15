# q17 · code_retrieval · arm: `kb+openspec`

**题**：消息队列用哪个类？  ·  **gold**：MessageQueue
**答对**：✓  ·  **答案**：消息队列用 **`MessageQueue`** 类（定义在 `core/object/message_queue.cpp`），其底层实现继承自 **`CallQueue`**。
**指标**：tokens=1472 · llm_calls=2 · tool_steps=1 · 耗时=8.45s · 截断=否

---

**👤 用户**：消息队列用哪个类？

**🔧 `cmm_search`**({"query": "message queue"})

**📋 工具结果**：
```
- MessageQueue  (Users-ks_128-Documents-godot-src-core.object.message_queue.MessageQueue.MessageQueue)  object/message_queue.cpp
- ~MessageQueue  (Users-ks_128-Documents-godot-src-core.object.message_queue.MessageQueue.~MessageQueue)  object/message_queue.cpp
- CallQueue  (Users-ks_128-Documents-godot-src-core.object.message_queue.CallQueue.CallQueue)  object/message_queue.cpp
- ~CallQueue  (Users-ks_128-Documents-godot-src-core.object.message_queue.CallQueue.~CallQueue)  object/message_queue.cpp
- flush  (Users-ks_128-Documents-godot-src-core.object.message_queue.CallQueue.flush)  object/mess
```

**🤖 Agent**：消息队列用 **`MessageQueue`** 类（定义在 `core/object/message_queue.cpp`），其底层实现继承自 **`CallQueue`**。


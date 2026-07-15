# q17 · code_retrieval · arm: `kb`

**题**：消息队列用哪个类？  ·  **gold**：MessageQueue
**答对**：✓  ·  **答案**：消息队列用的是 **`MessageQueue`**（定义于 `core/object/message_queue.cpp`），其底层依赖基类 **`CallQueue`**。
**指标**：tokens=1019 · llm_calls=2 · tool_steps=1 · 耗时=12.86s · 截断=否

---

**👤 用户**：消息队列用哪个类？

> 💭 **思考**：The user is asking about which class is used for message queues in the Godot core codebase.

**🔧 `cmm_search`**({"query": "message queue"})

> 💭 **思考**：The search results show the relevant classes.

**🤖 Agent**：消息队列用的是 **`MessageQueue`**（定义于 `core/object/message_queue.cpp`），其底层依赖基类 **`CallQueue`**。

**📋 工具结果**：
```
- MessageQueue  (Users-ks_128-Documents-godot-src-core.object.message_queue.MessageQueue.MessageQueue)  object/message_queue.cpp
- ~MessageQueue  (Users-ks_128-Documents-godot-src-core.object.message_queue.MessageQueue.~MessageQueue)  object/message_queue.cpp
- CallQueue  (Users-ks_128-Documents-godot-src-core.object.message_queue.CallQueue.CallQueue)  object/message_queue.cpp
- ~CallQueue  (Users-ks_128-Documents-godot-src-core.object.message_queue.CallQueue.~CallQueue)  object/message_queue.cpp
- flush  (Users-ks_128-Documents-godot-src-core.object.message_queue.CallQueue.flush)  object/mess
```


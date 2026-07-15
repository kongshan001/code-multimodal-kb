# q17 · code_retrieval · arm: `kb+openspec`

**题**：消息队列用哪个类？  ·  **gold**：MessageQueue
**答对**：✓  ·  **答案**：`MessageQueue`（单例），底层由 `CallQueue` 实现。位于 `core/object/message_queue.cpp`。
**指标**：tokens=1312 · llm_calls=2 · tool_steps=1 · 耗时=12.12s · 截断=否

---

**👤 用户**：消息队列用哪个类？

> 💭 **思考**：用户问的是消息队列相关的类。这在 Godot 4.7 的上下文中，我搜索一下。

**🔧 `cmm_search`**({"query": "message queue"})

**🤖 Agent**：`MessageQueue`（单例），底层由 `CallQueue` 实现。位于 `core/object/message_queue.cpp`。

**📋 工具结果**：
```
- MessageQueue  (Users-ks_128-Documents-godot-src-core.object.message_queue.MessageQueue.MessageQueue)  object/message_queue.cpp
- ~MessageQueue  (Users-ks_128-Documents-godot-src-core.object.message_queue.MessageQueue.~MessageQueue)  object/message_queue.cpp
- CallQueue  (Users-ks_128-Documents-godot-src-core.object.message_queue.CallQueue.CallQueue)  object/message_queue.cpp
- ~CallQueue  (Users-ks_128-Documents-godot-src-core.object.message_queue.CallQueue.~CallQueue)  object/message_queue.cpp
- flush  (Users-ks_128-Documents-godot-src-core.object.message_queue.CallQueue.flush)  object/mess
```


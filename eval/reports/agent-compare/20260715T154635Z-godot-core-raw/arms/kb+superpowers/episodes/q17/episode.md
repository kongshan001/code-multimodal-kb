# q17 · code_retrieval · arm: `kb+superpowers`

**题**：消息队列用哪个类？  ·  **gold**：MessageQueue
**答对**：✓  ·  **答案**：消息队列用 **`MessageQueue`**（定义在 `core/object/message_queue.cpp`），它继承自 **`CallQueue`**。

- `MessageQueue` — 单例，对外使用的消息队列类。
-
**指标**：tokens=1288 · llm_calls=2 · tool_steps=1 · 耗时=9.34s · 截断=否

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

**🤖 Agent**：消息队列用 **`MessageQueue`**（定义在 `core/object/message_queue.cpp`），它继承自 **`CallQueue`**。

- `MessageQueue` — 单例，对外使用的消息队列类。
- `CallQueue` — 底层实现，提供 `flush()` 等方法。


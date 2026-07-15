# q17 · code_retrieval · arm: `kb`

**题**：消息队列用哪个类？  ·  **gold**：MessageQueue
**答对**：✓  ·  **答案**：用 `MessageQueue`（定义在 `core/object/message_queue.cpp`，继承自 `CallQueue`）。

- `MessageQueue` — 主类，单例，负责延迟调用（`call_deferred`）
**指标**：tokens=1071 · llm_calls=2 · tool_steps=1 · 耗时=16.28s · 截断=否

---

**👤 用户**：消息队列用哪个类？

> 💭 **思考**：The user is asking about which class is used for message queues in Godot core/. Let me search for it.

**🔧 `cmm_search`**({"query": "message queue"})

> 💭 **思考**：Clear answer.

**🤖 Agent**：用 `MessageQueue`（定义在 `core/object/message_queue.cpp`，继承自 `CallQueue`）。

- `MessageQueue` — 主类，单例，负责延迟调用（`call_deferred`）的消息队列。
- `CallQueue` — 基类，提供队列的底层逻辑（如 `push_call`、`flush`、`pop_front` 等）。

**📋 工具结果**：
```
- MessageQueue  (Users-ks_128-Documents-godot-src-core.object.message_queue.MessageQueue.MessageQueue)  object/message_queue.cpp
- ~MessageQueue  (Users-ks_128-Documents-godot-src-core.object.message_queue.MessageQueue.~MessageQueue)  object/message_queue.cpp
- CallQueue  (Users-ks_128-Documents-godot-src-core.object.message_queue.CallQueue.CallQueue)  object/message_queue.cpp
- ~CallQueue  (Users-ks_128-Documents-godot-src-core.object.message_queue.CallQueue.~CallQueue)  object/message_queue.cpp
- flush  (Users-ks_128-Documents-godot-src-core.object.message_queue.CallQueue.flush)  object/mess
```


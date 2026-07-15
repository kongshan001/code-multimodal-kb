# q17 · code_retrieval · arm: `kb+openspec`

**题**：消息队列用哪个类？  ·  **gold**：MessageQueue
**答对**：✓  ·  **答案**：`MessageQueue`（`core/object/message_queue.cpp`）。内部还用了 `CallQueue`。
**指标**：tokens=977 · llm_calls=2 · tool_steps=1 · 耗时=21.02s · 截断=否

---

**👤 用户**：消息队列用哪个类？

> 💭 **思考**：用户问的是 Godot 中消息队列用哪个类。让我搜索一下。

**🔧 `cmm_search`**({"query": "message queue"})

> 💭 **思考**：Found it.

**🤖 Agent**：`MessageQueue`（`core/object/message_queue.cpp`）。内部还用了 `CallQueue`。

**📋 工具结果**：
```
- MessageQueue  (Users-ks_128-Documents-godot-src-core.object.message_queue.MessageQueue.MessageQueue)  object/message_queue.cpp
- ~MessageQueue  (Users-ks_128-Documents-godot-src-core.object.message_queue.MessageQueue.~MessageQueue)  object/message_queue.cpp
- CallQueue  (Users-ks_128-Documents-godot-src-core.object.message_queue.CallQueue.CallQueue)  object/message_queue.cpp
- ~CallQueue  (Users-ks_128-Documents-godot-src-core.object.message_queue.CallQueue.~CallQueue)  object/message_queue.cpp
- flush  (Users-ks_128-Documents-godot-src-core.object.message_queue.CallQueue.flush)  object/mess
```


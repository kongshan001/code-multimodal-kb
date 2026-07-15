# q17 · code_retrieval · arm: `no-kb`

**题**：消息队列用哪个类？  ·  **gold**：MessageQueue
**答对**：✓  ·  **答案**：`MessageQueue`（定义在 `core/object/message_queue.h`）。
**指标**：tokens=848 · llm_calls=2 · tool_steps=1 · 耗时=8.59s · 截断=否

---

**👤 用户**：消息队列用哪个类？

> 💭 **思考**：The user is asking about which class is used for message queues in the Godot codebase.

**🔧 `grep_code`**({"pattern": "class MessageQueue"})

> 💭 **思考**：Found it.

**🤖 Agent**：`MessageQueue`（定义在 `core/object/message_queue.h`）。

**📋 工具结果**：
```
matched 1 files:
/Users/ks_128/Documents/godot-src/core/object/message_queue.h
```


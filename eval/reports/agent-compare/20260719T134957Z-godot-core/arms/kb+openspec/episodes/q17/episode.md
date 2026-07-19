# q17 · code_retrieval · arm: `kb+openspec`

- **题**：消息队列用哪个类？
- **gold**：MessageQueue
- **答对**：✓
- **答案**：`MessageQueue`
- **指标**：tokens=2550 · llm_calls=2 · tool_steps=1 · 耗时=8.66s · 截断=否

---

**👤 用户**：消息队列用哪个类？

> 💭 **思考**：用户问"消息队列用哪个类？"，这是在问 Godot 代码库中用于消息队列的类。

我需要使用 cmm_search 工具来搜索相关的符号。让我搜索"消息队列"或"message queue"相关的类。

根据指令，我需要简短回答，用符号名作答，不要长解释。一旦工具返回相关符号就立刻作答。

让我搜索一下：

**🔧 `cmm_search`**({"query": "消息队列 message queue"})

> 💭 **思考**：搜索结果返回了两个相关类：
1. MessageQueue
2. CallQueue

根据问题"消息队列用哪个类？"，最直接的答案应该是 `MessageQueue`。

根据收敛纪律，一旦工具返回了相关符号就立刻用符号名作答，不要反复查。

**🤖 Agent**：`MessageQueue`

**📋 工具结果**：
```
- MessageQueue  (Users-ks_128-Documents-godot-src-core.object.message_queue.MessageQueue.MessageQueue)  object/message_queue.cpp
- ~MessageQueue  (Users-ks_128-Documents-godot-src-core.object.message_queue.MessageQueue.~MessageQueue)  object/message_queue.cpp
- CallQueue  (Users-ks_128-Documents-godot-src-core.object.message_queue.CallQueue.CallQueue)  object/message_queue.cpp
- ~CallQueue  (Users-ks_128-Documents-godot-src-core.object.message_queue.CallQueue.~CallQueue)  object/message_queue.cpp
- flush  (Users-ks_128-Documents-godot-src-core.object.message_queue.CallQueue.flush)  object/mess
```


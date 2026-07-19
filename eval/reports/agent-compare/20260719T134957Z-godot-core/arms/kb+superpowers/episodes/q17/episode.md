# q17 · code_retrieval · arm: `kb+superpowers`

- **题**：消息队列用哪个类？
- **gold**：MessageQueue
- **答对**：✓
- **答案**：`MessageQueue`
- **指标**：tokens=2587 · llm_calls=2 · tool_steps=1 · 耗时=8.97s · 截断=否

---

**👤 用户**：消息队列用哪个类？

> 💭 **思考**：用户在询问 Godot 代码库中消息队列用哪个类。我需要用代码知识库语义检索来找到相关的类。

我应该搜索 "message queue" 或 "消息队列" 相关的内容。

**🔧 `cmm_search`**({"query": "message queue"})

> 💭 **思考**：搜索结果显示有两个相关类：
1. MessageQueue - 在 object/message_queue.cpp
2. CallQueue - 在 object/message_queue.cpp

根据搜索结果，用户问的是"消息队列用哪个类"，最直接的答案应该是 `MessageQueue` 类。

按照指令，我应该直接给符号名作答，不需要长解释。收敛纪律：一旦工具返回了相关符号就立刻用符号名作答。

**🤖 Agent**：`MessageQueue`

**📋 工具结果**：
```
- MessageQueue  (Users-ks_128-Documents-godot-src-core.object.message_queue.MessageQueue.MessageQueue)  object/message_queue.cpp
- ~MessageQueue  (Users-ks_128-Documents-godot-src-core.object.message_queue.MessageQueue.~MessageQueue)  object/message_queue.cpp
- CallQueue  (Users-ks_128-Documents-godot-src-core.object.message_queue.CallQueue.CallQueue)  object/message_queue.cpp
- ~CallQueue  (Users-ks_128-Documents-godot-src-core.object.message_queue.CallQueue.~CallQueue)  object/message_queue.cpp
- flush  (Users-ks_128-Documents-godot-src-core.object.message_queue.CallQueue.flush)  object/mess
```


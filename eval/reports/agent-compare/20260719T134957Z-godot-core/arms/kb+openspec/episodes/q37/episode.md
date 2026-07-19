# q37 · code_retrieval · arm: `kb+openspec`

- **题**：Godot core 里定长环形缓冲区（先进先出、写满覆盖最旧）的容器类叫什么？
- **gold**：RingBuffer
- **答对**：✓
- **答案**：`RingBuffer`
- **指标**：tokens=2574 · llm_calls=2 · tool_steps=1 · 耗时=5.34s · 截断=否

---

**👤 用户**：Godot core 里定长环形缓冲区（先进先出、写满覆盖最旧）的容器类叫什么？

> 💭 **思考**：用户在找 Godot core 里的定长环形缓冲区（先进先出、写满覆盖最旧）的容器类名。

我需要用语义搜索工具来查找相关的类。可能的关键词：
- 环形缓冲区
- circular buffer
- ring buffer
- FIFO
- 先进先出

让我先搜索一下相关的符号。

**🔧 `cmm_search`**({"query": "circular buffer ring FIFO"})

> 💭 **思考**：搜索结果直接返回了 RingBuffer 类，这应该就是用户在找的定长环形缓冲区容器类。根据工具返回的结果，位于 templates/ring_buffer.h。

按照指示，我需要直接用符号名作答，不要长解释。查到即答。

**🤖 Agent**：`RingBuffer`

**📋 工具结果**：
```
- RingBuffer  (Users-ks_128-Documents-godot-src-core.templates.ring_buffer.RingBuffer.RingBuffer)  templates/ring_buffer.h
- inc  (Users-ks_128-Documents-godot-src-core.templates.ring_buffer.RingBuffer.inc)  templates/ring_buffer.h
- read  (Users-ks_128-Documents-godot-src-core.templates.ring_buffer.RingBuffer.read)  templates/ring_buffer.h
- copy  (Users-ks_128-Documents-godot-src-core.templates.ring_buffer.RingBuffer.copy)  templates/ring_buffer.h
- find  (Users-ks_128-Documents-godot-src-core.templates.ring_buffer.RingBuffer.find)  templates/ring_buffer.h
```


# q37 · code_retrieval · arm: `kb`

- **题**：Godot core 里定长环形缓冲区（先进先出、写满覆盖最旧）的容器类叫什么？
- **gold**：RingBuffer
- **答对**：✓
- **答案**：`RingBuffer`
- **指标**：tokens=2033 · llm_calls=2 · tool_steps=1 · 耗时=8.04s · 截断=否

---

**👤 用户**：Godot core 里定长环形缓冲区（先进先出、写满覆盖最旧）的容器类叫什么？

> 💭 **思考**：用户在询问 Godot core 里定长环形缓冲区（FIFO、写满时覆盖最旧数据）的容器类名称。

我需要在 Godot core 代码库中搜索相关的环形缓冲区实现。可能的名称包括：
- RingBuffer
- CircularBuffer
- FIFO
- Queue
- 其他类似名称

让我先搜索一下。

**🔧 `cmm_search`**({"query": "ring buffer circular buffer FIFO"})

> 💭 **思考**：太好了！找到了！Godot core 里确实有一个 `RingBuffer` 类，位于 `templates/ring_buffer.h`。

这正是用户在问的定长环形缓冲区容器类。根据搜索结果，它有 read、copy、find 等方法，符合环形缓冲区的功能。

根据收敛纪律，我应该立即用符号名作答，不要反复查或长解释。

**🤖 Agent**：`RingBuffer`

**📋 工具结果**：
```
- RingBuffer  (Users-ks_128-Documents-godot-src-core.templates.ring_buffer.RingBuffer.RingBuffer)  templates/ring_buffer.h
- inc  (Users-ks_128-Documents-godot-src-core.templates.ring_buffer.RingBuffer.inc)  templates/ring_buffer.h
- read  (Users-ks_128-Documents-godot-src-core.templates.ring_buffer.RingBuffer.read)  templates/ring_buffer.h
- copy  (Users-ks_128-Documents-godot-src-core.templates.ring_buffer.RingBuffer.copy)  templates/ring_buffer.h
- find  (Users-ks_128-Documents-godot-src-core.templates.ring_buffer.RingBuffer.find)  templates/ring_buffer.h
```


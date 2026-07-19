# q37 · code_retrieval · arm: `kb+superpowers`

- **题**：Godot core 里定长环形缓冲区（先进先出、写满覆盖最旧）的容器类叫什么？
- **gold**：RingBuffer
- **答对**：✓
- **答案**：`RingBuffer`
- **指标**：tokens=2703 · llm_calls=2 · tool_steps=1 · 耗时=7.36s · 截断=否

---

**👤 用户**：Godot core 里定长环形缓冲区（先进先出、写满覆盖最旧）的容器类叫什么？

> 💭 **思考**：用户在问 Godot core 里的定长环形缓冲区容器类名。这是一个特定功能的容器类，具有以下特点：
1. 定长
2. 环形缓冲区
3. 先进先出
4. 写满时覆盖最旧的数据

我需要在 Godot core 代码库中搜索这个类。常见的环形缓冲区命名可能是：
- RingBuffer
- CircularBuffer
- FIFO
- Queue（但通常是动态的）

让我搜索一下。

**🔧 `cmm_search`**({"query": "ring buffer circular FIFO"})

> 💭 **思考**：搜索到了！确实是 `RingBuffer` 类，位于 `templates/ring_buffer.h`。这应该就是用户要找的定长环形缓冲区容器类。

**🤖 Agent**：`RingBuffer`

**📋 工具结果**：
```
- RingBuffer  (Users-ks_128-Documents-godot-src-core.templates.ring_buffer.RingBuffer.RingBuffer)  templates/ring_buffer.h
- inc  (Users-ks_128-Documents-godot-src-core.templates.ring_buffer.RingBuffer.inc)  templates/ring_buffer.h
- read  (Users-ks_128-Documents-godot-src-core.templates.ring_buffer.RingBuffer.read)  templates/ring_buffer.h
- copy  (Users-ks_128-Documents-godot-src-core.templates.ring_buffer.RingBuffer.copy)  templates/ring_buffer.h
- find  (Users-ks_128-Documents-godot-src-core.templates.ring_buffer.RingBuffer.find)  templates/ring_buffer.h
```


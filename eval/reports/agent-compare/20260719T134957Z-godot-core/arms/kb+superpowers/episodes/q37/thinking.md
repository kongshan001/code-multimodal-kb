# thinking

用户在问 Godot core 里的定长环形缓冲区容器类名。这是一个特定功能的容器类，具有以下特点：
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

---

搜索到了！确实是 `RingBuffer` 类，位于 `templates/ring_buffer.h`。这应该就是用户要找的定长环形缓冲区容器类。

---

`RingBuffer`

# thinking

用户在询问 Godot core 里定长环形缓冲区（FIFO、写满时覆盖最旧数据）的容器类名称。

我需要在 Godot core 代码库中搜索相关的环形缓冲区实现。可能的名称包括：
- RingBuffer
- CircularBuffer
- FIFO
- Queue
- 其他类似名称

让我先搜索一下。

---

太好了！找到了！Godot core 里确实有一个 `RingBuffer` 类，位于 `templates/ring_buffer.h`。

这正是用户在问的定长环形缓冲区容器类。根据搜索结果，它有 read、copy、find 等方法，符合环形缓冲区的功能。

根据收敛纪律，我应该立即用符号名作答，不要反复查或长解释。

---

`RingBuffer`

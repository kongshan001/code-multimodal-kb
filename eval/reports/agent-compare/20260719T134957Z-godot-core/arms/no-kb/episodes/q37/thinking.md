# thinking

用户在问 Godot core 源码中定长环形缓冲区（FIFO、写满时覆盖最旧元素）的容器类名称。我需要在 Godot core/ 源码里搜索相关实现。

环形缓冲区的可能关键词：
- "ring"
- "circular"
- "buffer"
- "fifo"
- "queue"
- "fixed size"
- "circular buffer"

让我先搜索 "ring" 相关：

---

没有明显结果。让我搜索 "circular"：

---

"buffer" 可能是个好关键词：

---

让我换个角度，查找 "fifo"：

---

让我在核心模板库里搜索可能叫 "CircularBuffer" 或类似名称的类：

---

让我搜索更通用的 "RingBuffer"：

---

找到了！有 `/Users/ks_128/Documents/godot-src/core/templates/ring_buffer.h` 这个文件。让我查看这个文件：

---

路径可能需要完整路径。让我尝试：

---

好的，找到 `ring_buffer.h` 文件了。文件名就是 `ring_buffer.h`，所以类名应该是 `RingBuffer`。让我看一下开头部分确认类名：

---

确认了是 `RingBuffer` 类。让我直接用这个类名作答，不重复查询。

---

`RingBuffer`

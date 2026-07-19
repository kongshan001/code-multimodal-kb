# thinking

用户在询问 Godot core 代码库中关于内存池的类。这类通常用于批量分配固定大小对象，避免频繁 new/delete。

我需要搜索相关的内存池类。可能的关键词：
- memory pool
- allocator
- pool
- object pool

让我搜索一下。

---

搜索结果里出现了 `PagedAllocator`，这看起来是我们要找的类——按页分配、批量分配固定大小对象的内存池类。让我再确认一下这个类的具体信息。

---

让我用完整的路径再试试。

---

好的，`PagedAllocator` 确实是我们找的类。让我直接回答用户。

---

`PagedAllocator`

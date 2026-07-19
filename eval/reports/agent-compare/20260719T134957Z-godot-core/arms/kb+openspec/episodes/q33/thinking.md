# thinking

用户在询问 Godot core 里的内存池类，这个类是按页批量分配固定大小对象，避免频繁 new/delete 的。

这是一个代码库查询问题，我需要使用语义搜索工具来找到这个类。

让我搜索相关的关键词：内存池、页分配、批量分配、固定大小对象等。

---

找到了！答案就是 `PagedAllocator`。这正是用户询问的"按页批量分配固定大小对象、避免频繁 new/delete 的内存池类"。

根据搜索结果，这个类定义在 `templates/paged_allocator.h` 中，提供了 `PagedAllocator` 类及其相关方法（`free`、`_reset` 等）。

直接用符号名作答即可，无需长篇解释。

---

`PagedAllocator`

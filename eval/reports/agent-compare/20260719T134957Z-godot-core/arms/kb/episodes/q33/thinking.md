# thinking

用户在问 Godot core 里的内存池类，用于按页批量分配固定大小对象，避免频繁 new/delete。

我需要在 Godot core/ 代码库中搜索这个类。关键词可能是 "memory pool"、"page allocator"、"fixed size"、"pool" 等。

让我先用 cmm_search 搜索一下。

---

搜索结果中有一些相关的项，但没有直接看到我想要的内存池类。让我尝试更具体的关键词。

---

找到了！`PagedAllocator` 在 `templates/paged_allocator.h` 中。这应该就是按页批量分配固定大小对象的内存池类。让我确认一下。

---

文件路径可能不对，让我重新搜索。

---

根据搜索结果，`PagedAllocator` 就是用户要找的类。它位于 templates/paged_allocator.h，提供了按页分配、避免频繁 new/delete 的功能。

答案应该直接给符号名。

---

`PagedAllocator`

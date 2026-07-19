# q33 · code_retrieval · arm: `kb+openspec`

- **题**：Godot core 里按页批量分配固定大小对象、避免频繁 new/delete 的内存池类叫什么？
- **gold**：PagedAllocator
- **答对**：✓
- **答案**：`PagedAllocator`
- **指标**：tokens=2602 · llm_calls=2 · tool_steps=1 · 耗时=7.33s · 截断=否

---

**👤 用户**：Godot core 里按页批量分配固定大小对象、避免频繁 new/delete 的内存池类叫什么？

> 💭 **思考**：用户在询问 Godot core 里的内存池类，这个类是按页批量分配固定大小对象，避免频繁 new/delete 的。

这是一个代码库查询问题，我需要使用语义搜索工具来找到这个类。

让我搜索相关的关键词：内存池、页分配、批量分配、固定大小对象等。

**🔧 `cmm_search`**({"query": "内存池 页分配 批量分配 固定大小对象 pool allocator"})

> 💭 **思考**：找到了！答案就是 `PagedAllocator`。这正是用户询问的"按页批量分配固定大小对象、避免频繁 new/delete 的内存池类"。

根据搜索结果，这个类定义在 `templates/paged_allocator.h` 中，提供了 `PagedAllocator` 类及其相关方法（`free`、`_reset` 等）。

直接用符号名作答即可，无需长篇解释。

**🤖 Agent**：`PagedAllocator`

**📋 工具结果**：
```
- memdelete_allocator  (Users-ks_128-Documents-godot-src-core.os.memory.memdelete_allocator)  os/memory.h
- PagedAllocator  (Users-ks_128-Documents-godot-src-core.templates.paged_allocator.PagedAllocator.PagedAllocator)  templates/paged_allocator.h
- ~PagedAllocator  (Users-ks_128-Documents-godot-src-core.templates.paged_allocator.PagedAllocator.~PagedAllocator)  templates/paged_allocator.h
- free  (Users-ks_128-Documents-godot-src-core.templates.paged_allocator.PagedAllocator.free)  templates/paged_allocator.h
- _reset  (Users-ks_128-Documents-godot-src-core.templates.paged_allocator.PagedAll
```


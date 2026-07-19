# q33 · code_retrieval · arm: `kb`

- **题**：Godot core 里按页批量分配固定大小对象、避免频繁 new/delete 的内存池类叫什么？
- **gold**：PagedAllocator
- **答对**：✓
- **答案**：`PagedAllocator`
- **指标**：tokens=6340 · llm_calls=5 · tool_steps=4 · 耗时=10.55s · 截断=否

---

**👤 用户**：Godot core 里按页批量分配固定大小对象、避免频繁 new/delete 的内存池类叫什么？

> 💭 **思考**：用户在问 Godot core 里的内存池类，用于按页批量分配固定大小对象，避免频繁 new/delete。

我需要在 Godot core/ 代码库中搜索这个类。关键词可能是 "memory pool"、"page allocator"、"fixed size"、"pool" 等。

让我先用 cmm_search 搜索一下。

**🔧 `cmm_search`**({"query": "memory pool page allocator fixed size"})

> 💭 **思考**：搜索结果中有一些相关的项，但没有直接看到我想要的内存池类。让我尝试更具体的关键词。

**🔧 `cmm_search`**({"query": "PoolMemory pool allocator template"})

> 💭 **思考**：找到了！`PagedAllocator` 在 `templates/paged_allocator.h` 中。这应该就是按页批量分配固定大小对象的内存池类。让我确认一下。

**🔧 `read_file`**({"path": "templates/paged_allocator.h"})

> 💭 **思考**：文件路径可能不对，让我重新搜索。

**🔧 `cmm_search`**({"query": "PagedAllocator class"})

> 💭 **思考**：根据搜索结果，`PagedAllocator` 就是用户要找的类。它位于 templates/paged_allocator.h，提供了按页分配、避免频繁 new/delete 的功能。

答案应该直接给符号名。

**🤖 Agent**：`PagedAllocator`

**📋 工具结果**：
```
- memdelete_allocator  (Users-ks_128-Documents-godot-src-core.os.memory.memdelete_allocator)  os/memory.h
- size  (Users-ks_128-Documents-godot-src-core.templates.fixed_vector.FixedVector.size)  templates/fixed_vector.h
- set_page_pool  (Users-ks_128-Documents-godot-src-core.templates.paged_array.PagedArray.set_page_pool)  templates/paged_array.h
- set_page_pool  (Users-ks_128-Documents-godot-src-core.templates.bin_sorted_array.BinSortedArray.set_page_pool)  templates/bin_sorted_array.h
- get_page_size_shift  (Users-ks_128-Documents-godot-src-core.templates.paged_array.PagedArrayPool.get_page_
```

**📋 工具结果**：
```
- ~BaseTemplateUserdata  (Users-ks_128-Documents-godot-src-core.object.worker_thread_pool.WorkerThreadPool.BaseTemplateUserdata.~BaseTemplateUserdata)  object/worker_thread_pool.h
- make_template  (Users-ks_128-Documents-godot-src-core.object.script_language.ScriptLanguage.make_template)  object/script_language.h
- memnew_arr_template  (Users-ks_128-Documents-godot-src-core.os.memory.memnew_arr_template)  os/memory.h
- memdelete_allocator  (Users-ks_128-Documents-godot-src-core.os.memory.memdelete_allocator)  os/memory.h
- PagedAllocator  (Users-ks_128-Documents-godot-src-core.templates.paged_
```

**📋 工具结果**：
```
(read error: [Errno 2] No such file or directory: 'templates/paged_allocator.h')
```

**📋 工具结果**：
```
- PagedAllocator  (Users-ks_128-Documents-godot-src-core.templates.paged_allocator.PagedAllocator.PagedAllocator)  templates/paged_allocator.h
- ~PagedAllocator  (Users-ks_128-Documents-godot-src-core.templates.paged_allocator.PagedAllocator.~PagedAllocator)  templates/paged_allocator.h
- free  (Users-ks_128-Documents-godot-src-core.templates.paged_allocator.PagedAllocator.free)  templates/paged_allocator.h
- _reset  (Users-ks_128-Documents-godot-src-core.templates.paged_allocator.PagedAllocator._reset)  templates/paged_allocator.h
- reset  (Users-ks_128-Documents-godot-src-core.templates.page
```


# q03 · code_retrieval · arm: `kb`

**题**：删除对象、释放内存用哪个函数？  ·  **gold**：memdelete
**答对**：✓  ·  **答案**：在 Godot C++ 代码库中，删除对象/释放内存主要用以下函数（均在 `os/memory.h` 中）：

| 用途 | 函数 |
|------|------|
| 删除 `memnew()` 创建的对象 | **`memdelete
**指标**：tokens=1570 · llm_calls=3 · tool_steps=2 · 耗时=18.44s · 截断=否

---

**👤 用户**：删除对象、释放内存用哪个函数？

> 💭 **思考**：The user is asking about which function is used to delete objects and free memory in Godot's C++ codebase. Let me search for this.

**🔧 `cmm_search`**({"query": "delete object free memory memfree"})

> 💭 **思考**：The user is asking about deleting objects and freeing memory. In Godot's C++ codebase, there are several relevant functions:

1. `memdelete()` - for deleting objects allocated with `memnew()`
2. `memfree()` - for freeing raw memory allocated with `memalloc()`
3. `Memory::free_static()` - static memo

**🔧 `cmm_search`**({"query": "memdelete Object memnew"})

**🤖 Agent**：在 Godot C++ 代码库中，删除对象/释放内存主要用以下函数（均在 `os/memory.h` 中）：

| 用途 | 函数 |
|------|------|
| 删除 `memnew()` 创建的对象 | **`memdelete()`** |
| 删除通过自定义 Allocator 创建的对象 | **`memdelete_allocator()`** |
| 删除 `memnew_arr()` 创建的数组 | **`memdelete_arr()`** |
| 释放 `memalloc()` 分配的裸内存 | **`memfree()`** |
| 释放静态分配内存 | **`M

**📋 工具结果**：
```
- operator delete  (Users-ks_128-Documents-godot-src-core.os.memory.operator delete)  os/memory.h
- delete_allocation  (Users-ks_128-Documents-godot-src-core.os.memory.DefaultTypedAllocator.delete_allocation)  os/memory.h
- free_static  (Users-ks_128-Documents-godot-src-core.os.memory.Memory.free_static)  os/memory.cpp
- free  (Users-ks_128-Documents-godot-src-core.os.memory.DefaultAllocator.free)  os/memory.h
- free_aligned_static  (Users-ks_128-Documents-godot-src-core.os.memory.Memory.free_aligned_static)  os/memory.cpp
```

**📋 工具结果**：
```
- memdelete  (Users-ks_128-Documents-godot-src-core.os.memory.memdelete)  os/memory.h
- memdelete_allocator  (Users-ks_128-Documents-godot-src-core.os.memory.memdelete_allocator)  os/memory.h
- memdelete_arr  (Users-ks_128-Documents-godot-src-core.os.memory.memdelete_arr)  os/memory.h
- memnew_arr_template  (Users-ks_128-Documents-godot-src-core.os.memory.memnew_arr_template)  os/memory.h
- memnew_arr_placement  (Users-ks_128-Documents-godot-src-core.os.memory.memnew_arr_placement)  os/memory.h
```


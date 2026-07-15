# q03 · code_retrieval · arm: `kb+superpowers`

**题**：删除对象、释放内存用哪个函数？  ·  **gold**：memdelete
**答对**：✓  ·  **答案**：在 Godot core 中，删除对象/释放内存主要用以下函数：

| 场景 | 函数 | 说明 |
|---|---|---|
| 删除单个对象（最常用） | **`memdelete`** | 对应 `memnew`，调用析构并释放内存
**指标**：tokens=2755 · llm_calls=3 · tool_steps=2 · 耗时=14.68s · 截断=否

---

**👤 用户**：删除对象、释放内存用哪个函数？

**🔧 `cmm_search`**({"query": "delete object free memory"})

**📋 工具结果**：
```
- operator delete  (Users-ks_128-Documents-godot-src-core.os.memory.operator delete)  os/memory.h
- delete_allocation  (Users-ks_128-Documents-godot-src-core.os.memory.DefaultTypedAllocator.delete_allocation)  os/memory.h
- free_static  (Users-ks_128-Documents-godot-src-core.os.memory.Memory.free_static)  os/memory.cpp
- free  (Users-ks_128-Documents-godot-src-core.os.memory.DefaultAllocator.free)  os/memory.h
- free_aligned_static  (Users-ks_128-Documents-godot-src-core.os.memory.Memory.free_aligned_static)  os/memory.cpp
```

**🔧 `cmm_search`**({"query": "Object free queue_delete memdelete"})

**📋 工具结果**：
```
- memdelete  (Users-ks_128-Documents-godot-src-core.os.memory.memdelete)  os/memory.h
- memdelete_allocator  (Users-ks_128-Documents-godot-src-core.os.memory.memdelete_allocator)  os/memory.h
- memdelete_arr  (Users-ks_128-Documents-godot-src-core.os.memory.memdelete_arr)  os/memory.h
- cancel_free  (Users-ks_128-Documents-godot-src-core.object.object.Object.cancel_free)  object/object.cpp
- free_instance_binding  (Users-ks_128-Documents-godot-src-core.object.object.Object.free_instance_binding)  object/object.cpp
```

**🤖 Agent**：在 Godot core 中，删除对象/释放内存主要用以下函数：

| 场景 | 函数 | 说明 |
|---|---|---|
| 删除单个对象（最常用） | **`memdelete`** | 对应 `memnew`，调用析构并释放内存 |
| 通过分配器删除 | **`memdelete_allocator`** | 配合特定 Allocator 使用 |
| 删除数组 | **`memdelete_arr`** | 对应 `memnew_arr` |
| 底层手动释放 | **`Memory::free_static`** | 直接释放 `memalloc` 的裸内存 |

**核心答


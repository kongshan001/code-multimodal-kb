# q03 · code_retrieval · arm: `kb`

**题**：删除对象、释放内存用哪个函数？  ·  **gold**：memdelete
**答对**：✓  ·  **答案**：在 Godot core 中，删除对象/释放内存主要用以下函数（定义于 `os/memory.h`）：

- **`memdelete`** — 最常用，删除通过 `memnew` 创建的对象。
- **`memdelete_allocat
**指标**：tokens=1220 · llm_calls=2 · tool_steps=2 · 耗时=10.34s · 截断=否

---

**👤 用户**：删除对象、释放内存用哪个函数？

**🔧 `cmm_search`**({"query": "delete object free memory"})

**🔧 `cmm_search`**({"query": "Object free memdelete"})

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
- cancel_free  (Users-ks_128-Documents-godot-src-core.object.object.Object.cancel_free)  object/object.cpp
- free_instance_binding  (Users-ks_128-Documents-godot-src-core.object.object.Object.free_instance_binding)  object/object.cpp
```

**🤖 Agent**：在 Godot core 中，删除对象/释放内存主要用以下函数（定义于 `os/memory.h`）：

- **`memdelete`** — 最常用，删除通过 `memnew` 创建的对象。
- **`memdelete_allocator`** — 删除通过自定义分配器（如 `memnew_allocator`）创建的对象。
- **`memdelete_arr`** — 删除通过 `memnew_arr` 创建的数组。
- **`Memory::free_static`** — 在静态上下文中释放内存（不依赖 `Memory` 单例）。
- **`operator delete`** 


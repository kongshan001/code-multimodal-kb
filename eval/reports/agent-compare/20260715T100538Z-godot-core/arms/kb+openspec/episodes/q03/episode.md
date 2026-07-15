# q03 · code_retrieval · arm: `kb+openspec`

**题**：删除对象、释放内存用哪个函数？  ·  **gold**：memdelete
**答对**：✓  ·  **答案**：在 Godot core 的 C++ 里，删除对象/释放内存主要用：

- **`memdelete(ptr)`** — 释放用 `memnew(T)` 分配的对象（`core/os/memory.h`）
- **`memfree(ptr)
**指标**：tokens=2147 · llm_calls=4 · tool_steps=3 · 耗时=20.66s · 截断=否

---

**👤 用户**：删除对象、释放内存用哪个函数？

> 💭 **思考**：The user is asking about which function is used to delete objects and free memory in Godot.

**🔧 `cmm_search`**({"query": "free object memory reference"})

> 💭 **思考**：The user asks about deleting objects and freeing memory. In Godot's C++ core, the key functions are:

1. `memfree()` — for freeing objects allocated with `memnew()`
2. `Object` has no built-in `free()` method in C++ (that's GDScript). In C++ you use `memfree()`.
3. `Reference` / `RefCounted` uses re

**🔧 `cmm_search`**({"query": "memfree memnew delete object"})

**🔧 `cmm_search`**({"query": "memfree memdelete free class object allocation"})

**🤖 Agent**：在 Godot core 的 C++ 里，删除对象/释放内存主要用：

- **`memdelete(ptr)`** — 释放用 `memnew(T)` 分配的对象（`core/os/memory.h`）
- **`memfree(ptr)`** — 释放用 `memalloc()` 分配的裸内存
- **`DefaultAllocator::free` / `DefaultTypedAllocator::delete_allocation`** — 底层分配器接口
- **`operator delete`** — 全局 `operator delete` 重载

典型配对：
- `memn

**📋 工具结果**：
```
- free_static  (Users-ks_128-Documents-godot-src-core.os.memory.Memory.free_static)  os/memory.cpp
- free  (Users-ks_128-Documents-godot-src-core.os.memory.DefaultAllocator.free)  os/memory.h
- free_aligned_static  (Users-ks_128-Documents-godot-src-core.os.memory.Memory.free_aligned_static)  os/memory.cpp
- _instance_binding_reference  (Users-ks_128-Documents-godot-src-core.object.object.Object._instance_binding_reference)  object/object.h
- reference  (Users-ks_128-Documents-godot-src-core.object.ref_counted.RefCounted.reference)  object/ref_counted.cpp
```

**📋 工具结果**：
```
- memnew_arr_template  (Users-ks_128-Documents-godot-src-core.os.memory.memnew_arr_template)  os/memory.h
- memnew_arr_placement  (Users-ks_128-Documents-godot-src-core.os.memory.memnew_arr_placement)  os/memory.h
- operator delete  (Users-ks_128-Documents-godot-src-core.os.memory.operator delete)  os/memory.h
- delete_allocation  (Users-ks_128-Documents-godot-src-core.os.memory.DefaultTypedAllocator.delete_allocation)  os/memory.h
- _delete_ctx  (Users-ks_128-Documents-godot-src-core.crypto.hashing_context.HashingContext._delete_ctx)  crypto/hashing_context.cpp
```

**📋 工具结果**：
```
- placeholder_class_free_instance  (Users-ks_128-Documents-godot-src-core.object.class_db.PlaceholderExtensionInstance.placeholder_class_free_instance)  object/class_db.cpp
- memdelete  (Users-ks_128-Documents-godot-src-core.os.memory.memdelete)  os/memory.h
- delete_allocation  (Users-ks_128-Documents-godot-src-core.os.memory.DefaultTypedAllocator.delete_allocation)  os/memory.h
- placeholder_instance_free_property_list  (Users-ks_128-Documents-godot-src-core.object.class_db.PlaceholderExtensionInstance.placeholder_instance_free_property_list)  object/class_db.cpp
- delete_allocation  (Users-
```


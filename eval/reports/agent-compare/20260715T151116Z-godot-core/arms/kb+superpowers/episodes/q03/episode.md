# q03 · code_retrieval · arm: `kb+superpowers`

**题**：删除对象、释放内存用哪个函数？  ·  **gold**：memdelete
**答对**：✓  ·  **答案**：在 Godot core 中，按层次：

| 函数 | 用途 |
|---|---|
| **`memdelete(ptr)`** | 删除 `memnew` 创建的对象，最常用（os/memory.h） |
| `memfree(ptr)
**指标**：tokens=1950 · llm_calls=3 · tool_steps=2 · 耗时=27.95s · 截断=否

---

**👤 用户**：删除对象、释放内存用哪个函数？

> 💭 **思考**：用户问的是在 Godot 中删除对象、释放内存用哪个函数。让我搜索一下。

**🔧 `cmm_search`**({"query": "delete object free memory"})

> 💭 **思考**：用户问的是删除对象、释放内存用哪个函数。在 Godot 中，有几种层次：

1. 低层内存分配/释放：`memdelete`、`memfree`、`Memory::free_static`
2. Object 生命周期：`Object::free()`、`queue_free()`

让我搜索 memdelete 和 Object 的 free 方法。

**🔧 `cmm_search`**({"query": "memdelete Object free instance"})

> 💭 **思考**：好的，现在我有足够的信息回答了。在 Godot 中：

- `memdelete()` — 删除用 `memnew` 创建的 C++ 对象，释放内存
- `Object::free()` — Object 层的释放方法
- `Node::queue_free()` — Node 延迟释放
- `memfree()` / `Memory::free_static()` — 低层内存释放

用户问的是"删除对象、释放内存"，核心函数是 `memdelete`。

**🤖 Agent**：在 Godot core 中，按层次：

| 函数 | 用途 |
|---|---|
| **`memdelete(ptr)`** | 删除 `memnew` 创建的对象，最常用（os/memory.h） |
| `memfree(ptr)` | 释放 `memalloc` 分配的原始内存 |
| `Memory::free_static()` | 静态释放（自定义 allocator 场景） |
| `Object::free()` | Object 层释放（Node 走 `queue_free()` 延迟到帧末） |

**核心答案**：C++ 层删对象用 **`memdelete`**。

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
- free_instance_binding  (Users-ks_128-Documents-godot-src-core.object.object.Object.free_instance_binding)  object/object.cpp
- gdextension_object_free_instance_binding  (Users-ks_128-Documents-godot-src-core.extension.gdextension_interface.gdextension_object_free_instance_binding)  extension/gdextension_interface.cpp
- placeholder_class_free_instance  (Users-ks_128-Documents-godot-src-core.object.class_db.PlaceholderExtensionInstance.placeholder_class_free_instance)  object/class_db.cpp
- placeholder_instance_free_property_list  (Users-ks_128-Documents-godot-src-core.object.class_db.Placehol
```


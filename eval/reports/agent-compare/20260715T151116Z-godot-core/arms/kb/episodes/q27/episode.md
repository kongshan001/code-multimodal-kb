# q27 · bug_fix · arm: `kb`

**题**：对象内存泄漏：某对象被释放后仍被引用（use-after-free）。Godot 里删除/释放对象的底层函数叫什么？  ·  **gold**：core/memory/memory.h, memdelete
**答对**：✓  ·  **答案**：Godot 里删除/释放对象涉及的核心函数：

- **`Object::free()`** — 对象自释放入口（派生类如 `Node::free()` 调用 `memdelete(this)`），面向对象的对外接口。
- **`memde
**指标**：tokens=2122 · llm_calls=6 · tool_steps=5 · 耗时=24.68s · 截断=否

---

**👤 用户**：对象内存泄漏：某对象被释放后仍被引用（use-after-free）。Godot 里删除/释放对象的底层函数叫什么？

> 💭 **思考**：The user is asking about the low-level function in Godot that deletes/frees objects. Let me search for this.

**🔧 `cmm_search`**({"query": "free object memory deallocation"})

**🔧 `cmm_search`**({"query": "Object free instance"})

> 💭 **思考**：Let me search more specifically for the `_free` or `free` method on Object that actually frees/destroys the object.

**🔧 `cmm_search`**({"query": "Object _free destroy cancel_free notification predelete"})

> 💭 **思考**：Let me find the actual `free()` method on Object class that is the core way to free an object.

**🔧 `read_file`**({"path": "core/object/object.cpp"})

**🔧 `cmm_search`**({"query": "Object::free memdelete NOTIFICATION_PREDELETE"})

> 💭 **思考**：Let me search for the `free()` method specifically on Object.

**🤖 Agent**：Godot 里删除/释放对象涉及的核心函数：

- **`Object::free()`** — 对象自释放入口（派生类如 `Node::free()` 调用 `memdelete(this)`），面向对象的对外接口。
- **`memdelete()`** (`os/memory.h`) — 真正的底层析构释放函数，对裸 `Object*` 调用即可，形如 `memdelete(obj);`。
- **`memdelete_allocator` / `memdelete_arr`** — 变体：按自定义 allocator 释放 / 释放数组。

释放流程中还会触发：
- **`Object

**📋 工具结果**：
```
- free_static  (Users-ks_128-Documents-godot-src-core.os.memory.Memory.free_static)  os/memory.cpp
- free  (Users-ks_128-Documents-godot-src-core.os.memory.DefaultAllocator.free)  os/memory.h
- free_aligned_static  (Users-ks_128-Documents-godot-src-core.os.memory.Memory.free_aligned_static)  os/memory.cpp
- cancel_free  (Users-ks_128-Documents-godot-src-core.object.object.Object.cancel_free)  object/object.cpp
- free_instance_binding  (Users-ks_128-Documents-godot-src-core.object.object.Object.free_instance_binding)  object/object.cpp
```

**📋 工具结果**：
```
- free_instance_binding  (Users-ks_128-Documents-godot-src-core.object.object.Object.free_instance_binding)  object/object.cpp
- gdextension_object_free_instance_binding  (Users-ks_128-Documents-godot-src-core.extension.gdextension_interface.gdextension_object_free_instance_binding)  extension/gdextension_interface.cpp
- placeholder_class_free_instance  (Users-ks_128-Documents-godot-src-core.object.class_db.PlaceholderExtensionInstance.placeholder_class_free_instance)  object/class_db.cpp
- placeholder_instance_free_property_list  (Users-ks_128-Documents-godot-src-core.object.class_db.Placehol
```

**📋 工具结果**：
```
- cancel_free  (Users-ks_128-Documents-godot-src-core.object.object.Object.cancel_free)  object/object.cpp
- _predelete  (Users-ks_128-Documents-godot-src-core.object.object.Object._predelete)  object/object.cpp
- predelete_handler  (Users-ks_128-Documents-godot-src-core.object.object.predelete_handler)  object/object.cpp
- gdextension_object_destroy  (Users-ks_128-Documents-godot-src-core.extension.gdextension_interface.gdextension_object_destroy)  extension/gdextension_interface.cpp
- _notification  (Users-ks_128-Documents-godot-src-core.object.object.Object._notification)  object/object.h
```

**📋 工具结果**：
```
(read error: [Errno 2] No such file or directory: 'core/object/object.cpp')
```

**📋 工具结果**：
```
- memdelete  (Users-ks_128-Documents-godot-src-core.os.memory.memdelete)  os/memory.h
- memdelete_allocator  (Users-ks_128-Documents-godot-src-core.os.memory.memdelete_allocator)  os/memory.h
- memdelete_arr  (Users-ks_128-Documents-godot-src-core.os.memory.memdelete_arr)  os/memory.h
- cancel_free  (Users-ks_128-Documents-godot-src-core.object.object.Object.cancel_free)  object/object.cpp
- free_instance_binding  (Users-ks_128-Documents-godot-src-core.object.object.Object.free_instance_binding)  object/object.cpp
```


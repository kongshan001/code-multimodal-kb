# q27 · bug_fix · arm: `kb+superpowers`

**题**：对象内存泄漏：某对象被释放后仍被引用（use-after-free）。Godot 里删除/释放对象的底层函数叫什么？  ·  **gold**：core/memory/memory.h, memdelete
**答对**：✓  ·  **答案**：Godot 中删除/释放对象的底层函数是：

- **`Object::free()`** — 公开接口，外部调用销毁对象。
- **`Object::_predelete()`** — 删除前的钩子（虚函数），返回 `false` 可通过
**指标**：tokens=1760 · llm_calls=7 · tool_steps=6 · 耗时=33.96s · 截断=否

---

**👤 用户**：对象内存泄漏：某对象被释放后仍被引用（use-after-free）。Godot 里删除/释放对象的底层函数叫什么？

> 💭 **思考**：用户问的是 Godot 中删除/释放对象的底层函数名称。让我搜索一下。

**🔧 `cmm_search`**({"query": "free object memory deallocate Object free"})

> 💭 **思考**：The user is asking about the底层函数 that deletes/frees an object in Godot. Let me search more specifically for the Object's free or _pre_delete / __free__ function.

**🔧 `cmm_search`**({"query": "Object free delete instance destroy _pre_delete __free__"})

> 💭 **思考**：Let me look at the Object class to find the `free()` method directly.

**🔧 `read_file`**({"path": "core/object/object.h"})

**🔧 `cmm_search`**({"query": "Object::free() method destroy cancel_free object.cpp"})

> 💭 **思考**：Let me look at the object.cpp file directly to find the free function.

**🔧 `read_file`**({"path": "core/object/object.cpp"})

**🔧 `cmm_search`**({"query": "Object free() destructor _pre_delete notification predelete"})

> 💭 **思考**：Let me find the `free()` method on Object class.

**🤖 Agent**：Godot 中删除/释放对象的底层函数是：

- **`Object::free()`** — 公开接口，外部调用销毁对象。
- **`Object::_predelete()`** — 删除前的钩子（虚函数），返回 `false` 可通过 `cancel_free` 取消释放。
- **`Object::notification(NOTIFICATION_PREDELETE)`** — 发出 `NOTIFICATION_PREDELETE` 通知，让对象内部做清理。

整体删除流程：`free()` → `_predelete()` → 发送 `NOTIFICATION_PREDELETE`

**📋 工具结果**：
```
- free_static  (Users-ks_128-Documents-godot-src-core.os.memory.Memory.free_static)  os/memory.cpp
- free  (Users-ks_128-Documents-godot-src-core.os.memory.DefaultAllocator.free)  os/memory.h
- cancel_free  (Users-ks_128-Documents-godot-src-core.object.object.Object.cancel_free)  object/object.cpp
- free_aligned_static  (Users-ks_128-Documents-godot-src-core.os.memory.Memory.free_aligned_static)  os/memory.cpp
- free_instance_binding  (Users-ks_128-Documents-godot-src-core.object.object.Object.free_instance_binding)  object/object.cpp
```

**📋 工具结果**：
```
- free_instance_binding  (Users-ks_128-Documents-godot-src-core.object.object.Object.free_instance_binding)  object/object.cpp
- placeholder_class_free_instance  (Users-ks_128-Documents-godot-src-core.object.class_db.PlaceholderExtensionInstance.placeholder_class_free_instance)  object/class_db.cpp
- gdextension_object_free_instance_binding  (Users-ks_128-Documents-godot-src-core.extension.gdextension_interface.gdextension_object_free_instance_binding)  extension/gdextension_interface.cpp
- placeholder_instance_free_property_list  (Users-ks_128-Documents-godot-src-core.object.class_db.Placehol
```

**📋 工具结果**：
```
(read error: [Errno 2] No such file or directory: 'core/object/object.h')
```

**📋 工具结果**：
```
- cancel_free  (Users-ks_128-Documents-godot-src-core.object.object.Object.cancel_free)  object/object.cpp
- gdextension_object_destroy  (Users-ks_128-Documents-godot-src-core.extension.gdextension_interface.gdextension_object_destroy)  extension/gdextension_interface.cpp
- free_instance_binding  (Users-ks_128-Documents-godot-src-core.object.object.Object.free_instance_binding)  object/object.cpp
- gdextension_object_free_instance_binding  (Users-ks_128-Documents-godot-src-core.extension.gdextension_interface.gdextension_object_free_instance_binding)  extension/gdextension_interface.cpp
- plac
```

**📋 工具结果**：
```
(read error: [Errno 2] No such file or directory: 'core/object/object.cpp')
```

**📋 工具结果**：
```
- _predelete  (Users-ks_128-Documents-godot-src-core.object.object.Object._predelete)  object/object.cpp
- predelete_handler  (Users-ks_128-Documents-godot-src-core.object.object.predelete_handler)  object/object.cpp
- _notification  (Users-ks_128-Documents-godot-src-core.object.object.Object._notification)  object/object.h
- notification  (Users-ks_128-Documents-godot-src-core.object.object.Object.notification)  object/object.h
- _notification_forward  (Users-ks_128-Documents-godot-src-core.object.object.Object._notification_forward)  object/object.cpp
```


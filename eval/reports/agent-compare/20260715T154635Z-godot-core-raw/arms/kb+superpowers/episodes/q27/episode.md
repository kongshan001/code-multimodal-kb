# q27 · bug_fix · arm: `kb+superpowers`

**题**：对象内存泄漏：某对象被释放后仍被引用（use-after-free）。Godot 里删除/释放对象的底层函数叫什么？  ·  **gold**：core/memory/memory.h, memdelete
**答对**：✓  ·  **答案**：Godot 中删除/释放对象涉及以下关键函数：

## 脚本层（GDScript / API 可见）

- **`Object.free()`** — 对象自身的释放方法，调用后触发 `NOTIFICATION_PREDELETE` 然后销
**指标**：tokens=2793 · llm_calls=3 · tool_steps=3 · 耗时=22.3s · 截断=否

---

**👤 用户**：对象内存泄漏：某对象被释放后仍被引用（use-after-free）。Godot 里删除/释放对象的底层函数叫什么？

**🔧 `cmm_search`**({"query": "free object memory deallocate instance"})

**🔧 `cmm_search`**({"query": "Object free memdelete"})

**📋 工具结果**：
```
- free_instance_binding  (Users-ks_128-Documents-godot-src-core.object.object.Object.free_instance_binding)  object/object.cpp
- gdextension_object_free_instance_binding  (Users-ks_128-Documents-godot-src-core.extension.gdextension_interface.gdextension_object_free_instance_binding)  extension/gdextension_interface.cpp
- placeholder_class_free_instance  (Users-ks_128-Documents-godot-src-core.object.class_db.PlaceholderExtensionInstance.placeholder_class_free_instance)  object/class_db.cpp
- placeholder_instance_free_property_list  (Users-ks_128-Documents-godot-src-core.object.class_db.Placehol
```

**📋 工具结果**：
```
- memdelete  (Users-ks_128-Documents-godot-src-core.os.memory.memdelete)  os/memory.h
- memdelete_allocator  (Users-ks_128-Documents-godot-src-core.os.memory.memdelete_allocator)  os/memory.h
- memdelete_arr  (Users-ks_128-Documents-godot-src-core.os.memory.memdelete_arr)  os/memory.h
- cancel_free  (Users-ks_128-Documents-godot-src-core.object.object.Object.cancel_free)  object/object.cpp
- free_instance_binding  (Users-ks_128-Documents-godot-src-core.object.object.Object.free_instance_binding)  object/object.cpp
```

**🔧 `cmm_search`**({"query": "Object free method notification predelete"})

**📋 工具结果**：
```
- _predelete  (Users-ks_128-Documents-godot-src-core.object.object.Object._predelete)  object/object.cpp
- predelete_handler  (Users-ks_128-Documents-godot-src-core.object.object.predelete_handler)  object/object.cpp
- _notification  (Users-ks_128-Documents-godot-src-core.object.object.Object._notification)  object/object.h
- notification  (Users-ks_128-Documents-godot-src-core.object.object.Object.notification)  object/object.h
- _notification_forward  (Users-ks_128-Documents-godot-src-core.object.object.Object._notification_forward)  object/object.cpp
```

**🤖 Agent**：Godot 中删除/释放对象涉及以下关键函数：

## 脚本层（GDScript / API 可见）

- **`Object.free()`** — 对象自身的释放方法，调用后触发 `NOTIFICATION_PREDELETE` 然后销毁对象。
- **`Object.queue_free()`** — 延迟释放，在当前帧/空闲时安全地调用 `free()`（常用于节点）。

## 底层 C++ 层

| 函数 | 位置 | 作用 |
|---|---|---|
| **`memdelete()`** | `os/memory.h` | 底层内存释放宏/模板，调用析构函数并释放内存（对应 


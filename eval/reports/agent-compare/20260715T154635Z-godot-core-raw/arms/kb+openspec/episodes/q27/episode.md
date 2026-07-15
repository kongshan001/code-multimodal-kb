# q27 · bug_fix · arm: `kb+openspec`

**题**：对象内存泄漏：某对象被释放后仍被引用（use-after-free）。Godot 里删除/释放对象的底层函数叫什么？  ·  **gold**：core/memory/memory.h, memdelete
**答对**：✓  ·  **答案**：Godot 中删除/释放对象的核心底层函数和机制如下：

## 关键符号

| 符号 | 所在文件 | 作用 |
|---|---|---|
| **`Object::free()`** | `object/object.cpp` | **
**指标**：tokens=4473 · llm_calls=11 · tool_steps=11 · 耗时=52.49s · 截断=否

---

**👤 用户**：对象内存泄漏：某对象被释放后仍被引用（use-after-free）。Godot 里删除/释放对象的底层函数叫什么？

**🔧 `cmm_search`**({"query": "free object memory deallocation"})

**🔧 `cmm_search`**({"query": "object deletion release instance"})

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
- is_queued_for_deletion  (Users-ks_128-Documents-godot-src-core.object.object.Object.is_queued_for_deletion)  object/object.cpp
- action_release  (Users-ks_128-Documents-godot-src-core.input.input.Input.action_release)  input/input.cpp
- release_pressed_events  (Users-ks_128-Documents-godot-src-core.input.input.Input.release_pressed_events)  input/input.cpp
- release_main_thread  (Users-ks_128-Documents-godot-src-core.os.thread.Thread.release_main_thread)  os/thread.h
- add_instance  (Users-ks_128-Documents-godot-src-core.object.object.ObjectDB.add_instance)  object/object.cpp
```

**🔧 `cmm_search`**({"query": "Object free method destroy delete"})

**📋 工具结果**：
```
- gdextension_object_destroy  (Users-ks_128-Documents-godot-src-core.extension.gdextension_interface.gdextension_object_destroy)  extension/gdextension_interface.cpp
- destroy  (Users-ks_128-Documents-godot-src-core.variant.variant.Variant.PackedArrayRefBase.destroy)  variant/variant.h
- cancel_free  (Users-ks_128-Documents-godot-src-core.object.object.Object.cancel_free)  object/object.cpp
- free_instance_binding  (Users-ks_128-Documents-godot-src-core.object.object.Object.free_instance_binding)  object/object.cpp
- gdextension_variant_destroy  (Users-ks_128-Documents-godot-src-core.extension
```

**🔧 `cmm_search`**({"query": "Object::free queue_delete _pre_delete"})

**📋 工具结果**：
```
- cancel_free  (Users-ks_128-Documents-godot-src-core.object.object.Object.cancel_free)  object/object.cpp
- free_instance_binding  (Users-ks_128-Documents-godot-src-core.object.object.Object.free_instance_binding)  object/object.cpp
- gdextension_object_free_instance_binding  (Users-ks_128-Documents-godot-src-core.extension.gdextension_interface.gdextension_object_free_instance_binding)  extension/gdextension_interface.cpp
- placeholder_class_free_instance  (Users-ks_128-Documents-godot-src-core.object.class_db.PlaceholderExtensionInstance.placeholder_class_free_instance)  object/class_db.cpp
```

**🔧 `read_file`**({"path": "core/object/object.h"})

**📋 工具结果**：
```
(read error: [Errno 2] No such file or directory: 'core/object/object.h')
```

**🔧 `cmm_search`**({"query": "Object free() method definition object.cpp"})

**📋 工具结果**：
```
- cancel_free  (Users-ks_128-Documents-godot-src-core.object.object.Object.cancel_free)  object/object.cpp
- free_instance_binding  (Users-ks_128-Documents-godot-src-core.object.object.Object.free_instance_binding)  object/object.cpp
- gdextension_object_free_instance_binding  (Users-ks_128-Documents-godot-src-core.extension.gdextension_interface.gdextension_object_free_instance_binding)  extension/gdextension_interface.cpp
- MethodDefinition  (Users-ks_128-Documents-godot-src-core.object.class_db.MethodDefinition.MethodDefinition)  object/class_db.h
- placeholder_class_free_instance  (Users-k
```

**🔧 `cmm_search`**({"query": "queue_free queue_delete Object deletion"})

**📋 工具结果**：
```
- is_queued_for_deletion  (Users-ks_128-Documents-godot-src-core.object.object.Object.is_queued_for_deletion)  object/object.cpp
- _is_queued_for_deletion  (Users-ks_128-Documents-godot-src-core.object.object.Object._is_queued_for_deletion)  object/object.h
- Object  (Users-ks_128-Documents-godot-src-core.object.object.Object.Object)  object/object.cpp
- ~Object  (Users-ks_128-Documents-godot-src-core.object.object.Object.~Object)  object/object.cpp
- _construct_object  (Users-ks_128-Documents-godot-src-core.object.object.Object._construct_object)  object/object.cpp
```

**🔧 `cmm_search`**({"query": "Node queue_free free object release"})

**📋 工具结果**：
```
- node_free_node_and_leaf  (Users-ks_128-Documents-godot-src-core.math.bvh_tree.BVH_Tree.node_free_node_and_leaf)  math/bvh_tree.h
- action_release  (Users-ks_128-Documents-godot-src-core.input.input.Input.action_release)  input/input.cpp
- cancel_free  (Users-ks_128-Documents-godot-src-core.object.object.Object.cancel_free)  object/object.cpp
- release_pressed_events  (Users-ks_128-Documents-godot-src-core.input.input.Input.release_pressed_events)  input/input.cpp
- release_main_thread  (Users-ks_128-Documents-godot-src-core.os.thread.Thread.release_main_thread)  os/thread.h
```

**🔧 `read_file`**({"path": "Users-ks_128-Documents-godot-src-core.object.object.object"})

**📋 工具结果**：
```
(read error: [Errno 2] No such file or directory: 'Users-ks_128-Documents-godot-src-core.object.object.object')
```

**🔧 `cmm_search`**({"query": "Object::free() void free object.cpp cancel_free"})

**📋 工具结果**：
```
- cancel_free  (Users-ks_128-Documents-godot-src-core.object.object.Object.cancel_free)  object/object.cpp
- free_instance_binding  (Users-ks_128-Documents-godot-src-core.object.object.Object.free_instance_binding)  object/object.cpp
- gdextension_object_free_instance_binding  (Users-ks_128-Documents-godot-src-core.extension.gdextension_interface.gdextension_object_free_instance_binding)  extension/gdextension_interface.cpp
- placeholder_class_free_instance  (Users-ks_128-Documents-godot-src-core.object.class_db.PlaceholderExtensionInstance.placeholder_class_free_instance)  object/class_db.cpp
```

**🔧 `cmm_search`**({"query": "_pre_delete _notification NOTIFICATION_PREDELETE Object destroy"})

**📋 工具结果**：
```
- gdextension_object_destroy  (Users-ks_128-Documents-godot-src-core.extension.gdextension_interface.gdextension_object_destroy)  extension/gdextension_interface.cpp
- _notification  (Users-ks_128-Documents-godot-src-core.object.object.Object._notification)  object/object.h
- notification  (Users-ks_128-Documents-godot-src-core.object.object.Object.notification)  object/object.h
- _notification_forward  (Users-ks_128-Documents-godot-src-core.object.object.Object._notification_forward)  object/object.cpp
- _notification_backward  (Users-ks_128-Documents-godot-src-core.object.object.Object._noti
```

**🤖 Agent**：Godot 中删除/释放对象的核心底层函数和机制如下：

## 关键符号

| 符号 | 所在文件 | 作用 |
|---|---|---|
| **`Object::free()`** | `object/object.cpp` | **核心释放函数**，立即销毁对象（触发 `NOTIFICATION_PREDELETE`，然后 `memdelete`） |
| **`Object::queue_free()`** | `object/object.cpp` | 延迟释放，将对象排入删除队列，在帧末尾安全销毁 |
| **`Object::is_queued_for_deletion()`*


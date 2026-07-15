# q27 · bug_fix · arm: `kb+openspec`

**题**：对象内存泄漏：某对象被释放后仍被引用（use-after-free）。Godot 里删除/释放对象的底层函数叫什么？  ·  **gold**：core/memory/memory.h, memdelete
**答对**：✓  ·  **答案**：Godot 中删除/释放对象的底层核心函数和机制：

**面向对象层（Script/GDScript 调用）**
- `Object::free()` — 脚本侧释放对象的入口（`object/object.cpp`）
- `Object:
**指标**：tokens=2162 · llm_calls=4 · tool_steps=3 · 耗时=29.82s · 截断=否

---

**👤 用户**：对象内存泄漏：某对象被释放后仍被引用（use-after-free）。Godot 里删除/释放对象的底层函数叫什么？

> 💭 **思考**：The user is asking about the low-level function in Godot that deletes/frees objects. Let me search for this.

**🔧 `cmm_search`**({"query": "object free release delete"})

> 💭 **思考**：Let me search more specifically for the `free` method on Object.

**🔧 `cmm_search`**({"query": "Object::free call free delete object instance"})

> 💭 **思考**：Let me search for the actual `free` function on Object class, or `_predelete` / `_delete`.

**🔧 `cmm_search`**({"query": "Object _predelete destructor _delete memdelete instance"})

**🤖 Agent**：Godot 中删除/释放对象的底层核心函数和机制：

**面向对象层（Script/GDScript 调用）**
- `Object::free()` — 脚本侧释放对象的入口（`object/object.cpp`）
- `Object::cancel_free()` — 取消 free 流程

**底层释放（C++ 内核）**
- `memdelete()` — 内存释放宏/模板（`os/memory.h`），所有堆对象最终经此释放
- `memdelete_allocator()` / `memdelete_arr()` — 对应自定义分配器/数组版本
- `Object::_prede

**📋 工具结果**：
```
- action_release  (Users-ks_128-Documents-godot-src-core.input.input.Input.action_release)  input/input.cpp
- cancel_free  (Users-ks_128-Documents-godot-src-core.object.object.Object.cancel_free)  object/object.cpp
- release_pressed_events  (Users-ks_128-Documents-godot-src-core.input.input.Input.release_pressed_events)  input/input.cpp
- release_main_thread  (Users-ks_128-Documents-godot-src-core.os.thread.Thread.release_main_thread)  os/thread.h
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
- _predelete  (Users-ks_128-Documents-godot-src-core.object.object.Object._predelete)  object/object.cpp
- predelete_handler  (Users-ks_128-Documents-godot-src-core.object.object.predelete_handler)  object/object.cpp
- memdelete  (Users-ks_128-Documents-godot-src-core.os.memory.memdelete)  os/memory.h
- memdelete_allocator  (Users-ks_128-Documents-godot-src-core.os.memory.memdelete_allocator)  os/memory.h
- memdelete_arr  (Users-ks_128-Documents-godot-src-core.os.memory.memdelete_arr)  os/memory.h
```


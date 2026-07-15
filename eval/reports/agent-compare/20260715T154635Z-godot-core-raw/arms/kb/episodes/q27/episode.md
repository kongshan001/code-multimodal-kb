# q27 · bug_fix · arm: `kb`

**题**：对象内存泄漏：某对象被释放后仍被引用（use-after-free）。Godot 里删除/释放对象的底层函数叫什么？  ·  **gold**：core/memory/memory.h, memdelete
**答对**：✓  ·  **答案**：Godot 中删除/释放对象的核心底层函数和机制：

1. **`memdelete`**（`os/memory.h`）— 最底层的 C++ 内存释放函数，用于释放通过 `memnew` 分配的 `Object`。这是真正释放对象内存的地方
**指标**：tokens=1050 · llm_calls=2 · tool_steps=2 · 耗时=8.19s · 截断=否

---

**👤 用户**：对象内存泄漏：某对象被释放后仍被引用（use-after-free）。Godot 里删除/释放对象的底层函数叫什么？

**🔧 `cmm_search`**({"query": "object free delete memdelete instance"})

**🔧 `cmm_search`**({"query": "Object free release memory deallocate"})

**📋 工具结果**：
```
- free_instance_binding  (Users-ks_128-Documents-godot-src-core.object.object.Object.free_instance_binding)  object/object.cpp
- gdextension_object_free_instance_binding  (Users-ks_128-Documents-godot-src-core.extension.gdextension_interface.gdextension_object_free_instance_binding)  extension/gdextension_interface.cpp
- placeholder_class_free_instance  (Users-ks_128-Documents-godot-src-core.object.class_db.PlaceholderExtensionInstance.placeholder_class_free_instance)  object/class_db.cpp
- placeholder_instance_free_property_list  (Users-ks_128-Documents-godot-src-core.object.class_db.Placehol
```

**📋 工具结果**：
```
- free_static  (Users-ks_128-Documents-godot-src-core.os.memory.Memory.free_static)  os/memory.cpp
- free  (Users-ks_128-Documents-godot-src-core.os.memory.DefaultAllocator.free)  os/memory.h
- free_aligned_static  (Users-ks_128-Documents-godot-src-core.os.memory.Memory.free_aligned_static)  os/memory.cpp
- action_release  (Users-ks_128-Documents-godot-src-core.input.input.Input.action_release)  input/input.cpp
- cancel_free  (Users-ks_128-Documents-godot-src-core.object.object.Object.cancel_free)  object/object.cpp
```

**🤖 Agent**：Godot 中删除/释放对象的核心底层函数和机制：

1. **`memdelete`**（`os/memory.h`）— 最底层的 C++ 内存释放函数，用于释放通过 `memnew` 分配的 `Object`。这是真正释放对象内存的地方。

2. **`Object::_pre_delete()` / `Object::~Object()`**（`object/object.cpp`）— 析构前后的清理逻辑。

3. **`Object::cancel_free()`**（`object/object.cpp`）— 取消待执行的 free。

4. **`free_instance_bin


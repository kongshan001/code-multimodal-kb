# q27 · bug_fix · arm: `kb+openspec`

- **题**：对象内存泄漏：某对象被释放后仍被引用（use-after-free）。Godot 里删除/释放对象的底层函数叫什么？
- **gold**：core/memory/memory.h, memdelete
- **答对**：✗
- **答案**：`RefCounted::unreference`
- **指标**：tokens=10513 · llm_calls=6 · tool_steps=5 · 耗时=11.83s · 截断=否

---

**👤 用户**：对象内存泄漏：某对象被释放后仍被引用（use-after-free）。Godot 里删除/释放对象的底层函数叫什么？

> 💭 **思考**：用户问的是 Godot 中删除/释放对象的底层函数名。这是一个代码库问题，我需要搜索相关函数。

在 Godot 中，对象的删除和释放通常涉及引用计数。我需要搜索相关的函数名，比如 free、destroy、unreference、release 等关键词。

让我搜索一下相关的符号。

**🔧 `cmm_search`**({"query": "delete free destroy release object"})

> 💭 **思考**：从搜索结果看，有几个相关的函数：
- `gdextension_object_destroy` - 这是 GDExtension 接口的销毁对象函数
- `cancel_free` - 这是 Object 类的取消释放函数

让我再搜索一下更具体的对象释放相关的函数，比如 "unreference"、"free" 等。

**🔧 `cmm_search`**({"query": "unreference free Object Reference"})

> 💭 **思考**：好的，现在我看到了几个关键函数：
- `RefCounted::unreference` - 这是引用计数对象的取消引用函数
- `Object::cancel_free` - 这是取消释放的函数

但用户问的是"删除/释放对象的底层函数"。在 Godot 中，主要的对象释放机制是通过引用计数。当引用计数归零时，对象会被自动释放。

让我再搜索一下直接释放/销毁对象的函数。

**🔧 `cmm_search`**({"query": "queue_free free object destroy dispose"})

> 💭 **思考**：让我搜索 "queue_free"，这是一个很常见的 Godot 对象释放函数。

**🔧 `cmm_search`**({"query": "queue_free"})

> 💭 **思考**：奇怪，queue_free 没找到。让我再搜索一下其他的释放相关函数。

用户问的是"删除/释放对象的底层函数"。从搜索结果来看，最相关的是：
- `RefCounted::unreference` - 用于引用计数对象
- `Object::cancel_free` - 取消释放
- `gdextension_object_destroy` - GDExtension 接口的销毁函数

但让我再搜索一下更底层的释放机制。

**🔧 `cmm_search`**({"query": "RefCounted unreference"})

> 💭 **思考**：基于搜索结果，Godot 中对象释放的核心机制是通过引用计数。对于引用计数对象（`RefCounted`），底层的释放函数是：

`RefCounted::unreference`

当调用 `unreference()` 后，如果引用计数归零，对象会自动被释放/销毁。

对于普通对象（继承自 `Object`），也有相关的机制，但核心是引用计数。

用户问的是"删除/释放对象的底层函数"，答案应该是 `RefCounted::unreference`。

**🤖 Agent**：`RefCounted::unreference`

**📋 工具结果**：
```
- gdextension_object_destroy  (Users-ks_128-Documents-godot-src-core.extension.gdextension_interface.gdextension_object_destroy)  extension/gdextension_interface.cpp
- destroy  (Users-ks_128-Documents-godot-src-core.variant.variant.Variant.PackedArrayRefBase.destroy)  variant/variant.h
- action_release  (Users-ks_128-Documents-godot-src-core.input.input.Input.action_release)  input/input.cpp
- cancel_free  (Users-ks_128-Documents-godot-src-core.object.object.Object.cancel_free)  object/object.cpp
- release_pressed_events  (Users-ks_128-Documents-godot-src-core.input.input.Input.release_pressed
```

**📋 工具结果**：
```
- unreference  (Users-ks_128-Documents-godot-src-core.object.ref_counted.RefCounted.unreference)  object/ref_counted.cpp
- placeholder_instance_unreference  (Users-ks_128-Documents-godot-src-core.object.class_db.PlaceholderExtensionInstance.placeholder_instance_unreference)  object/class_db.cpp
- _instance_binding_reference  (Users-ks_128-Documents-godot-src-core.object.object.Object._instance_binding_reference)  object/object.h
- reference  (Users-ks_128-Documents-godot-src-core.object.ref_counted.RefCounted.reference)  object/ref_counted.cpp
- cancel_free  (Users-ks_128-Documents-godot-src-c
```

**📋 工具结果**：
```
- gdextension_object_destroy  (Users-ks_128-Documents-godot-src-core.extension.gdextension_interface.gdextension_object_destroy)  extension/gdextension_interface.cpp
- destroy  (Users-ks_128-Documents-godot-src-core.variant.variant.Variant.PackedArrayRefBase.destroy)  variant/variant.h
- cancel_free  (Users-ks_128-Documents-godot-src-core.object.object.Object.cancel_free)  object/object.cpp
- free_instance_binding  (Users-ks_128-Documents-godot-src-core.object.object.Object.free_instance_binding)  object/object.cpp
- gdextension_variant_destroy  (Users-ks_128-Documents-godot-src-core.extension
```

**📋 工具结果**：
```
(no results)
```

**📋 工具结果**：
```
- unreference  (Users-ks_128-Documents-godot-src-core.object.ref_counted.RefCounted.unreference)  object/ref_counted.cpp
- placeholder_instance_unreference  (Users-ks_128-Documents-godot-src-core.object.class_db.PlaceholderExtensionInstance.placeholder_instance_unreference)  object/class_db.cpp
- RefCounted  (Users-ks_128-Documents-godot-src-core.object.ref_counted.RefCounted.RefCounted)  object/ref_counted.cpp
- reference  (Users-ks_128-Documents-godot-src-core.object.ref_counted.RefCounted.reference)  object/ref_counted.cpp
- init_ref  (Users-ks_128-Documents-godot-src-core.object.ref_counte
```


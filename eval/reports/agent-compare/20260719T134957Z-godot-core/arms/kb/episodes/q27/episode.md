# q27 · bug_fix · arm: `kb`

- **题**：对象内存泄漏：某对象被释放后仍被引用（use-after-free）。Godot 里删除/释放对象的底层函数叫什么？
- **gold**：core/memory/memory.h, memdelete
- **答对**：✗
- **答案**：`gdextension_object_destroy`
- **指标**：tokens=8802 · llm_calls=6 · tool_steps=5 · 耗时=14.86s · 截断=否

---

**👤 用户**：对象内存泄漏：某对象被释放后仍被引用（use-after-free）。Godot 里删除/释放对象的底层函数叫什么？

> 💭 **思考**：用户问的是 Godot 里删除/释放对象的底层函数叫什么。这是关于 use-after-free 内存泄漏的问题，需要找到 Godot 中负责释放/删除对象的底层函数。

我需要用 cmm_search 来搜索相关的符号。让我尝试搜索一些关键词：
- "free", "delete", "destroy", "release"
- "object deletion"
- "memory management"

让我先搜索 "delete object" 或 "free object" 相关的函数。

**🔧 `cmm_search`**({"query": "delete object free destroy release"})

> 💭 **思考**：好，我找到了一些相关的函数。看起来 `gdextension_object_destroy` 是一个底层函数，用于销毁 GDExtension 对象。另外还有 `Object.cancel_free` 方法。

让我再搜索一下更具体的对象删除/释放机制，比如 "queue_free" 或 "free" 相关的方法：

**🔧 `cmm_search`**({"query": "queue_free free object delete"})

> 💭 **思考**：我看到了一些相关的符号：
- `operator delete` (os/memory.h)
- `gdextension_object_free_instance_binding`
- `free_instance_binding`

让我再搜索一下 Object 的主要释放方法：

**🔧 `cmm_search`**({"query": "Object free delete destructor destroy core"})

> 💭 **思考**：根据搜索结果，在 Godot 中删除/释放对象的底层函数主要是：

1. `gdextension_object_destroy` - 这是 GDExtension 接口中用于销毁对象的函数
2. `gdextension_variant_destroy` - 用于销毁 Variant 类型
3. `operator delete` - C++ 标准的删除操作符

看起来 `gdextension_object_destroy` 是 Godot 提供的主要对象销毁接口。让我再看一下这个函数的具体实现：

**🔧 `read_file`**({"path": "extension/gdextension_interface.cpp"})

> 💭 **思考**：看起来路径不对。让我重新搜索一下这个文件的具体路径：

**🔧 `cmm_search`**({"query": "gdextension_object_destroy implementation"})

> 💭 **思考**：我已经找到了相关的符号。根据搜索结果，Godot 里删除/释放对象的底层函数主要是：

1. **`gdextension_object_destroy`** - 这是 GDExtension 接口中销毁对象的主要函数
2. **`gdextension_variant_destroy`** - 用于销毁 Variant 对象

根据题目要求的"收敛纪律"，我应该直接用符号名作答，不要反复查找。从搜索结果来看，`gdextension_object_destroy` 是最直接的对象销毁函数。

**🤖 Agent**：`gdextension_object_destroy`

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
- cancel_free  (Users-ks_128-Documents-godot-src-core.object.object.Object.cancel_free)  object/object.cpp
- free_instance_binding  (Users-ks_128-Documents-godot-src-core.object.object.Object.free_instance_binding)  object/object.cpp
- gdextension_object_free_instance_binding  (Users-ks_128-Documents-godot-src-core.extension.gdextension_interface.gdextension_object_free_instance_binding)  extension/gdextension_interface.cpp
- operator delete  (Users-ks_128-Documents-godot-src-core.os.memory.operator delete)  os/memory.h
- placeholder_class_free_instance  (Users-ks_128-Documents-godot-src-core.
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
(read error: [Errno 2] No such file or directory: 'extension/gdextension_interface.cpp')
```

**📋 工具结果**：
```
- gdextension_object_destroy  (Users-ks_128-Documents-godot-src-core.extension.gdextension_interface.gdextension_object_destroy)  extension/gdextension_interface.cpp
```


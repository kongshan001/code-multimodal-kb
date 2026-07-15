# q27 · bug_fix · arm: `no-kb`

**题**：对象内存泄漏：某对象被释放后仍被引用（use-after-free）。Godot 里删除/释放对象的底层函数叫什么？  ·  **gold**：core/memory/memory.h, memdelete
**答对**：✓  ·  **答案**：Godot 中删除/释放对象的底层函数主要有：

- **`memdelete(ptr)`** — 最底层的宏（`core/os/memory.h`），配合 `memnew` 使用，对所有通过堆分配的 Godot 对象调用析构并释放内存。

**指标**：tokens=1873 · llm_calls=4 · tool_steps=3 · 耗时=26.7s · 截断=否

---

**👤 用户**：对象内存泄漏：某对象被释放后仍被引用（use-after-free）。Godot 里删除/释放对象的底层函数叫什么？

> 💭 **思考**：The user is asking about the low-level function in Godot for deleting/freeing objects. Let me search for this.

**🔧 `grep_code`**({"pattern": "void Object::free\\b"})

> 💭 **思考**：Let me search more broadly.

**🔧 `grep_code`**({"pattern": "::free\\(\\)"})

**🔧 `grep_code`**({"pattern": "memdelete"})

> 💭 **思考**：The user is asking about the low-level function for deleting/freeing objects in Godot. Key functions:

1. `Object::free()` - the public method on Object
2. `memdelete()` - the low-level macro/template in memory.h for freeing memory
3. There might also be `_predelete()` and `predelete_handler`

Let m

**🤖 Agent**：Godot 中删除/释放对象的底层函数主要有：

- **`memdelete(ptr)`** — 最底层的宏（`core/os/memory.h`），配合 `memnew` 使用，对所有通过堆分配的 Godot 对象调用析构并释放内存。
- **`Object::free()`** — `core/object/object.cpp` 中 `Object` 类的公开方法，脚本/GDScript 层调用的 `free()` 最终走到这里。
- **`Object::queue_free()`** — 延迟释放（一帧结束、SceneTree 空闲时执行）。
- **`Object::_prede

**📋 工具结果**：
```
(no matches)
```

**📋 工具结果**：
```
matched 14 files:
/Users/ks_128/Documents/godot-src/core/extension/gdextension_interface.cpp
/Users/ks_128/Documents/godot-src/core/io/logger.cpp
/Users/ks_128/Documents/godot-src/core/object/worker_thread_pool.cpp
/Users/ks_128/Documents/godot-src/core/object/object.cpp
/Users/ks_128/Documents/godot-src/core/variant/variant_pools.cpp
/Users/ks_128/Documents/godot-src/core/variant/variant.cpp
/Users/ks_128/Documents/godot-src/core/templates/hash_map.h
/Users/ks_128/Documents/godot-src/core/templates/cowdata.h
/Users/ks_128/Documents/godot-src/core/templates/a_hash_map.h
/Users/ks_128/Documents
```

**📋 工具结果**：
```
matched 20 files:
/Users/ks_128/Documents/godot-src/core/crypto/hashing_context.cpp
/Users/ks_128/Documents/godot-src/core/extension/gdextension_interface.cpp
/Users/ks_128/Documents/godot-src/core/extension/gdextension.cpp
/Users/ks_128/Documents/godot-src/core/io/udp_server.cpp
/Users/ks_128/Documents/godot-src/core/io/xml_parser.cpp
/Users/ks_128/Documents/godot-src/core/io/image.cpp
/Users/ks_128/Documents/godot-src/core/io/resource.cpp
/Users/ks_128/Documents/godot-src/core/io/file_access_memory.cpp
/Users/ks_128/Documents/godot-src/core/io/resource_loader.cpp
/Users/ks_128/Documents/godo
```


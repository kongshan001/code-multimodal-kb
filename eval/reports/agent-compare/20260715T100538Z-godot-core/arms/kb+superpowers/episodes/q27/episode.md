# q27 · bug_fix · arm: `kb+superpowers`

**题**：Object memory leak: an object is freed but a dangling reference is still held, causing a use-after-free. Where is the bug most likely fixed?  ·  **gold**：core/memory/memory.h, memdelete
**答对**：✗  ·  **答案**：The bug is most likely fixed by using **`Ref<T>`** (the reference-counting smart pointer in `core/object/ref_counted.h`)
**指标**：tokens=1002 · llm_calls=3 · tool_steps=2 · 耗时=27.76s · 截断=否

---

**👤 用户**：Object memory leak: an object is freed but a dangling reference is still held, causing a use-after-free. Where is the bug most likely fixed?

> 💭 **思考**：The user is asking about where a use-after-free / dangling reference bug related to object memory management would most likely be fixed in Godot's core. Let me search for relevant code.

**🔧 `cmm_search`**({"query": "object reference count use-after-free prevent dangling"})

**🔧 `cmm_search`**({"query": "Object free notification when object is freed"})

> 💭 **思考**：The user is asking about a use-after-free / dangling reference bug. In Godot, the mechanism that prevents dangling pointers is the `Ref<T>` smart pointer combined with `RefCounted` reference counting. The bug would most likely be fixed by using `Ref<T>` instead of a raw `T*` pointer, which keeps the

**🤖 Agent**：The bug is most likely fixed by using **`Ref<T>`** (the reference-counting smart pointer in `core/object/ref_counted.h`) instead of a raw `T*` pointer.

Key symbols:

- **`Ref<T>`** — smart pointer template that automatically increments/decrements the `RefCounted` reference count, preventing prematu

**📋 工具结果**：
```
- get_reference_count  (Users-ks_128-Documents-godot-src-core.object.ref_counted.RefCounted.get_reference_count)  object/ref_counted.cpp
- _prevent_sync_wraparound  (Users-ks_128-Documents-godot-src-core.templates.command_queue_mt.CommandQueueMT._prevent_sync_wraparound)  templates/command_queue_mt.h
- _instance_binding_reference  (Users-ks_128-Documents-godot-src-core.object.object.Object._instance_binding_reference)  object/object.h
- reference  (Users-ks_128-Documents-godot-src-core.object.ref_counted.RefCounted.reference)  object/ref_counted.cpp
- cancel_free  (Users-ks_128-Documents-godot
```

**📋 工具结果**：
```
- _notification  (Users-ks_128-Documents-godot-src-core.object.object.Object._notification)  object/object.h
- notification  (Users-ks_128-Documents-godot-src-core.object.object.Object.notification)  object/object.h
- _notification_forward  (Users-ks_128-Documents-godot-src-core.object.object.Object._notification_forward)  object/object.cpp
- _notification_backward  (Users-ks_128-Documents-godot-src-core.object.object.Object._notification_backward)  object/object.cpp
- _notification_forwardv  (Users-ks_128-Documents-godot-src-core.object.object.Object._notification_forwardv)  object/object.h
```


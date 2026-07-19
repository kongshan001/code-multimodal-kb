# q34 · code_retrieval · arm: `kb`

- **题**：Godot core 里用原子操作实现线程安全引用计数的类叫什么？
- **gold**：SafeRefCount
- **答对**：✓
- **答案**：`SafeRefCount`
- **指标**：tokens=7050 · llm_calls=6 · tool_steps=5 · 耗时=12.41s · 截断=否

---

**👤 用户**：Godot core 里用原子操作实现线程安全引用计数的类叫什么？

> 💭 **思考**：用户问 Godot core 里用原子操作实现线程安全引用计数的类叫什么。

我需要在 Godot 代码库中搜索这个相关的类。关键词应该是"atomic" "reference" "count" 或者 "refcount" 之类的。

让我搜索一下。

**🔧 `cmm_search`**({"query": "atomic reference count thread safe"})

> 💭 **思考**：这个结果没有直接给出具体的类名。让我换个搜索词，搜索"atomic" "ref"或者"SafeRefCount"之类的。

**🔧 `cmm_search`**({"query": "SafeAtomic"})

> 💭 **思考**：让我搜索"Atomic"相关的类。

**🔧 `cmm_search`**({"query": "Atomic"})

> 💭 **思考**：这很奇怪。让我换个方式，搜索"refcount"或者"ref_count"。

**🔧 `cmm_search`**({"query": "ref_count"})

> 💭 **思考**：很好！我找到了 `SafeRefCount` 类。这个类应该就是用原子操作实现线程安全引用计数的类。让我确认一下这个类的定义。

**🔧 `read_file`**({"path": "templates/safe_refcount.h"})

> 💭 **思考**：可能是路径不对，但我已经找到了答案。`SafeRefCount` 就是这个类名。根据搜索结果，它在 `templates/safe_refcount.h` 中定义。这应该就是用原子操作实现线程安全引用计数的类。

**🤖 Agent**：`SafeRefCount`

**📋 工具结果**：
```
- get_reference_count  (Users-ks_128-Documents-godot-src-core.object.ref_counted.RefCounted.get_reference_count)  object/ref_counted.cpp
- is_current_thread_safe_for_nodes  (Users-ks_128-Documents-godot-src-core.os.thread_safe.is_current_thread_safe_for_nodes)  os/thread_safe.cpp
- set_current_thread_safe_for_nodes  (Users-ks_128-Documents-godot-src-core.os.thread_safe.set_current_thread_safe_for_nodes)  os/thread_safe.cpp
- get_thread_count  (Users-ks_128-Documents-godot-src-core.object.worker_thread_pool.WorkerThreadPool.get_thread_count)  object/worker_thread_pool.h
- get_group_processed_el
```

**📋 工具结果**：
```
(no results)
```

**📋 工具结果**：
```
(no results)
```

**📋 工具结果**：
```
- SafeRefCount  (Users-ks_128-Documents-godot-src-core.templates.safe_refcount.SafeRefCount)  templates/safe_refcount.h
- ref_count  (Users-ks_128-Documents-godot-src-core.variant.callable.CallableCustom.ref_count)  variant/callable.h
- REF_COUNT_OFFSET  (Users-ks_128-Documents-godot-src-core.templates.cowdata.CowData.REF_COUNT_OFFSET)  templates/cowdata.h
```

**📋 工具结果**：
```
(read error: [Errno 2] No such file or directory: 'templates/safe_refcount.h')
```


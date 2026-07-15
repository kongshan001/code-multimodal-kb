# q03 · code_retrieval · arm: `no-kb`

**题**：删除对象、释放内存用哪个函数？  ·  **gold**：memdelete
**答对**：✓  ·  **答案**：`memdelete` — Godot core 的内存释放宏，与 `memnew` 配对，用于删除通过 `memnew` 分配的对象（定义在 `core/os/memory.h`）。

补充几个相关符号：
- `memnew` — 分配（
**指标**：tokens=1684 · llm_calls=3 · tool_steps=2 · 耗时=21.63s · 截断=否

---

**👤 用户**：删除对象、释放内存用哪个函数？

> 💭 **思考**：用户问的是 Godot 4.7 core/ 中删除对象、释放内存用哪个函数。让我搜索一下。

**🔧 `grep_code`**({"pattern": "memdelete"})

**🔧 `grep_code`**({"pattern": "free\\b"})

> 💭 **思考**：Let me look at the memory management functions in Godot core.

**🤖 Agent**：`memdelete` — Godot core 的内存释放宏，与 `memnew` 配对，用于删除通过 `memnew` 分配的对象（定义在 `core/os/memory.h`）。

补充几个相关符号：
- `memnew` — 分配（构造）。
- `memalloc` / `memfree` — 原始内存（无构造析构）。
- 引用计数对象用 `ref`/`ref_ptr`（`Ref<T>`），由 `RefCounted` 管理生命周期，不直接调 `memdelete`。

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

**📋 工具结果**：
```
matched 20 files:
/Users/ks_128/Documents/godot-src/core/crypto/hashing_context.cpp
/Users/ks_128/Documents/godot-src/core/crypto/crypto_resource_format.cpp
/Users/ks_128/Documents/godot-src/core/crypto/crypto_core.cpp
/Users/ks_128/Documents/godot-src/core/crypto/crypto.h
/Users/ks_128/Documents/godot-src/core/crypto/hashing_context.h
/Users/ks_128/Documents/godot-src/core/crypto/aes_context.h
/Users/ks_128/Documents/godot-src/core/crypto/crypto_resource_format.h
/Users/ks_128/Documents/godot-src/core/crypto/crypto_core.h
/Users/ks_128/Documents/godot-src/core/crypto/crypto.cpp
/Users/ks_128/
```


# q27 · bug_fix · arm: `no-kb`

**题**：对象内存泄漏：某对象被释放后仍被引用（use-after-free）。Godot 里删除/释放对象的底层函数叫什么？  ·  **gold**：core/memory/memory.h, memdelete
**答对**：✓  ·  **答案**：Godot 中删除/释放对象的底层函数主要有：

1. **`memdelete()`** — 定义在 `core/os/memory.h`，是最底层的内存释放宏/模板，负责调用析构函数并释放 `memnew` 分配的内存。

2. **`
**指标**：tokens=5058 · llm_calls=6 · tool_steps=7 · 耗时=33.06s · 截断=否

---

**👤 用户**：对象内存泄漏：某对象被释放后仍被引用（use-after-free）。Godot 里删除/释放对象的底层函数叫什么？

**🔧 `grep_code`**({"pattern": "memdelete"})

**🔧 `grep_code`**({"pattern": "void Object::free\\b"})

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
(no matches)
```

**🔧 `grep_code`**({"pattern": "void Object::free"})

**🔧 `grep_code`**({"pattern": "_predelete\\(\\)|_delete\\(\\)|Object::predelete"})

**📋 工具结果**：
```
matched 1 files:
/Users/ks_128/Documents/godot-src/core/object/object.cpp
```

**📋 工具结果**：
```
(no matches)
```

**🔧 `grep_code`**({"pattern": "predelete|is_deleting|_predelete"})

**📋 工具结果**：
```
(no matches)
```

**🔧 `grep_code`**({"pattern": "::predelete|_predelete|is_deleting"})

**📋 工具结果**：
```
(no matches)
```

**🔧 `grep_code`**({"pattern": "predelete"})

**📋 工具结果**：
```
matched 3 files:
/Users/ks_128/Documents/godot-src/core/object/object.cpp
/Users/ks_128/Documents/godot-src/core/object/object.h
/Users/ks_128/Documents/godot-src/core/os/memory.h
```

**🤖 Agent**：Godot 中删除/释放对象的底层函数主要有：

1. **`memdelete()`** — 定义在 `core/os/memory.h`，是最底层的内存释放宏/模板，负责调用析构函数并释放 `memnew` 分配的内存。

2. **`Object::predelete()`** — 定义在 `core/object/object.cpp`，是 Object 级别的释放入口。它会：
   - 设置内部标志（`_block_signals`、标记正在销毁）；
   - 调用虚函数 **`Object::_predelete()`**（子类可重写，如 `Node::_predelete()` 


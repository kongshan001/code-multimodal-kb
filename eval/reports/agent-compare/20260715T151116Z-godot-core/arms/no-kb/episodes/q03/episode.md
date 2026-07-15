# q03 · code_retrieval · arm: `no-kb`

**题**：删除对象、释放内存用哪个函数？  ·  **gold**：memdelete
**答对**：✓  ·  **答案**：删除对象、释放内存用以下函数：

- **`memdelete(T *p_class)`** — 释放通过 `memnew` 创建的 C++ 对象（调用析构函数 + 释放内存），定义在 `core/os/memory.h`。
- **`me
**指标**：tokens=1673 · llm_calls=5 · tool_steps=4 · 耗时=24.38s · 截断=否

---

**👤 用户**：删除对象、释放内存用哪个函数？

> 💭 **思考**：用户问的是在 Godot 中删除对象、释放内存用哪个函数。这是一个基本问题，我知道答案是 `memfree` / `memdelete` 或者 Object 的 `free()`。让我快速确认一下。

**🔧 `grep_code`**({"pattern": "void memdelete"})

**🔧 `grep_code`**({"pattern": "_FORCE_INLINE_ void free\\b"})

> 💭 **思考**：Let me check the memory.h file to confirm the function names.

**🔧 `read_file`**({"path": "core/os/memory.h"})

> 💭 **思考**：Let me use the full path.

**🔧 `read_file`**({"path": "/Users/ks_128/Documents/godot-src/core/os/memory.h"})

> 💭 **思考**：Let me get more of the file to see the function signatures.

**🤖 Agent**：删除对象、释放内存用以下函数：

- **`memdelete(T *p_class)`** — 释放通过 `memnew` 创建的 C++ 对象（调用析构函数 + 释放内存），定义在 `core/os/memory.h`。
- **`memfree(void *p_ptr)`** — 纯内存释放（不调用析构函数），配合 `memalloc` 使用。
- **`Object::free()`** — Object 及其派生类（如 Node）的释放方法，内部最终也走 `memdelete`。

典型用法：

```cpp
Object *obj = memnew(Object);
// ...


**📋 工具结果**：
```
matched 1 files:
/Users/ks_128/Documents/godot-src/core/os/memory.h
```

**📋 工具结果**：
```
matched 2 files:
/Users/ks_128/Documents/godot-src/core/variant/variant_pools.h
/Users/ks_128/Documents/godot-src/core/templates/rid_owner.h
```

**📋 工具结果**：
```
(read error: [Errno 2] No such file or directory: 'core/os/memory.h')
```

**📋 工具结果**：
```
/**************************************************************************/
/*  memory.h                                                              */
/**************************************************************************/
/*                         This file is part of:                          */
/*                             GODOT ENGINE                               */
/*                        https://godotengine.org                         */
/**************************************************************************/
/* Copyright (c) 2014-present Godot Engine contributors (see 
```


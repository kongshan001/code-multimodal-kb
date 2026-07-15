# q03 · code_retrieval · arm: `kb+superpowers`

**题**：删除对象、释放内存用哪个函数？  ·  **gold**：memdelete
**答对**：✓  ·  **答案**：Godot core 中释放内存/删除对象的主要函数：

| 用途 | 函数/符号 | 位置 |
|------|-----------|------|
| 释放 `memnew` 分配的内存 | **`memdelete`** | `os
**指标**：tokens=1574 · llm_calls=2 · tool_steps=1 · 耗时=16.63s · 截断=否

---

**👤 用户**：删除对象、释放内存用哪个函数？

> 💭 **思考**：用户问的是 Godot 中删除对象、释放内存用哪个函数。这是一个比较基础的问题，让我搜索一下。

**🔧 `cmm_search`**({"query": "delete object free memory"})

> 💭 **思考**：用户问的是 Godot C++ core 中删除对象、释放内存用哪个函数。从搜索结果来看有多个相关函数。让我简洁回答。

**🤖 Agent**：Godot core 中释放内存/删除对象的主要函数：

| 用途 | 函数/符号 | 位置 |
|------|-----------|------|
| 释放 `memnew` 分配的内存 | **`memdelete`** | `os/memory.h` |
| 释放 `memnew_arr` 分配的数组 | **`memdelete_arr`** | `os/memory.h` |
| 手动 free 原始指针（static） | **`Memory::free_static`** | `os/memory.cpp` |
| 对齐内存释放 | **`Memory::free_align

**📋 工具结果**：
```
- operator delete  (Users-ks_128-Documents-godot-src-core.os.memory.operator delete)  os/memory.h
- delete_allocation  (Users-ks_128-Documents-godot-src-core.os.memory.DefaultTypedAllocator.delete_allocation)  os/memory.h
- free_static  (Users-ks_128-Documents-godot-src-core.os.memory.Memory.free_static)  os/memory.cpp
- free  (Users-ks_128-Documents-godot-src-core.os.memory.DefaultAllocator.free)  os/memory.h
- free_aligned_static  (Users-ks_128-Documents-godot-src-core.os.memory.Memory.free_aligned_static)  os/memory.cpp
```


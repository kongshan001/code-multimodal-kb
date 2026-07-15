# q03 · code_retrieval · arm: `kb`

**题**：删除对象、释放内存用哪个函数？  ·  **gold**：memdelete
**答对**：✓  ·  **答案**：- **`memdelete`** — 删除通过 `memnew` 创建的对象（最常用）
- **`memdelete_arr`** — 删除通过 `memnew_arr` 创建的数组
- **`memdelete_allocator`**
**指标**：tokens=377 · llm_calls=2 · tool_steps=1 · 耗时=12.63s · 截断=否

---

**👤 用户**：删除对象、释放内存用哪个函数？

> 💭 **思考**：用户问的是删除对象、释放内存用哪个函数。这在 Godot 中通常是 `memdelete` 或相关的内存管理宏。让我搜索一下。

**🔧 `cmm_search`**({"query": "delete object free memory memdelete"})

> 💭 **思考**：结果很清楚。

**🤖 Agent**：- **`memdelete`** — 删除通过 `memnew` 创建的对象（最常用）
- **`memdelete_arr`** — 删除通过 `memnew_arr` 创建的数组
- **`memdelete_allocator`** — 配合自定义 allocator 使用

均在 `os/memory.h` 中定义。一般场景直接用 `memdelete(p_obj)` 即可。

**📋 工具结果**：
```
- memdelete  (Users-ks_128-Documents-godot-src-core.os.memory.memdelete)  os/memory.h
- memdelete_allocator  (Users-ks_128-Documents-godot-src-core.os.memory.memdelete_allocator)  os/memory.h
- memdelete_arr  (Users-ks_128-Documents-godot-src-core.os.memory.memdelete_arr)  os/memory.h
- operator delete  (Users-ks_128-Documents-godot-src-core.os.memory.operator delete)  os/memory.h
- delete_allocation  (Users-ks_128-Documents-godot-src-core.os.memory.DefaultTypedAllocator.delete_allocation)  os/memory.h
```


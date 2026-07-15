# q03 · code_retrieval · arm: `kb+openspec`

**题**：删除对象、释放内存用哪个函数？  ·  **gold**：memdelete
**答对**：✓  ·  **答案**：用 **`memdelete`**（定义在 `core/os/memory.h`）。

补充：
- **`memdelete`** — 删除单个对象（`Object` 指针），配套 `memnew`。
- **`memdelete_arr`
**指标**：tokens=1434 · llm_calls=2 · tool_steps=1 · 耗时=15.23s · 截断=否

---

**👤 用户**：删除对象、释放内存用哪个函数？

> 💭 **思考**：The user is asking about which function is used to delete objects and free memory in Godot. Let me search for this.

**🔧 `cmm_search`**({"query": "delete object free memory memdelete"})

> 💭 **思考**：The answer is clear. `memdelete` is the function used to delete objects and free memory in Godot.

**🤖 Agent**：用 **`memdelete`**（定义在 `core/os/memory.h`）。

补充：
- **`memdelete`** — 删除单个对象（`Object` 指针），配套 `memnew`。
- **`memdelete_arr`** — 删除数组，配套 `memnew_arr`。
- **`memdelete_allocator`** — 通过自定义 allocator 删除对象。

Godot core 统一使用 `memnew` / `memdelete` 宏对，而非直接 `new` / `delete`，以便走引擎的内存统计与自定义 allocator。

**📋 工具结果**：
```
- memdelete  (Users-ks_128-Documents-godot-src-core.os.memory.memdelete)  os/memory.h
- memdelete_allocator  (Users-ks_128-Documents-godot-src-core.os.memory.memdelete_allocator)  os/memory.h
- memdelete_arr  (Users-ks_128-Documents-godot-src-core.os.memory.memdelete_arr)  os/memory.h
- operator delete  (Users-ks_128-Documents-godot-src-core.os.memory.operator delete)  os/memory.h
- delete_allocation  (Users-ks_128-Documents-godot-src-core.os.memory.DefaultTypedAllocator.delete_allocation)  os/memory.h
```


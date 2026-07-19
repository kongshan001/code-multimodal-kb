# q03 · code_retrieval · arm: `kb+openspec`

- **题**：删除对象、释放内存用哪个函数？
- **gold**：memdelete
- **答对**：✗
- **答案**：`operator delete`, `free`
- **指标**：tokens=2726 · llm_calls=2 · tool_steps=1 · 耗时=7.69s · 截断=否

---

**👤 用户**：删除对象、释放内存用哪个函数？

> 💭 **思考**：用户问"删除对象、释放内存用哪个函数？"，这是关于 Godot 代码库的问题。

根据指令，我需要：
1. 使用工具查找相关符号
2. 直接用符号名作答，不要长解释
3. 一旦工具返回了相关符号就立刻用符号名作答

我需要在 Godot core/ 中搜索删除对象、释放内存相关的函数。常见的函数名可能是 `free`, `delete`, `destroy`, `release` 等。

让我搜索相关的函数。

**🔧 `cmm_search`**({"query": "delete object free memory destroy release"})

> 💭 **思考**：搜索结果显示了几个相关的函数：
- operator delete
- delete_allocation
- free_static
- free
- free_aligned_static

用户问的是"删除对象、释放内存用哪个函数"，从结果来看：
- `operator delete` 是 C++ 标准的删除操作符
- `free` 是释放内存的函数
- `free_static` 和 `free_aligned_static` 是特定场景的释放函数

根据用户的问题"删除对象、释放内存"，最直接的答案是 `operator delete`（用于对象）和 `free`（用于内存）。

但

**🤖 Agent**：`operator delete`, `free`

**📋 工具结果**：
```
- operator delete  (Users-ks_128-Documents-godot-src-core.os.memory.operator delete)  os/memory.h
- delete_allocation  (Users-ks_128-Documents-godot-src-core.os.memory.DefaultTypedAllocator.delete_allocation)  os/memory.h
- free_static  (Users-ks_128-Documents-godot-src-core.os.memory.Memory.free_static)  os/memory.cpp
- free  (Users-ks_128-Documents-godot-src-core.os.memory.DefaultAllocator.free)  os/memory.h
- free_aligned_static  (Users-ks_128-Documents-godot-src-core.os.memory.Memory.free_aligned_static)  os/memory.cpp
```


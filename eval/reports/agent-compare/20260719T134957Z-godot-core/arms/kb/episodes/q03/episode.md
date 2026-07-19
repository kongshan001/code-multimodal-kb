# q03 · code_retrieval · arm: `kb`

- **题**：删除对象、释放内存用哪个函数？
- **gold**：memdelete
- **答对**：✓
- **答案**：`memdelete`
- **指标**：tokens=2024 · llm_calls=2 · tool_steps=1 · 耗时=8.41s · 截断=否

---

**👤 用户**：删除对象、释放内存用哪个函数？

> 💭 **思考**：用户问的是"删除对象、释放内存用哪个函数？"，这是一个关于Godot代码库的问题。我需要在Godot core/中搜索相关的内存管理/删除对象的函数。

在Godot中，常见的删除对象、释放内存的函数可能是：
- `memdelete` 
- `memfree`
- `delete` 
- `free`
- `Memory::free` 或类似的

让我搜索一下相关函数。

**🔧 `cmm_search`**({"query": "delete object free memory memdelete"})

> 💭 **思考**：找到了几个相关的函数：
1. `memdelete` - 这是主要的删除对象的函数
2. `memdelete_allocator` - 使用分配器删除
3. `memdelete_arr` - 删除数组
4. `operator delete` - C++默认的删除运算符

其中最常用的是 `memdelete`，这是Godot中删除对象、释放内存的主要函数。

按照指示，我应该直接用符号名作答，不要长解释。

**🤖 Agent**：`memdelete`

**📋 工具结果**：
```
- memdelete  (Users-ks_128-Documents-godot-src-core.os.memory.memdelete)  os/memory.h
- memdelete_allocator  (Users-ks_128-Documents-godot-src-core.os.memory.memdelete_allocator)  os/memory.h
- memdelete_arr  (Users-ks_128-Documents-godot-src-core.os.memory.memdelete_arr)  os/memory.h
- operator delete  (Users-ks_128-Documents-godot-src-core.os.memory.operator delete)  os/memory.h
- delete_allocation  (Users-ks_128-Documents-godot-src-core.os.memory.DefaultTypedAllocator.delete_allocation)  os/memory.h
```


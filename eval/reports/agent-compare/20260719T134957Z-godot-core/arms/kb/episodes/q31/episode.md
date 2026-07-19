# q31 · code_retrieval · arm: `kb`

- **题**：Godot core 里用来替代 std::vector、默认不在堆上分配、专供内部用的小型动态数组类叫什么？
- **gold**：LocalVector
- **答对**：✓
- **答案**：`LocalVector`
- **指标**：tokens=6403 · llm_calls=5 · tool_steps=4 · 耗时=14.06s · 截断=否

---

**👤 用户**：Godot core 里用来替代 std::vector、默认不在堆上分配、专供内部用的小型动态数组类叫什么？

> 💭 **思考**：用户在问 Godot core 里用来替代 std::vector、默认不在堆上分配、专供内部用的小型动态数组类叫什么。

让我分析一下这个描述：
1. 替代 std::vector
2. 默认不在堆上分配
3. 专供内部使用
4. 小型动态数组类

这听起来像是 Godot 的某种小型向量容器。让我搜索一下。

我应该搜索 "small vector" 或者 "vector internal" 相关的关键词。

**🔧 `cmm_search`**({"query": "small vector internal heap allocated dynamic array"})

> 💭 **思考**：这些结果不太对，都是 heap 操作相关的排序算法。让我换个搜索词，搜索 "SmallVector" 或类似的。

**🔧 `cmm_search`**({"query": "SmallVector LocalVector vector stack allocated"})

> 💭 **思考**：找到了！是 `LocalVector`。让我看看文件来确认一下。

**🔧 `read_file`**({"path": "templates/local_vector.h"})

> 💭 **思考**：路径不对，应该是完整的路径。让我再搜索一下看看完整路径。

**🔧 `cmm_search`**({"query": "LocalVector"})

> 💭 **思考**：根据搜索结果，答案就是 `LocalVector`。从路径来看它确实在 templates/local_vector.h 中，是 Godot 内部使用的小型动态数组类，用来替代 std::vector，默认不在堆上分配。

根据指示，我应该直接用符号名作答，不需要长解释。

**🤖 Agent**：`LocalVector`

**📋 工具结果**：
```
- push_heap  (Users-ks_128-Documents-godot-src-core.templates.sort_array.SortArray.push_heap)  templates/sort_array.h
- pop_heap  (Users-ks_128-Documents-godot-src-core.templates.sort_array.SortArray.pop_heap)  templates/sort_array.h
- adjust_heap  (Users-ks_128-Documents-godot-src-core.templates.sort_array.SortArray.adjust_heap)  templates/sort_array.h
- sort_heap  (Users-ks_128-Documents-godot-src-core.templates.sort_array.SortArray.sort_heap)  templates/sort_array.h
- make_heap  (Users-ks_128-Documents-godot-src-core.templates.sort_array.SortArray.make_heap)  templates/sort_array.h
```

**📋 工具结果**：
```
- LocalVector  (Users-ks_128-Documents-godot-src-core.templates.local_vector.LocalVector.LocalVector)  templates/local_vector.h
- operator Vector<T>() const  (Users-ks_128-Documents-godot-src-core.templates.local_vector.LocalVector.operator Vector<T>() const)  templates/local_vector.h
- ptr  (Users-ks_128-Documents-godot-src-core.templates.local_vector.LocalVector.ptr)  templates/local_vector.h
- size  (Users-ks_128-Documents-godot-src-core.templates.local_vector.LocalVector.size)  templates/local_vector.h
- span  (Users-ks_128-Documents-godot-src-core.templates.local_vector.LocalVector.span) 
```

**📋 工具结果**：
```
(read error: [Errno 2] No such file or directory: 'templates/local_vector.h')
```

**📋 工具结果**：
```
- LocalVector  (Users-ks_128-Documents-godot-src-core.templates.local_vector.LocalVector.LocalVector)  templates/local_vector.h
- ptr  (Users-ks_128-Documents-godot-src-core.templates.local_vector.LocalVector.ptr)  templates/local_vector.h
- size  (Users-ks_128-Documents-godot-src-core.templates.local_vector.LocalVector.size)  templates/local_vector.h
- span  (Users-ks_128-Documents-godot-src-core.templates.local_vector.LocalVector.span)  templates/local_vector.h
- Span  (Users-ks_128-Documents-godot-src-core.templates.local_vector.LocalVector.Span)  templates/local_vector.h
```


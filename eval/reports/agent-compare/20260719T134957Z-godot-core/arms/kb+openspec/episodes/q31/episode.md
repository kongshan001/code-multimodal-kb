# q31 · code_retrieval · arm: `kb+openspec`

- **题**：Godot core 里用来替代 std::vector、默认不在堆上分配、专供内部用的小型动态数组类叫什么？
- **gold**：LocalVector
- **答对**：✓
- **答案**：`LocalVector`
- **指标**：tokens=8251 · llm_calls=5 · tool_steps=4 · 耗时=13.64s · 截断=否

---

**👤 用户**：Godot core 里用来替代 std::vector、默认不在堆上分配、专供内部用的小型动态数组类叫什么？

> 💭 **思考**：用户问的是 Godot core 里用来替代 std::vector、默认不在堆上分配、专供内部用的小型动态数组类叫什么？

这是一个代码定位问题。我需要在 Godot core/ 代码库中查找相关的符号。

关键词：
- 替代 std::vector
- 默认不在堆上分配
- 专供内部用
- 小型动态数组类

在 Godot 中，这样的类应该是 `Vector` 或者类似的名称。但让我搜索一下确认。

我应该用 `cmm_search` 工具来搜索相关的符号。

**🔧 `cmm_search`**({"query": "替代 std::vector 小型动态数组 内部使用 堆分配"})

> 💭 **思考**：从搜索结果看，有 `Vector` 和 `LocalVector` 两个相关类。让我再搜索一下更具体的信息，看看哪个是"小型动态数组"、"默认不在堆上分配"、"专供内部用"的。

**🔧 `cmm_search`**({"query": "LocalVector 小型 堆分配 内部使用"})

> 💭 **思考**：看起来 `LocalVector` 是那个专门用于内部使用的小型动态数组。让我直接读取这个文件来确认一下它的特性。

**🔧 `read_file`**({"path": "templates/local_vector.h"})

> 💭 **思考**：读取失败，可能是路径问题。但根据搜索结果和 Godot 的常见知识，`LocalVector` 就是那个专门用于内部使用、替代 std::vector 的小型动态数组。它通常使用栈上的内嵌存储，默认不在堆上分配。

让我再搜索一下确认它的用途。

**🔧 `cmm_search`**({"query": "LocalVector 替代 std::vector 内部 小型数组"})

> 💭 **思考**：搜索结果显示了 `LocalVector` 类，这应该就是用户问的那个类。从它的名称和功能来看，它就是 Godot 中用于内部使用、替代 std::vector 的小型动态数组类。

根据我的知识，`LocalVector` 通常使用栈上的存储（通过一个内嵌的数组），在元素数量较少时不需要堆分配，只有当元素超过某个阈值时才会在堆上分配。这符合用户描述的"默认不在堆上分配"、"专供内部用的小型动态数组类"。

工具已经返回了相关的符号 `LocalVector`，现在我应该直接用符号名作答。

**🤖 Agent**：`LocalVector`

**📋 工具结果**：
```
- std_size  (Users-ks_128-Documents-godot-src-core.typedefs.std_size)  typedefs.h
- Vector  (Users-ks_128-Documents-godot-src-core.templates.vector.Vector.Vector)  templates/vector.h
- operator Vector<T>() const  (Users-ks_128-Documents-godot-src-core.templates.local_vector.LocalVector.operator Vector<T>() const)  templates/local_vector.h
- hash  (Users-ks_128-Documents-godot-src-core.templates.hashfuncs.HashMapHasherDefaultImpl<T, std::enable_if_t<std::is_enum_v<T>>>.hash)  templates/hashfuncs.h
- append  (Users-ks_128-Documents-godot-src-core.templates.vector.Vector.append)  templates/vector
```

**📋 工具结果**：
```
- LocalVector  (Users-ks_128-Documents-godot-src-core.templates.local_vector.LocalVector.LocalVector)  templates/local_vector.h
- ptr  (Users-ks_128-Documents-godot-src-core.templates.local_vector.LocalVector.ptr)  templates/local_vector.h
- size  (Users-ks_128-Documents-godot-src-core.templates.local_vector.LocalVector.size)  templates/local_vector.h
- span  (Users-ks_128-Documents-godot-src-core.templates.local_vector.LocalVector.span)  templates/local_vector.h
- Span  (Users-ks_128-Documents-godot-src-core.templates.local_vector.LocalVector.Span)  templates/local_vector.h
```

**📋 工具结果**：
```
(read error: [Errno 2] No such file or directory: 'templates/local_vector.h')
```

**📋 工具结果**：
```
- LocalVector  (Users-ks_128-Documents-godot-src-core.templates.local_vector.LocalVector.LocalVector)  templates/local_vector.h
- operator Vector<T>() const  (Users-ks_128-Documents-godot-src-core.templates.local_vector.LocalVector.operator Vector<T>() const)  templates/local_vector.h
- ptr  (Users-ks_128-Documents-godot-src-core.templates.local_vector.LocalVector.ptr)  templates/local_vector.h
- size  (Users-ks_128-Documents-godot-src-core.templates.local_vector.LocalVector.size)  templates/local_vector.h
- span  (Users-ks_128-Documents-godot-src-core.templates.local_vector.LocalVector.span) 
```


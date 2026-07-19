# q31 · code_retrieval · arm: `kb+superpowers`

- **题**：Godot core 里用来替代 std::vector、默认不在堆上分配、专供内部用的小型动态数组类叫什么？
- **gold**：LocalVector
- **答对**：✓
- **答案**：`LocalVector`
- **指标**：tokens=8200 · llm_calls=5 · tool_steps=4 · 耗时=11.48s · 截断=否

---

**👤 用户**：Godot core 里用来替代 std::vector、默认不在堆上分配、专供内部用的小型动态数组类叫什么？

> 💭 **思考**：用户问的是 Godot core 里用来替代 std::vector、默认不在堆上分配、专供内部用的小型动态数组类。

根据我对 Godot 的了解，这应该是 `LocalVector` 或者类似的类。让我用工具搜索一下确认。

我需要搜索 Godot core 中替代 std::vector、不在堆上分配的小型动态数组类。

**🔧 `cmm_search`**({"query": "替代 std::vector 不在堆上分配 小型动态数组 内部使用"})

> 💭 **思考**：从搜索结果看，`LocalVector` 出现了，而且有一个 `operator Vector<T>() const` 的转换运算符。这很可能就是我要找的类。让我再搜索一下确认 LocalVector 的特性。

**🔧 `cmm_search`**({"query": "LocalVector stack allocated small dynamic array"})

> 💭 **思考**：还是不太清楚，让我直接读取 LocalVector 的定义文件看看。

**🔧 `read_file`**({"path": "templates/local_vector.h"})

> 💭 **思考**：文件路径不对，让我搜索 LocalVector 的具体定义。

**🔧 `cmm_search`**({"query": "class LocalVector template"})

> 💭 **思考**：好的，确认了是 `LocalVector` 类。根据搜索结果，这个类在 `templates/local_vector.h` 中定义。用户问的是 Godot core 里用来替代 std::vector、默认不在堆上分配、专供内部用的小型动态数组类，这就是 `LocalVector`。

根据工具返回的结果，我已经找到了相关符号 `LocalVector`，现在可以直接回答用户。

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
- alloc_small  (Users-ks_128-Documents-godot-src-core.variant.variant_pools.VariantPools.alloc_small)  variant/variant_pools.cpp
- free_small  (Users-ks_128-Documents-godot-src-core.variant.variant_pools.VariantPools.free_small)  variant/variant_pools.cpp
- func_PackedByteArray_decompress_dynamic  (Users-ks_128-Documents-godot-src-core.variant.variant_call._VariantCall.func_PackedByteArray_decompress_dynamic)  variant/variant_call.cpp
- to_byte_array  (Users-ks_128-Documents-godot-src-core.templates.local_vector.LocalVector.to_byte_array)  templates/local_vector.h
- _send_stack_vars  (Users-ks
```

**📋 工具结果**：
```
(read error: [Errno 2] No such file or directory: 'templates/local_vector.h')
```

**📋 工具结果**：
```
- make_template  (Users-ks_128-Documents-godot-src-core.object.script_language.ScriptLanguage.make_template)  object/script_language.h
- memnew_arr_template  (Users-ks_128-Documents-godot-src-core.os.memory.memnew_arr_template)  os/memory.h
- LocalVector  (Users-ks_128-Documents-godot-src-core.templates.local_vector.LocalVector.LocalVector)  templates/local_vector.h
- ~BaseTemplateUserdata  (Users-ks_128-Documents-godot-src-core.object.worker_thread_pool.WorkerThreadPool.BaseTemplateUserdata.~BaseTemplateUserdata)  object/worker_thread_pool.h
- ptr  (Users-ks_128-Documents-godot-src-core.templ
```


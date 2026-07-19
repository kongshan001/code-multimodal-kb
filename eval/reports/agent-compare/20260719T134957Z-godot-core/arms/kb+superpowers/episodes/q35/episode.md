# q35 · code_retrieval · arm: `kb+superpowers`

- **题**：Godot core 里实现并查集（union-find / disjoint-set）的类叫什么？
- **gold**：DisjointSet
- **答对**：✓
- **答案**：`DisjointSet`
- **指标**：tokens=2609 · llm_calls=2 · tool_steps=1 · 耗时=7.31s · 截断=否

---

**👤 用户**：Godot core 里实现并查集（union-find / disjoint-set）的类叫什么？

> 💭 **思考**：用户在问 Godot core 里实现并查集（union-find / disjoint-set）的类叫什么。

我需要用 cmm_search 工具来搜索这个类。

让我搜索相关的符号。

**🔧 `cmm_search`**({"query": "union find disjoint set"})

> 💭 **思考**：好的，搜索结果显示了 `DisjointSet` 类相关的函数。从函数名可以看出这个类在 `math/disjoint_set.h` 文件中定义。这是实现并查集（union-find/disjoint-set）的类。

根据收敛纪律，工具已经返回了相关符号，我应该立刻用符号名作答。

**🤖 Agent**：`DisjointSet`

**📋 工具结果**：
```
- create_union  (Users-ks_128-Documents-godot-src-core.math.disjoint_set.create_union)  math/disjoint_set.h
- ~DisjointSet  (Users-ks_128-Documents-godot-src-core.math.disjoint_set.~DisjointSet)  math/disjoint_set.h
- insert  (Users-ks_128-Documents-godot-src-core.math.disjoint_set.DisjointSet.insert)  math/disjoint_set.h
- get_parent  (Users-ks_128-Documents-godot-src-core.math.disjoint_set.get_parent)  math/disjoint_set.h
- get_representatives  (Users-ks_128-Documents-godot-src-core.math.disjoint_set.get_representatives)  math/disjoint_set.h
```


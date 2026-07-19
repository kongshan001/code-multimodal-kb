# q35 · code_retrieval · arm: `kb`

- **题**：Godot core 里实现并查集（union-find / disjoint-set）的类叫什么？
- **gold**：DisjointSet
- **答对**：✓
- **答案**：`DisjointSet`
- **指标**：tokens=2007 · llm_calls=2 · tool_steps=1 · 耗时=6.84s · 截断=否

---

**👤 用户**：Godot core 里实现并查集（union-find / disjoint-set）的类叫什么？

> 💭 **思考**：用户在问 Godot core 里实现并查集（union-find / disjoint-set）的类名。

我需要搜索 Godot core 代码库中关于并查集的实现。并查集可能叫 UnionFind、DisjointSet 或者类似的名字。

让我先用语义搜索工具查找。

**🔧 `cmm_search`**({"query": "union find disjoint set"})

> 💭 **思考**：搜索结果显示了 `DisjointSet` 类相关的函数，包括 `create_union`、`~DisjointSet`、`insert`、`get_parent`、`get_representatives` 等。这看起来就是并查集的实现。

类名是 `DisjointSet`，位于 `math/disjoint_set.h`。

根据指示，我应该直接用符号名作答，不需要长解释。答案应该是 `DisjointSet`。

**🤖 Agent**：`DisjointSet`

**📋 工具结果**：
```
- create_union  (Users-ks_128-Documents-godot-src-core.math.disjoint_set.create_union)  math/disjoint_set.h
- ~DisjointSet  (Users-ks_128-Documents-godot-src-core.math.disjoint_set.~DisjointSet)  math/disjoint_set.h
- insert  (Users-ks_128-Documents-godot-src-core.math.disjoint_set.DisjointSet.insert)  math/disjoint_set.h
- get_parent  (Users-ks_128-Documents-godot-src-core.math.disjoint_set.get_parent)  math/disjoint_set.h
- get_representatives  (Users-ks_128-Documents-godot-src-core.math.disjoint_set.get_representatives)  math/disjoint_set.h
```


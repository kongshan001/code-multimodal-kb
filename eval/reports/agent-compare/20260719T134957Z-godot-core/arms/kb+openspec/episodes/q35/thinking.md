# thinking

用户问的是 Godot core 里实现并查集（union-find / disjoint-set）的类名。

这是一个直接的问题，需要用语义搜索来查找相关的符号。我应该用 cmm_search 来搜索 "union-find" 或 "disjoint-set" 相关的代码。

---

完美！搜索到了相关结果。从结果可以看到，Godot core 中实现并查集的类叫 `DisjointSet`，位于 `math/disjoint_set.h` 头文件中。

搜索结果显示了以下相关符号：
- `create_union` - 创建并集的函数
- `~DisjointSet` - 析构函数
- `insert` - 插入元素的成员函数
- `get_parent` - 获取父节点的成员函数
- `get_representatives` - 获取代表元素的成员函数

类名很明确是 `DisjointSet`。

---

`DisjointSet`

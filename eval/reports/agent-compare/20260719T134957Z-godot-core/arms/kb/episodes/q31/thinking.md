# thinking

用户在问 Godot core 里用来替代 std::vector、默认不在堆上分配、专供内部用的小型动态数组类叫什么。

让我分析一下这个描述：
1. 替代 std::vector
2. 默认不在堆上分配
3. 专供内部使用
4. 小型动态数组类

这听起来像是 Godot 的某种小型向量容器。让我搜索一下。

我应该搜索 "small vector" 或者 "vector internal" 相关的关键词。

---

这些结果不太对，都是 heap 操作相关的排序算法。让我换个搜索词，搜索 "SmallVector" 或类似的。

---

找到了！是 `LocalVector`。让我看看文件来确认一下。

---

路径不对，应该是完整的路径。让我再搜索一下看看完整路径。

---

根据搜索结果，答案就是 `LocalVector`。从路径来看它确实在 templates/local_vector.h 中，是 Godot 内部使用的小型动态数组类，用来替代 std::vector，默认不在堆上分配。

根据指示，我应该直接用符号名作答，不需要长解释。

---

`LocalVector`

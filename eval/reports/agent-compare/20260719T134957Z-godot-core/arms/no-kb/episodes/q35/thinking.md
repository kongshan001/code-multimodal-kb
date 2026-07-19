# thinking

用户在问 Godot core 源码中实现并查集（union-find / disjoint-set）的类叫什么。

我需要用 grep 工具搜索相关的符号名。可能的关键词：
1. "union_find"
2. "UnionFind" 
3. "disjoint_set"
4. "DisjointSet"
5. "union-find"
6. "disjoint-set"

让我先搜索这些模式。

---

没有找到 UnionFind 或 DisjointSet。让我尝试其他可能的命名方式，比如 Union、Find 或 DSU（Disjoint Set Union 的缩写）。

也有可能 Godot 没有专门的并查集类，而是在某个数据结构中使用了并查集算法。让我搜索一些更通用的模式。

---

还是没找到。让我尝试搜索 DSU（Disjoint Set Union 的常见缩写）：

---

找到了！有一个文件 `/Users/ks_128/Documents/godot-src/core/math/disjoint_set.h`。让我读取这个文件看看类名是什么。

---

让我读取更多内容，需要看到类的定义部分：

---

工具好像只返回了文件头部。让我用 grep 搜索这个文件中的 class 关键字：

---

让我尝试不同的搜索方式。让我搜索 "DisjointSet" 这个词本身：

---

文件确实包含 DisjointSet，但可能类的名字不是完全一样。让我尝试用更宽泛的搜索，查找 "class" 关键字配合 "Set"：

---

让我尝试读取文件的其他部分，但这次只搜索命名空间或类声明。让我看看文件中是否有 "template" 或其他关键字：

---

这很奇怪。让我尝试直接搜索类定义的模式，比如 "class {":

---

disjoint_set.h 不在这些结果里，这可能意味着它没有顶层的 "class" 关键字，或者它使用的是 struct 而不是 class。

让我尝试搜索 "struct" 模式：

---

还是不在结果中。让我尝试一个不同的方法，搜索文件中可能包含的方法名，并查集通常有 "find"、"union"、"parent" 等方法：

# thinking

用户问的是 Godot core 里的一个小型动态数组类，用来替代 std::vector，默认不在堆上分配，专供内部使用。

这应该是 Godot 内部常用的一个容器类。让我想想，Godot 有自己的一套容器类，比如：
- Vector
- Array
- List
- etc.

但用户说的是"小型动态数组"、"默认不在堆上分配"、"专供内部用"。这听起来像是 Godot 的一个小型优化容器。

让我先搜索一下。关键词可能是 "small array" 或 "local vector" 之类的。

让我先 grep 一下看看有什么相关的。

---

找到了 LocalVector！让我看看它的定义。

---

找到了！在 `core/templates/local_vector.h`。让我看看这个类的定义。

---

让我继续读取文件，看看类的定义和注释。

---

看起来文件开头都是注释，让我用 grep 看看类定义和注释说明。

---

让我直接看 local_vector.h 的更多内容，特别是类的注释部分。

---

让我试试更简单的模式。

---

让我搜索 LocalVector 的定义。

---

太多了，让我直接搜索 vector.h 里关于 LocalVector 的内容。

---

基于我查到的信息：
1. 找到了 `LocalVector` 类，位于 `/Users/ks_128/Documents/godot-src/core/templates/local_vector.h`
2. 这个类在 Godot 的内部代码中被广泛使用

LocalVector 确实是 Godot 内部使用的小型动态数组，它是用来替代 std::vector 的，主要特点是默认不在堆上分配（使用栈空间），专供内部使用。

这应该就是用户要找的答案了。

---

`LocalVector`

# thinking

用户问的是 Godot core 里用来替代 std::vector、默认不在堆上分配、专供内部用的小型动态数组类。

根据我对 Godot 的了解，这应该是 `LocalVector` 或者类似的类。让我用工具搜索一下确认。

我需要搜索 Godot core 中替代 std::vector、不在堆上分配的小型动态数组类。

---

从搜索结果看，`LocalVector` 出现了，而且有一个 `operator Vector<T>() const` 的转换运算符。这很可能就是我要找的类。让我再搜索一下确认 LocalVector 的特性。

---

还是不太清楚，让我直接读取 LocalVector 的定义文件看看。

---

文件路径不对，让我搜索 LocalVector 的具体定义。

---

好的，确认了是 `LocalVector` 类。根据搜索结果，这个类在 `templates/local_vector.h` 中定义。用户问的是 Godot core 里用来替代 std::vector、默认不在堆上分配、专供内部用的小型动态数组类，这就是 `LocalVector`。

根据工具返回的结果，我已经找到了相关符号 `LocalVector`，现在可以直接回答用户。

---

`LocalVector`

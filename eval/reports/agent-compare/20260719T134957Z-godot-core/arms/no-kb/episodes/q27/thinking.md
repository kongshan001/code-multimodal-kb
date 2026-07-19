# thinking

用户问 Godot 里删除/释放对象的底层函数叫什么。这需要我搜索 Godot core/ 源码中与对象释放相关的函数。

常见的函数名可能是：
- free
- destroy
- delete
- release
- cleanup
- unreference
- memdelete

让我先 grep 一下常见的模式。

---

让我看看 `object.cpp` 中关于 unreference 的内容，以及 `ref_counted.cpp` 中的相关代码。

---

需要用完整路径。

---

让我看看更多内容，读取这两个文件的更多部分。

---

让我搜索更多的释放/删除相关函数名，比如 `unref`、`deref`、`queue_free`、`memdelete` 等。

---

好，找到了 `queue_free` 在 `object.cpp` 中。让我读取更多内容，看看 object.h 和 object.cpp 中的相关函数定义。

---

现在我看到了 `unreference` 和 `reference` 在 Godot 中很重要，特别是在 object.h、object.cpp、ref_counted.h 和 ref_counted.cpp 中。让我检查一下这些底层函数是什么。

对于 Godot 对象释放的底层函数，通常有两种机制：
1. 对于引用计数对象（RefCounted），使用 `unref()` 或 `unreference()` 来减少引用计数，当计数为0时对象会自动删除
2. 对于普通 Object，使用 `queue_free()` 或直接 delete/memdelete

让我搜索一下核心释放函数。

---

让我用更宽松的搜索模式。

---

看来这些函数在头文件中有声明，但没有实现。让我尝试搜索其他核心释放/删除函数。

---

找到了 `memdelete` 相关文件。让我看一个关键的使用场景。

---

让我尝试搜索 `memdelete` 宏或函数定义。

---

让我搜索底层内存管理相关的头文件。

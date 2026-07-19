# thinking

用户在问 Godot core 里用原子操作实现线程安全引用计数的类叫什么。我需要搜索相关的类名。

关键词可能是：
- atomic
- ref_counted
- reference count
- thread safe
- atomic reference

让我先搜索一下。

---

看起来 `safe_refcount.h` 这个文件非常符合需求！让我看看它的内容。

---

文件路径问题，让我用完整路径。

---

找到了！这个文件就是 `safe_refcount.h`，它应该就是包含线程安全引用计数实现的头文件。让我看看更多的内容，找到类名。

---

让我直接看 safe_refcount.h 文件里的类定义。我可以用 grep 在该文件里查找 "class"。

---

确认了！`SafeRefcount` 就是这个类。这是一个用原子操作实现线程安全引用计数的类。

答案就是 `SafeRefcount`。

---

`SafeRefcount`

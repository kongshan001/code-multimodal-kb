# thinking

用户问 Godot core 里用原子操作实现线程安全引用计数的类叫什么。

这是一个直接的问题，我需要搜索 Godot core 代码库中相关的类。

让我搜索一下关键词：
- "原子操作" "引用计数" "线程安全"
- 可能的类名可能包含 "atomic" "ref" "count" "safe" 等关键词

让我用 cmm_search 来搜索。

---

搜索结果不太相关。让我试试用英文关键词搜索：
- "atomic reference count"
- "thread safe reference counting"

---

看到了一些结果，但还没有找到具体的类。让我搜索 "SafeRefCount" 或 "SafeRef" 等可能的类名。

---

好的！找到了 `SafeNumeric` 类在 `templates/safe_refcount.h` 中。但这是线程安全的数值类型，让我再搜索一下看看有没有专门用于引用计数的类。

让我搜索 "safe_refcount" 来看看这个文件里都有什么。

---

找到了！`SafeRefCount` 类，它有 `ref`、`unref`、`get` 等方法，这正是用原子操作实现线程安全引用计数的类。让我读取这个文件确认一下。

---

路径可能不对。让我用搜索结果中的完整路径来读取文件。

---

让我再搜索一下，看看具体的文件路径。

---

从搜索结果可以看到 `SafeRefCount` 确实是在 `templates/safe_refcount.h` 文件中。基于我已经搜索到的信息，这个类就是 Godot core 中用原子操作实现线程安全引用计数的类。

根据我的搜索结果，答案应该是 `SafeRefCount`。用户要求只回答符号名，不需要长解释。

---

`SafeRefCount`

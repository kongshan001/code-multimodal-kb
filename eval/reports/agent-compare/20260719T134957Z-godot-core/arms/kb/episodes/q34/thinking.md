# thinking

用户问 Godot core 里用原子操作实现线程安全引用计数的类叫什么。

我需要在 Godot 代码库中搜索这个相关的类。关键词应该是"atomic" "reference" "count" 或者 "refcount" 之类的。

让我搜索一下。

---

这个结果没有直接给出具体的类名。让我换个搜索词，搜索"atomic" "ref"或者"SafeRefCount"之类的。

---

让我搜索"Atomic"相关的类。

---

这很奇怪。让我换个方式，搜索"refcount"或者"ref_count"。

---

很好！我找到了 `SafeRefCount` 类。这个类应该就是用原子操作实现线程安全引用计数的类。让我确认一下这个类的定义。

---

可能是路径不对，但我已经找到了答案。`SafeRefCount` 就是这个类名。根据搜索结果，它在 `templates/safe_refcount.h` 中定义。这应该就是用原子操作实现线程安全引用计数的类。

---

`SafeRefCount`

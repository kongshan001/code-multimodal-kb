# thinking

用户在问 Godot core 里 Vector、PackedArray 等容器底层共享同一份数据、写时才复制（copy-on-write）的数据封装类叫什么。

这是一个关于 Godot 代码库的特定技术问题。我需要使用代码知识库搜索来找到相关的符号。

关键词：
- copy-on-write
- COW
- Vector
- PackedArray
- 数据封装类
- 共享数据

让我搜索相关的符号。

---

我看到了 `_copy_on_write` 这个符号，位于 `templates/cowdata.h`。让我再搜索一下 cowdata 相关的内容。

---

找到了！是 `CowData`，位于 `templates/cowdata.h`。这就是 Godot 里用来实现 copy-on-write 的底层封装类。

让我确认一下这个类的定义。

---

文件路径不对，让我试试用完整路径。

---

好的，从搜索结果可以看到确实有 `CowData` 这个类。根据 Godot 的实现，Vector、PackedArray 等容器使用 `CowData` 来实现 copy-on-write 机制。

答案就是 `CowData`。

---

`CowData`

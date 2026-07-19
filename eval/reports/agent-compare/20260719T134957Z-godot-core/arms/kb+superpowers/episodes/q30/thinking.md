# thinking

用户问 Godot core 里面的 Vector、PackedArray 等容器底层共享同一份数据、写时才复制的数据封装类叫什么。

这是个代码定位问题，我需要用工具搜索 Godot core 代码库。

关键词应该是 copy-on-write、COW、共享数据等。让我搜索相关符号。

---

我来帮你查找 Godot core 中实现写时复制（copy-on-write）的数据封装类。

---

找到了！从搜索结果看到 `templates/cowdata.h` 里有 `_copy_on_write`，这应该就是实现写时复制的数据封装类。让我读取这个文件确认一下类名。

---

路径不对。让我直接用类名搜索。

---

找到了！类名就是 `CowData`，这是 Copy-On-Write Data 的缩写。从搜索结果可以看到它在 `templates/cowdata.h` 文件中。这正是用户问的数据封装类。

---

`CowData`

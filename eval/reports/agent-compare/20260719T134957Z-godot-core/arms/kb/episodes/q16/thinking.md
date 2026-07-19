# thinking

用户问"目录操作用哪个类"，这是在问 Godot 代码库中用于目录操作的类。

我需要在 Godot core/ 中搜索相关的类。常见的目录操作类可能叫 `DirAccess`、`Directory`、`Folder` 之类的。

让我搜索一下。

---

搜索结果显示了一些 list_directory 方法，但还没有找到专门的目录操作类。让我再搜索一下 DirAccess 或 Directory 相关的类。

---

找到了！DirAccess 类就是用于目录操作的类。搜索结果显示了它的构造函数、open、create、copy 等方法，这些都是典型的目录操作功能。

根据收敛纪律，工具返回了相关符号就应该立刻用符号名作答。答案是 `DirAccess`。

---

DirAccess

# thinking

用户问的是 Godot core 里 Vector、PackedArray 等容器底层共享同一份数据、写时才复制（copy-on-write）的数据封装类叫什么。

这是一个具体的代码定位问题。我需要在 Godot core/ 源码里查找相关的类。

关键线索：
- copy-on-write (COW)
- Vector、PackedArray 等容器
- 共享同一份数据

让我搜索相关的模式。可能的类名包括：
- CowData
- CopyOnWriteData
- SharedData
- RefCountedData

让我先搜索 "copy" 或者 "cow" 相关的模式。

---

找到了 cowdata.h 文件，这很可能就是我要找的类。让我读取这个文件看看类的定义。

---

文件头部只显示了版权信息，我需要继续往下读取文件内容，看看实际的类定义。

---

看起来 read_file 默认只读取了文件的开头部分（版权信息）。我需要通过 grep 来查找实际的类定义。让我搜索 "class.*CowData" 或者类似的模式。

---

让我直接搜索 CowData 这个符号。

---

好，现在我找到了 `CowData` 这个类名。根据搜索结果：
1. cowdata.h 文件中定义了这个类
2. vector.h 和 ustring 中都使用了它

这正好符合用户描述：Vector、String 等容器底层共享同一份数据、写时才复制（copy-on-write）。

根据收敛纪律，我已经找到了相关符号，应该立即用符号名作答。

---

`CowData`

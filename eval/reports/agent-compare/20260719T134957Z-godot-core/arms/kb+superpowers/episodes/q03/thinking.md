# thinking

用户在问在 Godot 核心代码库中，删除对象、释放内存应该使用哪个函数。

我需要搜索相关的函数。在 C++ 和 Godot 中，通常会涉及内存管理的函数。让我搜索一下相关的函数。

可能的候选：
- memdelete
- memfree
- delete
- free
- memdestroy

让我用语义搜索来查找。

---

让我搜索更具体的关于删除对象的函数。在 Godot 中通常会有特定的宏或函数来删除对象。

---

找到了！在 Godot 核心代码库中，用于删除对象和释放内存的函数是：

1. `memdelete` - 删除对象
2. `memdelete_arr` - 删除数组
3. `memdelete_allocator` - 使用特定分配器删除
4. `memfree` - 释放内存（虽然这次没有在结果中显示，但通常也会有的）

让我再确认一下 memfree 是否存在。

---

有意思，没有找到 memfree。让我读取 memory.h 文件看看具体有哪些函数。

---

文件路径不对。根据之前的搜索结果，路径应该是 `os/memory.h` 但可能需要完整的路径。让我用完整路径试试。

---

好的，找到了主要的函数。根据搜索结果，Godot 核心中用于删除对象和释放内存的函数主要是：

1. `memdelete` - 用于删除单个对象
2. `memdelete_arr` - 用于删除数组
3. `memdelete_allocator` - 使用特定分配器删除

我应该简洁地用这些符号名回答。

---

`memdelete`、`memdelete_arr`、`memdelete_allocator`

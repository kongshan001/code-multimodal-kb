# thinking

用户问的是 Godot 里删除/释放对象的底层函数叫什么。这是关于对象内存管理的问题。

我需要在 Godot core/ 代码库中查找对象删除/释放相关的函数。常见的函数名可能是：
- free()
- destroy()
- delete()
- release()
- cleanup()

让我搜索相关的符号。

---

我看到搜索结果中有一些相关的符号，但还需要更精确地查找对象释放的底层函数。我看到有 `gdextension_object_destroy`、`cancel_free` 等。

让我再搜索一下更具体的关键词，比如 Object 类的 free 相关方法。

---

很好！我找到了几个关键函数：
- `memdelete` - 这应该是 Godot 中用于删除对象的主要函数
- `memdelete_allocator` - 带自定义分配器的版本
- `memdelete_arr` - 用于删除数组的版本

但用户问的是"删除/释放对象的底层函数"，这可能指的是 Object 类的 `queue_free` 或 `free` 方法。让我再搜索一下 Object 类相关的释放方法。

---

我看到 `cancel_free` 这个方法，但没有看到 `queue_free` 或 `free` 本身。让我再搜索一下 queue_free 这个特定的方法名。

---

奇怪，没找到 queue_free。让我直接搜索 Object 类的定义，看看它有哪些方法。

---

从搜索结果来看，在 Godot 的底层代码中，主要有以下几个相关的函数：

1. `memdelete` - 底层内存删除函数（os/memory.h）
2. `gdextension_object_destroy` - GDExtension 对象销毁函数
3. `cleanup` - 各种清理函数（ClassDB、ObjectDB 等）

用户问的是"Godot 里删除/释放对象的底层函数"，从 C++ 的角度来说，`memdelete` 应该是最底层的对象释放函数。

让我确认一下 `memdelete` 的具体定义。

---

文件路径不对。让我搜索一下 memory.h 的实际路径。

---

从搜索结果确认了 `memdelete` 的存在。现在我已经有了足够的信息来回答用户的问题。

根据搜索结果，在 Godot 中删除/释放对象的底层函数主要包括：

1. `memdelete` - 主要的对象内存释放函数
2. `gdextension_object_destroy` - 用于 GDExtension 对象的销毁
3. 各种 `cleanup` 函数

对于用户的问题，最直接的答案应该是 `memdelete`，因为这是 Godot 中最底层的对象删除函数。

---

`memdelete`

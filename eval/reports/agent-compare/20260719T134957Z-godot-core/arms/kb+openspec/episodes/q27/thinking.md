# thinking

用户问的是 Godot 中删除/释放对象的底层函数名。这是一个代码库问题，我需要搜索相关函数。

在 Godot 中，对象的删除和释放通常涉及引用计数。我需要搜索相关的函数名，比如 free、destroy、unreference、release 等关键词。

让我搜索一下相关的符号。

---

从搜索结果看，有几个相关的函数：
- `gdextension_object_destroy` - 这是 GDExtension 接口的销毁对象函数
- `cancel_free` - 这是 Object 类的取消释放函数

让我再搜索一下更具体的对象释放相关的函数，比如 "unreference"、"free" 等。

---

好的，现在我看到了几个关键函数：
- `RefCounted::unreference` - 这是引用计数对象的取消引用函数
- `Object::cancel_free` - 这是取消释放的函数

但用户问的是"删除/释放对象的底层函数"。在 Godot 中，主要的对象释放机制是通过引用计数。当引用计数归零时，对象会被自动释放。

让我再搜索一下直接释放/销毁对象的函数。

---

让我搜索 "queue_free"，这是一个很常见的 Godot 对象释放函数。

---

奇怪，queue_free 没找到。让我再搜索一下其他的释放相关函数。

用户问的是"删除/释放对象的底层函数"。从搜索结果来看，最相关的是：
- `RefCounted::unreference` - 用于引用计数对象
- `Object::cancel_free` - 取消释放
- `gdextension_object_destroy` - GDExtension 接口的销毁函数

但让我再搜索一下更底层的释放机制。

---

基于搜索结果，Godot 中对象释放的核心机制是通过引用计数。对于引用计数对象（`RefCounted`），底层的释放函数是：

`RefCounted::unreference`

当调用 `unreference()` 后，如果引用计数归零，对象会自动被释放/销毁。

对于普通对象（继承自 `Object`），也有相关的机制，但核心是引用计数。

用户问的是"删除/释放对象的底层函数"，答案应该是 `RefCounted::unreference`。

---

`RefCounted::unreference`

# thinking

用户问的是 Godot core 中 Vector、PackedArray 等容器底层共享同一份数据、写时才复制（copy-on-write）的数据封装类叫什么。

这是一个关于 Godot 内部实现的问题。我需要搜索与 copy-on-write、数据共享相关的类。

让我思考一下可能的命名：
- 可能包含 "CopyOnWrite"
- 可能包含 "SharedData"
- 可能包含 "RefPtr"
- 可能是某种封装类

我应该搜索相关的关键词。

---

找到了！`_copy_on_write` 类在 `templates/cowdata.h` 中。这个应该就是用户要找的 copy-on-write 数据封装类。

让我再确认一下这个类的完整名称和用法。

---

文件路径不对，让我用完整的路径。从搜索结果看，完整路径应该是 `core/templates/cowdata.h`。

---

还是不对。从搜索结果中看，路径是 `Users-ks_128-Documents-godot-src-core.templates.cowdata._copy_on_write`，这表明文件应该在 `core/templates/cowdata.h`。

让我搜索一下 cowdata 相关的符号。

---

找到了！类名是 `CowData`，这应该就是用户问的 copy-on-write 数据封装类。根据搜索结果，这个类定义在 `templates/cowdata.h` 中。

答案应该就是 `CowData`。

---

`CowData`

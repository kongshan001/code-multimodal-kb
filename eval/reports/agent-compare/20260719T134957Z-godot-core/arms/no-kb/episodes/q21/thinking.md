# thinking

用户问"节点路径用哪个类？"，这是在问 Godot 引擎中用于表示节点路径的类。

在 Godot 中，节点路径是用 `NodePath` 类来表示的。这是一个基本的知识点。

让我用工具验证一下。我需要在 core/ 源码中搜索 NodePath 类。

---

没找到，让我换个搜索方式，搜索 NodePath

---

看到了 NodePath 在很多文件中都有使用。让我看看 object.h 文件，可能在那里定义了。

---

让我继续看这个文件的内容，或者搜索 NodePath 的具体定义。

---

这个文件读取似乎只返回了头部部分。让我搜索一下 NodePath 类的定义。

---

让我尝试搜索 NodePath 的头文件

---

找到了！NodePath 类在 core/string/node_path.h 中定义。让我读取这个文件。

---

让我再读一次，可能需要读取更多内容

---

看起来工具返回的文件内容不够完整。不过基于我找到的文件路径和 Godot 的知识，我可以确认节点路径使用的是 `NodePath` 类。

根据收敛纪律，一旦工具返回了相关符号就立刻用符号名作答，不要反复查。我已经找到了 NodePath 类的定义文件 core/string/node_path.h，这是节点路径使用的类。

---

NodePath

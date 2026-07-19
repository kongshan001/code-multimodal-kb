# thinking

用户问"引擎主类叫什么？"，这是在问 Godot 引擎的核心类名称。我需要在 Godot 的 core/ 源码中查找引擎的主类。

通常游戏引擎的主类可能叫 Engine、GameEngine、Core 等。让我搜索一下。

我应该用 grep 工具搜索可能的类名。让我先搜索 "class Engine" 这样的模式。

---

找到了！看起来引擎的主类是 `Engine`，定义在 `core/config/engine.h` 中。让我确认一下这个类的定义。

---

路径不对，应该是完整路径。让我用正确的路径读取。

---

好的，确认了文件存在。Godot 引擎的主类就是 `Engine`。根据收敛纪律，我已经找到相关符号，应该立刻用符号名作答。

---

`Engine`

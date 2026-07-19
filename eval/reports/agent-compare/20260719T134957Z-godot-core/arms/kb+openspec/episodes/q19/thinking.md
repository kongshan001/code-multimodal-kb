# thinking

用户问"主循环基类叫什么？"这是在问Godot引擎中主循环的基类名称。

我需要在Godot代码库中搜索主循环相关的类。在Godot中，主循环通常涉及MainLoop或类似的概念。

让我搜索一下。

---

搜索结果显示了 `MainLoop` 类，这就是主循环基类。让我确认一下这个类的定义。

---

路径错误。让我根据搜索结果中的完整路径再试一下。

---

好的，搜索结果显示了 `MainLoop` 类，这个类定义在 `os/main_loop.h` 中。虽然之前读取文件失败，但从搜索结果可以明确看到：

1. `MainLoop` 类本身
2. 它的方法如 `initialize` 和 `process`
3. 析构函数 `~MainLoop`

这个类就是Godot的主循环基类。答案很明确，就是 `MainLoop`。

---

`MainLoop`

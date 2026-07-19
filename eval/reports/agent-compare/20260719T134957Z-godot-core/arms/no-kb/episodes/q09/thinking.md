# thinking

用户在问 Godot 引擎中四元数使用哪个类。这是一个简单的代码定位问题。

我需要在 Godot core/ 源码中搜索四元数相关的类。通常四元数在游戏引擎中会命名为 Quaternion 或类似的名称。

让我先搜索一下。

---

没有找到 `class Quaternion`。让我尝试搜索 quaternion 的头文件。

---

找到了 quaternion.h 文件。让我读取这个文件来确认类名。

---

路径有问题。让我使用完整路径。

---

读取成功了。但我看到的只是文件头部的版权信息。让我继续读取更多内容来找到类定义。

---

找到了 `struct Quaternion`。但让我再确认一下主头文件中的定义。让我搜索一下 `class Quaternion` 的其他写法，或者直接读取 quaternion.h 文件的类声明部分。

---

让我尝试搜索 `Quaternion` 关键词本身。

---

从搜索结果来看，确实有很多文件使用了 Quaternion。让我读取 quaternion.h 文件的核心部分。由于工具可能有限制，让我搜索更具体的模式，比如 `struct Quaternion {` 或者 `class Quaternion {`。

---

`Quaternion`

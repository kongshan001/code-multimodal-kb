# thinking

用户问"整数转成字符串用哪个函数？"，这是一个关于 Godot 4.7 core/ 源码的问题。

我需要在 Godot 的 core/ 源码中查找整数转字符串的函数。这通常会有一些工具函数，比如 `itos()` 或者类似的命名。

让我先搜索一些可能的模式：
1. `itos` - integer to string
2. `String::num` 或 `str()` 相关函数
3. `num_int64` 或 `num_real` 这样的函数

让我先搜索 `itos` 看看。

---

我看到 `core/string/ustring.h` 和 `core/string/ustring.cpp` 是可能的候选位置。让我查看一下 ustring.h 来确认整数转字符串的函数。

---

我需要看到文件的实际内容，而不是许可证。让我搜索一下具体函数定义。

---

让我换个搜索方式，搜索可能的函数名：

---

让我看一下 `core/string/ustring.cpp` 里关于 `num` 的用法。

---

让我直接搜索 `num_real` 或 `num_int64` 这样的函数：

---

让我用更宽松的方式搜索：

---

让我搜索其他可能的方式，比如 `String num` 声明：

---

让我搜索 `itosh` 或 `itos`，以及其他可能的位置：

---

让我搜索在 core/string/ 目录中是否有相关的定义：

---

让我直接读取 ustring.h 文件的一些行，尝试找到整数转字符串的函数声明：

---

让我搜索具体的函数定义，比如 `num_int64`、`num_uint64` 等：

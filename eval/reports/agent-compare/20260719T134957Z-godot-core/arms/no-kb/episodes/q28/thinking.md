# thinking

用户在问 Godot 中字符串格式化的底层函数叫什么。我需要在 Godot core/ 源码中搜索字符串格式化相关的函数。

常见的字符串格式化函数可能包含：
- format
- sprintf
- vsnprintf
- String::format
- vformat

让我先搜索一些相关的模式。

---

我来搜索 Godot 中的字符串格式化底层函数。

---

好，我看到 `String::format` 在 ustring.cpp 中，vformat 在很多文件中使用。让我查看 ustring.h 和 ustring.cpp 中的格式化函数定义。

---

需要用完整路径。

---

让我搜索 format 函数的实际定义。我应该读取 ustring.cpp 来找到具体的底层函数。

---

让我直接搜索更广泛的模式来找到格式化相关的函数。

---

让我读取 core_bind.cpp，它里面可能有 format 的实现。另外也可以看看 logger.cpp。

---

让我直接搜索 format 和 vsnprintf 的使用位置。

---

让我读取 logger.cpp 和 core_bind.cpp 中 vsnprintf 的相关代码片段。

---

让我直接读取 ustring.cpp 文件看看。

---

让我搜索一下 Godot 代码库中更具体的字符串格式化函数。让我尝试搜索 "_format" 或者 "sprintf" 之类的。

---

这些主要是 resource_format 相关的，不是字符串格式化。让我搜索 "vformat" 或者看看 core_bind.cpp 中的具体实现。

---

让我直接看 core_bind.cpp 中关于 vsnprintf 的代码片段，因为它通常涉及字符串格式化。

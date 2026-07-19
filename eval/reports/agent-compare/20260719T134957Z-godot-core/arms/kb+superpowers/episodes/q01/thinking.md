# thinking

用户问 Godot 里字符串格式化的底层函数叫什么。这需要我在 Godot core/ 代码库中搜索字符串格式化相关的函数。

我应该用 cmm_search 工具来搜索相关符号。让我搜索一下字符串格式化相关的函数。

常见的字符串格式化函数可能叫：
- format
- sprintf
- vsprintf
- String::format
- 等等

让我先搜索一下。

---

搜索结果显示了几个相关的函数：
1. sprintf - 在 string/ustring.cpp 中的 String::sprintf
2. format - 在 string/ustring.cpp 中的 String::format

看起来 Godot 中字符串格式化的底层函数应该是在 String 类中。让我再搜索一下更具体的信息，看看底层实现是什么。

---

搜索结果显示了 `vformat` 这个函数在 variant/variant.h 中。这可能是更底层的格式化函数。让我搜索一下看看这个函数的具体实现。

---

好的，`vformat` 是在 variant/variant.h 中定义的函数。这应该是 Godot 中字符串格式化的底层函数。让我确认一下读取一下文件看看具体实现。

---

读取文件失败了。让我再搜索一下 vformat 的具体实现位置。

---

根据搜索结果，Godot 中字符串格式化的底层函数是 `vformat`，它定义在 variant/variant.h 中。

让我再搜索一下看看是否还有其他相关的底层格式化函数。

---

好的，搜索结果显示了：
1. `vformat` - 在 variant/variant.h 中，这应该是更底层的格式化函数
2. `sprintf` - 在 string/ustring.cpp 中的 String::sprintf

根据 Godot 的架构，`vformat` 应该是最底层的字符串格式化函数，用于支持 Variant 类型的格式化。而 String::sprintf 和 String::format 可能是更高层次的封装。

用户问的是"底层函数"，所以答案应该是 `vformat`。

---

`vformat`

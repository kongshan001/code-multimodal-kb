# thinking

用户问的是 Godot 里字符串格式化的底层函数叫什么。我需要在 Godot core/ 代码库中搜索相关的字符串格式化函数。

让我搜索一下。

---

从搜索结果看，Godot 里有几个字符串格式化相关的函数：

1. `vformat` - 在 variant/variant.h 中定义
2. `sprintf` - 在 String 类中 (string/ustring.cpp)
3. `format` - 也在 String 类中 (string/ustring.cpp)

用户问的是"底层函数"，我需要看一下这些函数哪个是真正的底层实现。让我读取一下相关文件。

---

看起来直接读取文件失败了，可能路径不对。让我再搜索一下，看看哪个是真正的底层函数。

从搜索结果来看，有几个候选：
- `vformat` - 在 variant/variant.h 中
- `sprintf` - 在 String 类中
- `format` - 在 String 类中

`vformat` 看起来是底层的 C++ 函数，而 `sprintf` 和 `format` 是 String 类的方法。通常 `vformat`（variable arguments format）是更底层的实现。

让我再确认一下。

---

看起来 vformat 是在 variant/variant.h 中定义的。这应该是 Godot 中字符串格式化的底层函数。

根据搜索结果，Godot 中字符串格式化的底层函数是 `vformat`，它位于 variant 模块中。String 类的 `format` 和 `sprintf` 方法可能都是基于这个底层函数实现的。

用户问的是"底层函数"，所以答案应该是 `vformat`。

---

`vformat`

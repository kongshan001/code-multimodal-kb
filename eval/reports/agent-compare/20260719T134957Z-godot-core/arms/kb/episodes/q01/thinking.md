# thinking

用户想知道 Godot 里字符串格式化的底层函数叫什么。我需要在 Godot core/ 代码库中搜索与字符串格式化相关的函数。

常见的字符串格式化函数名可能包含 "format"、"sprintf"、"printf" 等关键词。让我搜索一下。

---

好的，找到了 `String.format` 这个函数。这是 String 类的一个方法。让我再看看是否有更底层的格式化实现。

---

找到了！Godot 中字符串格式化的底层函数是 `String.sprintf`。这是 String 类的一个方法，用于类似于 C 语言 sprintf 的格式化操作。

---

`String.sprintf`

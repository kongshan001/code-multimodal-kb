# thinking

用户想知道 Godot 中字符串格式化的底层函数名称。这是一个代码定位问题，我需要在 Godot core/ 中搜索相关的格式化函数。

我应该搜索与字符串格式化相关的关键词，比如 "format", "sprintf", "vformat" 等。

---

找到了！在 Godot 中字符串格式化的底层函数主要有：

1. `String.sprintf` - string/ustring.cpp 中
2. `String.format` - string/ustring.cpp 中
3. `vformat` - variant/variant.h 中

根据用户的问题（字符串格式化在某些 locale 边界情况下输出乱码），最可能相关的底层函数是 `String.sprintf` 和 `String.format`，它们都在 string/ustring.cpp 中实现。

另外还有 `vformat` 在 variant/variant.h 中。

用户问的是"底层函数叫什么"，我应该直接给出符号名称。根据搜索结果，核心的格式化函数是 `String.sprintf` 和 `String.format`。

---

`String.sprintf`、`String.format`、`vformat`

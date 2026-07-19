# thinking

用户问 Godot 里字符串格式化的底层函数名称。我需要用 cmm_search 工具来搜索相关的函数或类。

让我搜索一下字符串格式化相关的符号。

---

用户询问字符串格式化的底层函数名称。从搜索结果来看，有 `sprintf` 和 `format` 两个相关函数。这两个都在 `string/ustring.cpp` 中。

但用户问的是"底层格式化例程"，这可能是指更底层的 C 函数或内部实现函数。让我再搜索一下看看是否有更底层的实现，比如 `vsprintf`、`vsnprintf` 等标准 C 库函数的包装，或者 Godot 自己实现的底层格式化函数。

---

搜索结果有 `vformat`。让我也看一下 `ustring.cpp` 文件内容，确认底层实现。

---

路径可能不对，让我看看搜索结果中提到的完整路径。从搜索结果看是 `string/ustring.cpp`，可能需要完整的相对路径。让我直接搜索具体的函数实现。

---

好的，从搜索结果来看：
- `String::sprintf` - 在 string/ustring.cpp 中
- `String::format` - 在 string/ustring.cpp 中

用户问的是"底层格式化例程"，在 Godot 中，`String::sprintf` 和 `String::format` 是主要的字符串格式化方法。其中 `sprintf` 可能是更底层的实现，因为它包装了 C 的 `sprintf` 函数。

根据用户问题"字符串格式化在某些 locale 边界情况下输出乱码，疑是底层格式化例程的 bug"，用户指的应该是 `String::sprintf` 或 `String::format`。

让我提供答案。用户要的是符号名称。

---

`String::sprintf`, `String::format`

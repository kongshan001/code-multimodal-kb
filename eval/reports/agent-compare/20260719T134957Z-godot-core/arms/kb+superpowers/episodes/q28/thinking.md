# thinking

用户在问 Godot 中字符串格式化的底层函数叫什么。这需要我在 Godot 的核心代码库中查找字符串格式化相关的函数。

我应该搜索与字符串格式化相关的关键词，比如 "format"、"sprintf"、"string_format" 等。

让我先用 mcp__bench__cmm_search 来搜索相关函数。

---

看到了 `String.format` 这个函数，它位于 string/ustring.cpp 中。这应该是用户要找的字符串格式化底层函数。让我再搜索一下看看是否有更底层的实现，比如 vsprintf 或者类似的函数。

---

好的，我找到了 `String.sprintf` 这个函数。这应该是 Godot 中字符串格式化的核心函数。让我读一下这个文件的相关部分，确认一下这个函数的作用。

---

看起来路径不对。让我从搜索结果中提取正确的路径。搜索结果中显示的是：
- `String.format` 在 `string/ustring.cpp`
- `String.sprintf` 在 `string/ustring.cpp`

这说明文件路径应该是 `string/ustring.cpp`，但是这个文件可能不是在项目根目录下。让我用更完整的路径试试。或者我应该查看这个函数的具体信息。

基于搜索结果，我可以回答用户的问题了。Godot 中字符串格式化的底层函数主要是：
1. `String.format` - 用于格式化字符串
2. `String.sprintf` - 用于类似 C 风格的字符串格式化

这两个函数都在 `string/ustring.cpp` 中实现。

用户问的是"底层函数叫什么"，从搜索结果看，最核心的应该是 `String.sprintf` 和 `String.format`。

---

`String.sprintf` 和 `String.format`

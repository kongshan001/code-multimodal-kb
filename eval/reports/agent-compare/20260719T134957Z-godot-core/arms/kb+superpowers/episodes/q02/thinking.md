# thinking

用户问的是整数转成字符串用哪个函数。这是在 Godot 引擎的代码库（C++）中。我需要搜索相关的函数。

在 C++ 中，整数转字符串通常有几种方式：
- `itos()` - Godot 特有的函数
- `String::num()` - Godot 的 String 类方法
- `String::num_int64()` - 用于 64 位整数
- 标准库的 `std::to_string()`

让我先搜索一下 Godot 的代码库看看有哪些相关的函数。

---

这个搜索结果不太对，返回的是关于整数常量绑定的函数，不是整数转字符串的函数。让我换个搜索词，试试搜索 itos 或者 String::num。

---

好，找到了 `itos` 函数。让我再搜索一下 String::num 相关的函数。

---

很好，找到了几个相关的函数：
- `itos` - 应该是一个全局函数
- `String::num` - String 类的静态方法
- `String::num_int64` - 用于 64 位整数
- `String::num_uint64` - 用于无符号 64 位整数

让我读取一下 itos 的定义来确认一下。

---

路径可能不对。让我再搜索一下看看具体的路径。

---

看起来已经找到了相关函数。根据搜索结果，Godot 中整数转字符串的函数主要有：

1. `itos` - 全局函数
2. `String::num` - String 类的静态方法  
3. `String::num_int64` - 用于 64 位整数
4. `String::num_uint64` - 用于无符号 64 位整数

我应该直接回答用户，给出这些函数名。

---

`itos`、`String::num`、`String::num_int64`、`String::num_uint64`

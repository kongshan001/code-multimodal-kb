# thinking

用户问整数转成字符串用哪个函数。这是在Godot代码库（C++）中的问题。

我需要搜索相关的函数。在C++中，整数转字符串通常有几种方式：
1. itoa（非标准）
2. std::to_string（C++11标准）
3. sprintf/snprintf
4. stringstream
5. Godot可能有自己的工具函数

让我用语义检索搜索一下。

---

这些结果看起来不太对，都是关于整数常量绑定的，不是整数转字符串的转换函数。让我换个搜索词。

---

这些是字符串转整数的函数（to_int等），不是整数转字符串的。让我搜索更直接的关键词。

---

很好！找到了！在Godot中，整数转字符串使用的是 `String::num` 相关的函数：
- `num` - 基本的数字转字符串
- `num_int64` - 64位整数转字符串
- `num_uint64` - 无符号64位整数转字符串
- `num_real` - 实数转字符串
- `num_scientific` - 科学计数法转字符串

用户问的是整数转字符串，所以应该是 `String::num`、`String::num_int64` 或 `String::num_uint64`。

根据收敛纪律，我应该立刻用符号名作答。

---

`String::num`、`String::num_int64`、`String::num_uint64`

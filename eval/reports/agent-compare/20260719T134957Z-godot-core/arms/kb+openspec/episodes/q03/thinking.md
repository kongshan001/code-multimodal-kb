# thinking

用户问"删除对象、释放内存用哪个函数？"，这是关于 Godot 代码库的问题。

根据指令，我需要：
1. 使用工具查找相关符号
2. 直接用符号名作答，不要长解释
3. 一旦工具返回了相关符号就立刻用符号名作答

我需要在 Godot core/ 中搜索删除对象、释放内存相关的函数。常见的函数名可能是 `free`, `delete`, `destroy`, `release` 等。

让我搜索相关的函数。

---

搜索结果显示了几个相关的函数：
- operator delete
- delete_allocation
- free_static
- free
- free_aligned_static

用户问的是"删除对象、释放内存用哪个函数"，从结果来看：
- `operator delete` 是 C++ 标准的删除操作符
- `free` 是释放内存的函数
- `free_static` 和 `free_aligned_static` 是特定场景的释放函数

根据用户的问题"删除对象、释放内存"，最直接的答案是 `operator delete`（用于对象）和 `free`（用于内存）。

但我应该给出最核心的符号名。从 Godot 的设计来看，删除对象和释放内存有不同的函数。

让我再确认一下是否有更具体的类或方法。不过用户问的是函数，所以我应该直接回答函数名。

从结果来看，主要的函数是：
- `operator delete` - 用于删除对象
- `free` - 用于释放内存

我应该给出这两个符号名作为答案。

---

`operator delete`, `free`

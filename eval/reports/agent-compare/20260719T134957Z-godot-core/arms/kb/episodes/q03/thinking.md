# thinking

用户问的是"删除对象、释放内存用哪个函数？"，这是一个关于Godot代码库的问题。我需要在Godot core/中搜索相关的内存管理/删除对象的函数。

在Godot中，常见的删除对象、释放内存的函数可能是：
- `memdelete` 
- `memfree`
- `delete` 
- `free`
- `Memory::free` 或类似的

让我搜索一下相关函数。

---

找到了几个相关的函数：
1. `memdelete` - 这是主要的删除对象的函数
2. `memdelete_allocator` - 使用分配器删除
3. `memdelete_arr` - 删除数组
4. `operator delete` - C++默认的删除运算符

其中最常用的是 `memdelete`，这是Godot中删除对象、释放内存的主要函数。

按照指示，我应该直接用符号名作答，不要长解释。

---

`memdelete`

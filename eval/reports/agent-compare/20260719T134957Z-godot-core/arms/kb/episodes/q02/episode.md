# q02 · code_retrieval · arm: `kb`

- **题**：整数转成字符串用哪个函数？
- **gold**：itos
- **答对**：✗
- **答案**：`String::num`、`String::num_int64`、`String::num_uint64`
- **指标**：tokens=4979 · llm_calls=4 · tool_steps=3 · 耗时=11.7s · 截断=否

---

**👤 用户**：整数转成字符串用哪个函数？

> 💭 **思考**：用户问整数转成字符串用哪个函数。这是在Godot代码库（C++）中的问题。

我需要搜索相关的函数。在C++中，整数转字符串通常有几种方式：
1. itoa（非标准）
2. std::to_string（C++11标准）
3. sprintf/snprintf
4. stringstream
5. Godot可能有自己的工具函数

让我用语义检索搜索一下。

**🔧 `cmm_search`**({"query": "整数转字符串 integer to string conversion"})

> 💭 **思考**：这些结果看起来不太对，都是关于整数常量绑定的，不是整数转字符串的转换函数。让我换个搜索词。

**🔧 `cmm_search`**({"query": "itoa int to string convert"})

> 💭 **思考**：这些是字符串转整数的函数（to_int等），不是整数转字符串的。让我搜索更直接的关键词。

**🔧 `cmm_search`**({"query": "num num_string number string conversion"})

> 💭 **思考**：很好！找到了！在Godot中，整数转字符串使用的是 `String::num` 相关的函数：
- `num` - 基本的数字转字符串
- `num_int64` - 64位整数转字符串
- `num_uint64` - 无符号64位整数转字符串
- `num_real` - 实数转字符串
- `num_scientific` - 科学计数法转字符串

用户问的是整数转字符串，所以应该是 `String::num`、`String::num_int64` 或 `String::num_uint64`。

根据收敛纪律，我应该立刻用符号名作答。

**🤖 Agent**：`String::num`、`String::num_int64`、`String::num_uint64`

**📋 工具结果**：
```
- bind_integer_constant  (Users-ks_128-Documents-godot-src-core.object.gdtype.GDType.bind_integer_constant)  object/gdtype.cpp
- bind_integer_constant  (Users-ks_128-Documents-godot-src-core.object.class_db.ClassDB.bind_integer_constant)  object/class_db.cpp
- get_integer_constant  (Users-ks_128-Documents-godot-src-core.object.class_db.ClassDB.get_integer_constant)  object/class_db.cpp
- has_integer_constant  (Users-ks_128-Documents-godot-src-core.object.class_db.ClassDB.has_integer_constant)  object/class_db.cpp
- class_has_integer_constant  (Users-ks_128-Documents-godot-src-core.core_bind.Cl
```

**📋 工具结果**：
```
- to_int  (Users-ks_128-Documents-godot-src-core.string.ustring.String.to_int)  string/ustring.cpp
- _to_int  (Users-ks_128-Documents-godot-src-core.string.ustring._to_int)  string/ustring.cpp
- hex_to_int  (Users-ks_128-Documents-godot-src-core.string.ustring.String.hex_to_int)  string/ustring.cpp
- bin_to_int  (Users-ks_128-Documents-godot-src-core.string.ustring.String.bin_to_int)  string/ustring.cpp
- convert_rgba8_to_bgra8  (Users-ks_128-Documents-godot-src-core.io.image.Image.convert_rgba8_to_bgra8)  io/image.cpp
```

**📋 工具结果**：
```
- num  (Users-ks_128-Documents-godot-src-core.string.ustring.String.num)  string/ustring.cpp
- num_int64  (Users-ks_128-Documents-godot-src-core.string.ustring.String.num_int64)  string/ustring.cpp
- num_uint64  (Users-ks_128-Documents-godot-src-core.string.ustring.String.num_uint64)  string/ustring.cpp
- num_real  (Users-ks_128-Documents-godot-src-core.string.ustring.String.num_real)  string/ustring.cpp
- num_scientific  (Users-ks_128-Documents-godot-src-core.string.ustring.String.num_scientific)  string/ustring.cpp
```


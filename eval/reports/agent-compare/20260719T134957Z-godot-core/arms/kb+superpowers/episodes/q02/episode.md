# q02 · code_retrieval · arm: `kb+superpowers`

- **题**：整数转成字符串用哪个函数？
- **gold**：itos
- **答对**：✓
- **答案**：`itos`、`String::num`、`String::num_int64`、`String::num_uint64`
- **指标**：tokens=10618 · llm_calls=6 · tool_steps=5 · 耗时=13.55s · 截断=否

---

**👤 用户**：整数转成字符串用哪个函数？

> 💭 **思考**：用户问的是整数转成字符串用哪个函数。这是在 Godot 引擎的代码库（C++）中。我需要搜索相关的函数。

在 C++ 中，整数转字符串通常有几种方式：
- `itos()` - Godot 特有的函数
- `String::num()` - Godot 的 String 类方法
- `String::num_int64()` - 用于 64 位整数
- 标准库的 `std::to_string()`

让我先搜索一下 Godot 的代码库看看有哪些相关的函数。

**🔧 `cmm_search`**({"query": "integer to string conversion"})

> 💭 **思考**：这个搜索结果不太对，返回的是关于整数常量绑定的函数，不是整数转字符串的函数。让我换个搜索词，试试搜索 itos 或者 String::num。

**🔧 `cmm_search`**({"query": "itos integer string conversion"})

> 💭 **思考**：好，找到了 `itos` 函数。让我再搜索一下 String::num 相关的函数。

**🔧 `cmm_search`**({"query": "String num integer"})

> 💭 **思考**：很好，找到了几个相关的函数：
- `itos` - 应该是一个全局函数
- `String::num` - String 类的静态方法
- `String::num_int64` - 用于 64 位整数
- `String::num_uint64` - 用于无符号 64 位整数

让我读取一下 itos 的定义来确认一下。

**🔧 `read_file`**({"path": "string/ustring.cpp"})

> 💭 **思考**：路径可能不对。让我再搜索一下看看具体的路径。

**🔧 `cmm_search`**({"query": "itos function definition"})

> 💭 **思考**：看起来已经找到了相关函数。根据搜索结果，Godot 中整数转字符串的函数主要有：

1. `itos` - 全局函数
2. `String::num` - String 类的静态方法  
3. `String::num_int64` - 用于 64 位整数
4. `String::num_uint64` - 用于无符号 64 位整数

我应该直接回答用户，给出这些函数名。

**🤖 Agent**：`itos`、`String::num`、`String::num_int64`、`String::num_uint64`

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
- itos  (Users-ks_128-Documents-godot-src-core.string.ustring.itos)  string/ustring.cpp
- bind_integer_constant  (Users-ks_128-Documents-godot-src-core.object.gdtype.GDType.bind_integer_constant)  object/gdtype.cpp
- bind_integer_constant  (Users-ks_128-Documents-godot-src-core.object.class_db.ClassDB.bind_integer_constant)  object/class_db.cpp
- get_integer_constant  (Users-ks_128-Documents-godot-src-core.object.class_db.ClassDB.get_integer_constant)  object/class_db.cpp
- has_integer_constant  (Users-ks_128-Documents-godot-src-core.object.class_db.ClassDB.has_integer_constant)  object/class_
```

**📋 工具结果**：
```
- num  (Users-ks_128-Documents-godot-src-core.string.ustring.String.num)  string/ustring.cpp
- num_int64  (Users-ks_128-Documents-godot-src-core.string.ustring.String.num_int64)  string/ustring.cpp
- num_uint64  (Users-ks_128-Documents-godot-src-core.string.ustring.String.num_uint64)  string/ustring.cpp
- num_real  (Users-ks_128-Documents-godot-src-core.string.ustring.String.num_real)  string/ustring.cpp
- num_scientific  (Users-ks_128-Documents-godot-src-core.string.ustring.String.num_scientific)  string/ustring.cpp
```

**📋 工具结果**：
```
(read error: [Errno 2] No such file or directory: 'string/ustring.cpp')
```

**📋 工具结果**：
```
- itos  (Users-ks_128-Documents-godot-src-core.string.ustring.itos)  string/ustring.cpp
- _ignore_definition  (Users-ks_128-Documents-godot-src-core.io.xml_parser.XMLParser._ignore_definition)  io/xml_parser.cpp
- MethodDefinition  (Users-ks_128-Documents-godot-src-core.object.class_db.MethodDefinition.MethodDefinition)  object/class_db.h
- set_initialization_function  (Users-ks_128-Documents-godot-src-core.extension.gdextension_function_loader.GDExtensionFunctionLoader.set_initialization_function)  extension/gdextension_function_loader.cpp
- register_utility_function  (Users-ks_128-Documents-
```


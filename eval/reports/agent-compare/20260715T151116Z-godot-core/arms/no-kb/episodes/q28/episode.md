# q28 · bug_fix · arm: `no-kb`

**题**：字符串格式化在某些 locale 边界情况下输出乱码，疑是底层格式化例程的 bug。Godot 里字符串格式化的底层函数叫什么？  ·  **gold**：core/string/print_string.cpp, vformat
**答对**：✗  ·  **答案**：Godot 字符串格式化的底层函数有两个：

- **`String::format(const Variant &p_values, const String &p_placeholder)`** — 基于占位符的格式化（`"Hello 
**指标**：tokens=2169 · llm_calls=10 · tool_steps=9 · 耗时=33.27s · 截断=否

---

**👤 用户**：字符串格式化在某些 locale 边界情况下输出乱码，疑是底层格式化例程的 bug。Godot 里字符串格式化的底层函数叫什么？

> 💭 **思考**：The user is asking about the underlying function for string formatting in Godot. Let me search for it.

**🔧 `grep_code`**({"pattern": "String format"})

**🔧 `grep_code`**({"pattern": "sprintf"})

> 💭 **思考**：Let me look at the ustring.h to find the format/sprintf function declarations.

**🔧 `grep_code`**({"pattern": "String\\s+(format|sprintf)\\s*\\("})

**🔧 `grep_code`**({"pattern": "format\\("})

**🔧 `grep_code`**({"pattern": "sprintf\\("})

**🔧 `read_file`**({"path": "core/string/ustring.h"})

**🔧 `read_file`**({"path": "/Users/ks_128/Documents/godot-src/core/string/ustring.h"})

> 💭 **思考**：The file is large. Let me search for format/sprintf in ustring.cpp to find the actual implementation.

**🔧 `grep_code`**({"pattern": "String String::format"})

**🔧 `grep_code`**({"pattern": "String String::sprintf"})

**🤖 Agent**：Godot 字符串格式化的底层函数有两个：

- **`String::format(const Variant &p_values, const String &p_placeholder)`** — 基于占位符的格式化（`"Hello {0}".format(["World"])`）
- **`String::sprintf(const Array &p_values, bool p_error)`** — C 风格的 `sprintf` 格式化（`"%s %d".sprintf(["Hello", 42])`）

两者均在 `core/string/ustring.cpp` 中实现。lo

**📋 工具结果**：
```
matched 7 files:
/Users/ks_128/Documents/godot-src/core/extension/gdextension_interface_header_generator.h
/Users/ks_128/Documents/godot-src/core/object/script_backtrace.h
/Users/ks_128/Documents/godot-src/core/variant/variant_op.h
/Users/ks_128/Documents/godot-src/core/os/time.cpp
/Users/ks_128/Documents/godot-src/core/string/ustring.h
/Users/ks_128/Documents/godot-src/core/string/translation_server.h
/Users/ks_128/Documents/godot-src/core/string/ustring.cpp
```

**📋 工具结果**：
```
matched 5 files:
/Users/ks_128/Documents/godot-src/core/io/logger.cpp
/Users/ks_128/Documents/godot-src/core/variant/variant_op.h
/Users/ks_128/Documents/godot-src/core/variant/variant.h
/Users/ks_128/Documents/godot-src/core/string/ustring.h
/Users/ks_128/Documents/godot-src/core/string/ustring.cpp
```

**📋 工具结果**：
```
(no matches)
```

**📋 工具结果**：
```
(no matches)
```

**📋 工具结果**：
```
(no matches)
```

**📋 工具结果**：
```
(read error: [Errno 2] No such file or directory: 'core/string/ustring.h')
```

**📋 工具结果**：
```
/**************************************************************************/
/*  ustring.h                                                             */
/**************************************************************************/
/*                         This file is part of:                          */
/*                             GODOT ENGINE                               */
/*                        https://godotengine.org                         */
/**************************************************************************/
/* Copyright (c) 2014-present Godot Engine contributors (see 
```

**📋 工具结果**：
```
matched 1 files:
/Users/ks_128/Documents/godot-src/core/string/ustring.cpp
```

**📋 工具结果**：
```
matched 1 files:
/Users/ks_128/Documents/godot-src/core/string/ustring.cpp
```


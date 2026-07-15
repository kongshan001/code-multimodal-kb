# q01 · code_retrieval · arm: `no-kb`

**题**：Godot 里字符串格式化的底层函数叫什么？  ·  **gold**：vformat
**答对**：✗  ·  **答案**：Godot 字符串格式化的底层函数主要有两个，都在 `String` 类（`core/string/ustring.h` / `ustring.cpp`）中：

1. **`String::format()`** — 基于占位符（如 `{0
**指标**：tokens=5220 · llm_calls=9 · tool_steps=12 · 耗时=43.33s · 截断=否

---

**👤 用户**：Godot 里字符串格式化的底层函数叫什么？

**🔧 `grep_code`**({"pattern": "String format"})

**🔧 `grep_code`**({"pattern": "format_string"})

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
matched 1 files:
/Users/ks_128/Documents/godot-src/core/os/time.cpp
```

**🔧 `grep_code`**({"pattern": "String::format"})

**🔧 `grep_code`**({"pattern": "sprintf"})

**📋 工具结果**：
```
matched 1 files:
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

**🔧 `grep_code`**({"pattern": "String sprintf"})

**📋 工具结果**：
```
matched 1 files:
/Users/ks_128/Documents/godot-src/core/string/ustring.h
```

**🔧 `read_file`**({"path": "/Users/ks_128/Documents/godot-src/core/string/ustring.h"})

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

**🔧 `grep_code`**({"pattern": "String format\\("})

**🔧 `grep_code`**({"pattern": "String sprintf\\("})

**📋 工具结果**：
```
(no matches)
```

**📋 工具结果**：
```
(no matches)
```

**🔧 `grep_code`**({"pattern": "format\\("})

**📋 工具结果**：
```
(no matches)
```

**🔧 `read_file`**({"path": "/Users/ks_128/Documents/godot-src/core/string/ustring.cpp"})

**📋 工具结果**：
```
/**************************************************************************/
/*  ustring.cpp                                                           */
/**************************************************************************/
/*                         This file is part of:                          */
/*                             GODOT ENGINE                               */
/*                        https://godotengine.org                         */
/**************************************************************************/
/* Copyright (c) 2014-present Godot Engine contributors (see 
```

**🔧 `grep_code`**({"pattern": "String String::format"})

**🔧 `grep_code`**({"pattern": "String String::sprintf"})

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

**🤖 Agent**：Godot 字符串格式化的底层函数主要有两个，都在 `String` 类（`core/string/ustring.h` / `ustring.cpp`）中：

1. **`String::format()`** — 基于占位符（如 `{0}`, `{1}` 或字典键）的格式化，对应 GDScript 的 `"...".format(values)`。
2. **`String::sprintf()`** — 类 C 的 `sprintf` 风格格式化，对应 GDScript 的 `"..." % values`。

两者都是 `String` 类的成员函数，定义在 `core/string/


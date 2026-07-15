# q28 · bug_fix · arm: `no-kb`

**题**：字符串格式化在某些 locale 边界情况下输出乱码，疑是底层格式化例程的 bug。Godot 里字符串格式化的底层函数叫什么？  ·  **gold**：core/string/print_string.cpp, vformat
**答对**：✓  ·  **答案**：Godot 字符串格式化的底层函数主要有两个，都在 `core/string/ustring.cpp` 中：

1. **`String::sprintf`** — 底层 C 风格格式化例程（`%s`、`%d`、`%f` 等），是实际执行格
**指标**：tokens=3903 · llm_calls=4 · tool_steps=6 · 耗时=17.51s · 截断=否

---

**👤 用户**：字符串格式化在某些 locale 边界情况下输出乱码，疑是底层格式化例程的 bug。Godot 里字符串格式化的底层函数叫什么？

**🔧 `grep_code`**({"pattern": "String format"})

**🔧 `grep_code`**({"pattern": "vformat"})

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
matched 20 files:
/Users/ks_128/Documents/godot-src/core/crypto/crypto_resource_format.cpp
/Users/ks_128/Documents/godot-src/core/crypto/crypto_core.cpp
/Users/ks_128/Documents/godot-src/core/extension/gdextension_interface.cpp
/Users/ks_128/Documents/godot-src/core/extension/gdextension_interface_header_generator.cpp
/Users/ks_128/Documents/godot-src/core/extension/gdextension_library_loader.cpp
/Users/ks_128/Documents/godot-src/core/extension/gdextension.cpp
/Users/ks_128/Documents/godot-src/core/extension/gdextension_manager.cpp
/Users/ks_128/Documents/godot-src/core/extension/extension_api
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

**🔧 `read_file`**({"path": "/Users/ks_128/Documents/godot-src/core/string/ustring.h"})

**📋 工具结果**：
```
matched 1 files:
/Users/ks_128/Documents/godot-src/core/string/ustring.h
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

**🤖 Agent**：Godot 字符串格式化的底层函数主要有两个，都在 `core/string/ustring.cpp` 中：

1. **`String::sprintf`** — 底层 C 风格格式化例程（`%s`、`%d`、`%f` 等），是实际执行格式化解析与替换的核心实现，locale 边界问题最可能出在这里。
2. **`String::format`** — Godot 自己的占位符格式化（`{}` / `{index}` 风格），内部最终也会走到字符串拼接逻辑。

另外还有一个全局辅助函数 **`vformat`**（定义在 `core/variant/variant.h`），它是对 `Stri


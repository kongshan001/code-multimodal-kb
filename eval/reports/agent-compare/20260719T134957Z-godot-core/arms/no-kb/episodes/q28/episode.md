# q28 · bug_fix · arm: `no-kb`

- **题**：字符串格式化在某些 locale 边界情况下输出乱码，疑是底层格式化例程的 bug。Godot 里字符串格式化的底层函数叫什么？
- **gold**：core/string/print_string.cpp, vformat
- **答对**：✗
- **答案**：我来搜索 Godot 中的字符串格式化底层函数。
- **指标**：tokens=29311 · llm_calls=19 · tool_steps=18 · 耗时=26.75s · 截断=⚠是

---

**👤 用户**：字符串格式化在某些 locale 边界情况下输出乱码，疑是底层格式化例程的 bug。Godot 里字符串格式化的底层函数叫什么？

> 💭 **思考**：用户在问 Godot 中字符串格式化的底层函数叫什么。我需要在 Godot core/ 源码中搜索字符串格式化相关的函数。

常见的字符串格式化函数可能包含：
- format
- sprintf
- vsnprintf
- String::format
- vformat

让我先搜索一些相关的模式。

**🤖 Agent**：我来搜索 Godot 中的字符串格式化底层函数。

**🔧 `grep_code`**({"pattern": "String::format"})

**🔧 `grep_code`**({"pattern": "vformat"})

**🔧 `grep_code`**({"pattern": "String.*sprintf"})

> 💭 **思考**：好，我看到 `String::format` 在 ustring.cpp 中，vformat 在很多文件中使用。让我查看 ustring.h 和 ustring.cpp 中的格式化函数定义。

**🔧 `read_file`**({"path": "core/string/ustring.h"})

> 💭 **思考**：需要用完整路径。

**🔧 `read_file`**({"path": "/Users/ks_128/Documents/godot-src/core/string/ustring.h"})

> 💭 **思考**：让我搜索 format 函数的实际定义。我应该读取 ustring.cpp 来找到具体的底层函数。

**🔧 `grep_code`**({"pattern": "String.*format.*\\("})

**🔧 `grep_code`**({"pattern": "_sprintf"})

**🔧 `grep_code`**({"pattern": "vformat.*\\("})

> 💭 **思考**：让我直接搜索更广泛的模式来找到格式化相关的函数。

**🔧 `grep_code`**({"pattern": "\\basprintf\\b"})

**🔧 `grep_code`**({"pattern": "\\bvsnprintf\\b"})

**🔧 `grep_code`**({"pattern": "\\bformat\\b"})

> 💭 **思考**：让我读取 core_bind.cpp，它里面可能有 format 的实现。另外也可以看看 logger.cpp。

**🔧 `read_file`**({"path": "/Users/ks_128/Documents/godot-src/core/core_bind.cpp"})

> 💭 **思考**：让我直接搜索 format 和 vsnprintf 的使用位置。

**🔧 `grep_code`**({"pattern": "vsnprintf"})

> 💭 **思考**：让我读取 logger.cpp 和 core_bind.cpp 中 vsnprintf 的相关代码片段。

**🔧 `grep_code`**({"pattern": "String\\s+format"})

> 💭 **思考**：让我直接读取 ustring.cpp 文件看看。

**🔧 `read_file`**({"path": "/Users/ks_128/Documents/godot-src/core/string/ustring.cpp"})

> 💭 **思考**：让我搜索一下 Godot 代码库中更具体的字符串格式化函数。让我尝试搜索 "_format" 或者 "sprintf" 之类的。

**🔧 `grep_code`**({"pattern": "_format"})

> 💭 **思考**：这些主要是 resource_format 相关的，不是字符串格式化。让我搜索 "vformat" 或者看看 core_bind.cpp 中的具体实现。

**🔧 `grep_code`**({"pattern": "vformat"})

> 💭 **思考**：让我直接看 core_bind.cpp 中关于 vsnprintf 的代码片段，因为它通常涉及字符串格式化。

**🔧 `grep_code`**({"pattern": "vsnprintf.*format"})

**📋 工具结果**：
```
matched 1 files:
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

**📋 工具结果**：
```
matched 4 files:
/Users/ks_128/Documents/godot-src/core/variant/variant_op.h
/Users/ks_128/Documents/godot-src/core/variant/variant.h
/Users/ks_128/Documents/godot-src/core/string/ustring.h
/Users/ks_128/Documents/godot-src/core/string/ustring.cpp
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
(no matches)
```

**📋 工具结果**：
```
matched 2 files:
/Users/ks_128/Documents/godot-src/core/io/logger.cpp
/Users/ks_128/Documents/godot-src/core/core_bind.cpp
```

**📋 工具结果**：
```
matched 20 files:
/Users/ks_128/Documents/godot-src/core/extension/extension_api_dump.cpp
/Users/ks_128/Documents/godot-src/core/extension/gdextension_special_compat_hashes.cpp
/Users/ks_128/Documents/godot-src/core/typedefs.h
/Users/ks_128/Documents/godot-src/core/config/project_settings.cpp
/Users/ks_128/Documents/godot-src/core/input/input_map.cpp
/Users/ks_128/Documents/godot-src/core/io/file_access_pack.h
/Users/ks_128/Documents/godot-src/core/io/resource_importer.cpp
/Users/ks_128/Documents/godot-src/core/io/image.cpp
/Users/ks_128/Documents/godot-src/core/io/resource_loader.cpp
/Users/k
```

**📋 工具结果**：
```
/**************************************************************************/
/*  core_bind.cpp                                                         */
/**************************************************************************/
/*                         This file is part of:                          */
/*                             GODOT ENGINE                               */
/*                        https://godotengine.org                         */
/**************************************************************************/
/* Copyright (c) 2014-present Godot Engine contributors (see 
```

**📋 工具结果**：
```
matched 2 files:
/Users/ks_128/Documents/godot-src/core/io/logger.cpp
/Users/ks_128/Documents/godot-src/core/core_bind.cpp
```

**📋 工具结果**：
```
(no matches)
```

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

**📋 工具结果**：
```
matched 20 files:
/Users/ks_128/Documents/godot-src/core/crypto/crypto_resource_format.cpp
/Users/ks_128/Documents/godot-src/core/crypto/crypto_resource_format.h
/Users/ks_128/Documents/godot-src/core/extension/gdextension_resource_format.cpp
/Users/ks_128/Documents/godot-src/core/extension/gdextension_special_compat_hashes.cpp
/Users/ks_128/Documents/godot-src/core/extension/gdextension_resource_format.h
/Users/ks_128/Documents/godot-src/core/typedefs.h
/Users/ks_128/Documents/godot-src/core/io/image_loader.h
/Users/ks_128/Documents/godot-src/core/io/file_access_pack.h
/Users/ks_128/Documents
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

**📋 工具结果**：
```
matched 2 files:
/Users/ks_128/Documents/godot-src/core/io/logger.cpp
/Users/ks_128/Documents/godot-src/core/core_bind.cpp
```


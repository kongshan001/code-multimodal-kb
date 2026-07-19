# q25 · code_retrieval · arm: `no-kb`

- **题**：翻译/本地化服务器用哪个类？
- **gold**：TranslationServer
- **答对**：✓
- **答案**：`TranslationServer`
- **指标**：tokens=5200 · llm_calls=5 · tool_steps=4 · 耗时=21.0s · 截断=否

---

**👤 用户**：翻译/本地化服务器用哪个类？

> 💭 **思考**：用户问"翻译/本地化服务器用哪个类？"，这是在问 Godot 4.7 core/ 中关于翻译/本地化相关的类。

让我搜索相关的代码。Godot 的翻译/本地化系统通常涉及 TranslationServer 类。让我用 grep 来查找相关代码。

**🔧 `grep_code`**({"pattern": "TranslationServer"})

**🔧 `grep_code`**({"pattern": "class.*Translation"})

> 💭 **思考**：太好了！找到了相关的文件。翻译/本地化服务器的类名是 `TranslationServer`。让我确认一下这个类的定义。

**🔧 `read_file`**({"path": "core/string/translation_server.h"})

> 💭 **思考**：路径问题，让我用完整路径试试。

**🔧 `read_file`**({"path": "/Users/ks_128/Documents/godot-src/core/string/translation_server.h"})

> 💭 **思考**：根据搜索结果和读取的文件，翻译/本地化服务器使用的是 `TranslationServer` 类。

现在可以给出答案了，用符号名直接作答。

**🤖 Agent**：`TranslationServer`

**📋 工具结果**：
```
matched 10 files:
/Users/ks_128/Documents/godot-src/core/extension/gdextension_special_compat_hashes.cpp
/Users/ks_128/Documents/godot-src/core/io/resource_loader.cpp
/Users/ks_128/Documents/godot-src/core/object/object.cpp
/Users/ks_128/Documents/godot-src/core/string/translation_domain.h
/Users/ks_128/Documents/godot-src/core/string/translation_domain.cpp
/Users/ks_128/Documents/godot-src/core/string/translation_server.cpp
/Users/ks_128/Documents/godot-src/core/string/translation_server.h
/Users/ks_128/Documents/godot-src/core/string/translation.cpp
/Users/ks_128/Documents/godot-src/core/str
```

**📋 工具结果**：
```
matched 11 files:
/Users/ks_128/Documents/godot-src/core/io/translation_loader_po.h
/Users/ks_128/Documents/godot-src/core/object/object.cpp
/Users/ks_128/Documents/godot-src/core/string/translation_domain.h
/Users/ks_128/Documents/godot-src/core/string/translation_domain.cpp
/Users/ks_128/Documents/godot-src/core/string/translation.h
/Users/ks_128/Documents/godot-src/core/string/translation_server.cpp
/Users/ks_128/Documents/godot-src/core/string/optimized_translation.cpp
/Users/ks_128/Documents/godot-src/core/string/translation_server.h
/Users/ks_128/Documents/godot-src/core/string/translati
```

**📋 工具结果**：
```
(read error: [Errno 2] No such file or directory: 'core/string/translation_server.h')
```

**📋 工具结果**：
```
/**************************************************************************/
/*  translation_server.h                                                  */
/**************************************************************************/
/*                         This file is part of:                          */
/*                             GODOT ENGINE                               */
/*                        https://godotengine.org                         */
/**************************************************************************/
/* Copyright (c) 2014-present Godot Engine contributors (see 
```


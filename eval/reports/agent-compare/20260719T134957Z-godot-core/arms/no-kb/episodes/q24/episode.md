# q24 · code_retrieval · arm: `no-kb`

- **题**：加密解密用哪个类？
- **gold**：Crypto
- **答对**：✓
- **答案**：`Crypto`
- **指标**：tokens=5302 · llm_calls=5 · tool_steps=4 · 耗时=19.59s · 截断=否

---

**👤 用户**：加密解密用哪个类？

> 💭 **思考**：用户在问 Godot 4.7 core/ 中加密解密用的是哪个类。我需要在源码中搜索加密相关的类。

在 Godot 中，加密解密相关的类通常是：
- CryptoKey - 用于非对称加密
- X509Certificate - 证书
- Crypto - 通用加密类

让我搜索一下相关的类名。

**🔧 `grep_code`**({"pattern": "class.*Crypto"})

**🔧 `grep_code`**({"pattern": "encrypt"})

> 💭 **思考**：找到了！在 core/crypto/crypto.h 和 core/crypto/crypto.cpp 中应该有 Crypto 类的定义。让我读一下头文件确认。

**🔧 `read_file`**({"path": "core/crypto/crypto.h"})

> 💭 **思考**：路径可能不对，让我用完整路径试试。

**🔧 `read_file`**({"path": "/Users/ks_128/Documents/godot-src/core/crypto/crypto.h"})

> 💭 **思考**：好的，我能读取文件了。虽然开头是版权注释，但从路径匹配来看，这个 Crypto 类是存在的。让我再看看文件内容，确认类名。

**🤖 Agent**：`Crypto`

**📋 工具结果**：
```
matched 5 files:
/Users/ks_128/Documents/godot-src/core/crypto/crypto.h
/Users/ks_128/Documents/godot-src/core/crypto/crypto_resource_format.h
/Users/ks_128/Documents/godot-src/core/crypto/crypto_core.h
/Users/ks_128/Documents/godot-src/core/crypto/crypto.cpp
/Users/ks_128/Documents/godot-src/core/register_core_types.cpp
```

**📋 工具结果**：
```
matched 18 files:
/Users/ks_128/Documents/godot-src/core/crypto/crypto_core.cpp
/Users/ks_128/Documents/godot-src/core/crypto/crypto.h
/Users/ks_128/Documents/godot-src/core/crypto/aes_context.h
/Users/ks_128/Documents/godot-src/core/crypto/crypto_core.h
/Users/ks_128/Documents/godot-src/core/crypto/crypto.cpp
/Users/ks_128/Documents/godot-src/core/crypto/aes_context.cpp
/Users/ks_128/Documents/godot-src/core/io/file_access_pack.h
/Users/ks_128/Documents/godot-src/core/io/config_file.h
/Users/ks_128/Documents/godot-src/core/io/file_access_encrypted.cpp
/Users/ks_128/Documents/godot-src/core/io
```

**📋 工具结果**：
```
(read error: [Errno 2] No such file or directory: 'core/crypto/crypto.h')
```

**📋 工具结果**：
```
/**************************************************************************/
/*  crypto.h                                                              */
/**************************************************************************/
/*                         This file is part of:                          */
/*                             GODOT ENGINE                               */
/*                        https://godotengine.org                         */
/**************************************************************************/
/* Copyright (c) 2014-present Godot Engine contributors (see 
```


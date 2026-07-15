# q24 · code_retrieval · arm: `no-kb`

**题**：加密解密用哪个类？  ·  **gold**：Crypto
**答对**：✓  ·  **答案**：加密解密主要用以下类：

- **`Crypto`** — 高层加密接口，提供 AES-256-CBC 加解密、HMAC、随机数生成、RSA 密钥生成/签名等功能。
- **`CryptoCore`** — 底层加密原语（MD5、SHA-1
**指标**：tokens=1617 · llm_calls=3 · tool_steps=2 · 耗时=14.96s · 截断=否

---

**👤 用户**：加密解密用哪个类？

**🔧 `grep_code`**({"pattern": "class Crypto"})

**📋 工具结果**：
```
matched 2 files:
/Users/ks_128/Documents/godot-src/core/crypto/crypto.h
/Users/ks_128/Documents/godot-src/core/crypto/crypto_core.h
```

**🔧 `read_file`**({"path": "/Users/ks_128/Documents/godot-src/core/crypto/crypto.h"})

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

**🤖 Agent**：加密解密主要用以下类：

- **`Crypto`** — 高层加密接口，提供 AES-256-CBC 加解密、HMAC、随机数生成、RSA 密钥生成/签名等功能。
- **`CryptoCore`** — 底层加密原语（MD5、SHA-1、SHA-256、AES-256 等）。

相关辅助类：
- **`CryptoKey`** — RSA 密钥的加载/保存。
- **`X509Certificate`** — X.509 证书处理。

日常使用直接用 **`Crypto`** 即可。


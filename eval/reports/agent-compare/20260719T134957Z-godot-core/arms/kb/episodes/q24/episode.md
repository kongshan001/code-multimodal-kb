# q24 · code_retrieval · arm: `kb`

- **题**：加密解密用哪个类？
- **gold**：Crypto
- **答对**：✓
- **答案**：`AESContext`, `Crypto`, `CryptoCore`, `CryptoKey`
- **指标**：tokens=11196 · llm_calls=8 · tool_steps=7 · 耗时=18.43s · 截断=否

---

**👤 用户**：加密解密用哪个类？

> 💭 **思考**：用户问"加密解密用哪个类？"，这是在询问 Godot 代码库中用于加密解密的类。我需要搜索相关的类或符号。

让我搜索一下加密解密相关的代码。

**🔧 `cmm_search`**({"query": "加密 解密 encrypt decrypt"})

> 💭 **思考**：没有找到结果。让我尝试用英文关键词搜索。

**🔧 `cmm_search`**({"query": "crypto cipher aes encryption"})

> 💭 **思考**：很好，我找到了 AESContext 类，这个类是用于 AES 加密的。让我也搜索一下看看是否有其他加密相关的类，比如 Crypto 或者其他。

**🔧 `cmm_search`**({"query": "Crypto hash sha256 md5"})

> 💭 **思考**：我找到了 CryptoCore 和 AESContext 两个类。让我也看看是否有其他相关类。

**🔧 `cmm_search`**({"query": "CryptoKey X509"})

> 💭 **思考**：很好，我找到了几个与加密解密相关的类：
1. AESContext - 用于 AES 加密解密
2. CryptoCore - 用于哈希计算（SHA256, MD5）
3. CryptoKey - 用于密钥管理

用户问的是"加密解密用哪个类"，最直接的答案是 AESContext，因为它专门用于加密解密。CryptoCore 更多用于哈希，CryptoKey 用于密钥管理。

让我再搜索一下确认是否有更通用的 Crypto 类。

**🔧 `cmm_search`**({"query": "class Crypto encrypt decrypt"})

> 💭 **思考**：找到了 Crypto 类！让我再确认一下 Crypto 类的具体定义和功能。

**🔧 `read_file`**({"path": "crypto/crypto.h"})

> 💭 **思考**：文件路径可能不对，让我用完整的用户路径来读取。

**🔧 `read_file`**({"path": "Users-ks_128-Documents-godot-src-core/crypto/crypto.h"})

> 💭 **思考**：我需要提供正确的相对路径。让我基于之前搜索结果的路径来构建正确的路径。从搜索结果看，路径应该类似 "crypto/crypto.h"。不过由于文件读取有困难，让我直接基于搜索结果来回答。

根据搜索结果，Godot core 中的加密解密相关类有：
1. `AESContext` - 用于 AES 加密解密
2. `Crypto` - 通用加密功能类
3. `CryptoCore` - 哈希计算
4. `CryptoKey` - 密钥管理

用户问的是"加密解密用哪个类"，最直接的是 AESContext（用于对称加密）和 Crypto（通用加密类）。

**🤖 Agent**：`AESContext`, `Crypto`, `CryptoCore`, `CryptoKey`

**📋 工具结果**：
```
(no results)
```

**📋 工具结果**：
```
- start  (Users-ks_128-Documents-godot-src-core.crypto.aes_context.AESContext.start)  crypto/aes_context.cpp
- update  (Users-ks_128-Documents-godot-src-core.crypto.aes_context.AESContext.update)  crypto/aes_context.cpp
- finish  (Users-ks_128-Documents-godot-src-core.crypto.aes_context.AESContext.finish)  crypto/aes_context.cpp
- _bind_methods  (Users-ks_128-Documents-godot-src-core.crypto.aes_context.AESContext._bind_methods)  crypto/aes_context.cpp
- get_iv_state  (Users-ks_128-Documents-godot-src-core.crypto.aes_context.AESContext.get_iv_state)  crypto/aes_context.cpp
```

**📋 工具结果**：
```
- sha256  (Users-ks_128-Documents-godot-src-core.crypto.crypto_core.CryptoCore.sha256)  crypto/crypto_core.cpp
- md5  (Users-ks_128-Documents-godot-src-core.crypto.crypto_core.CryptoCore.md5)  crypto/crypto_core.cpp
- sha256_text  (Users-ks_128-Documents-godot-src-core.string.ustring.String.sha256_text)  string/ustring.cpp
- sha256_buffer  (Users-ks_128-Documents-godot-src-core.string.ustring.String.sha256_buffer)  string/ustring.cpp
- get_sha256  (Users-ks_128-Documents-godot-src-core.io.file_access.FileAccess.get_sha256)  io/file_access.cpp
```

**📋 工具结果**：
```
- create  (Users-ks_128-Documents-godot-src-core.crypto.crypto.CryptoKey.create)  crypto/crypto.cpp
- _bind_methods  (Users-ks_128-Documents-godot-src-core.crypto.crypto.CryptoKey._bind_methods)  crypto/crypto.cpp
- CryptoKey  (Users-ks_128-Documents-godot-src-core.crypto.crypto.CryptoKey)  crypto/crypto.h
```

**📋 工具结果**：
```
- create  (Users-ks_128-Documents-godot-src-core.crypto.crypto.Crypto.create)  crypto/crypto.cpp
- hmac_digest  (Users-ks_128-Documents-godot-src-core.crypto.crypto.Crypto.hmac_digest)  crypto/crypto.cpp
- _bind_methods  (Users-ks_128-Documents-godot-src-core.crypto.crypto.Crypto._bind_methods)  crypto/crypto.cpp
- load_default_certificates  (Users-ks_128-Documents-godot-src-core.crypto.crypto.Crypto.load_default_certificates)  crypto/crypto.cpp
- constant_time_compare  (Users-ks_128-Documents-godot-src-core.crypto.crypto.Crypto.constant_time_compare)  crypto/crypto.cpp
```

**📋 工具结果**：
```
(read error: [Errno 2] No such file or directory: 'crypto/crypto.h')
```

**📋 工具结果**：
```
(read error: [Errno 2] No such file or directory: 'Users-ks_128-Documents-godot-src-core/crypto/crypto.h')
```


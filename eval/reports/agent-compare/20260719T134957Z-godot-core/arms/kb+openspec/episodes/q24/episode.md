# q24 · code_retrieval · arm: `kb+openspec`

- **题**：加密解密用哪个类？
- **gold**：Crypto
- **答对**：✓
- **答案**：`Crypto`、`CryptoKey`
- **指标**：tokens=21028 · llm_calls=11 · tool_steps=10 · 耗时=16.66s · 截断=否

---

**👤 用户**：加密解密用哪个类？

> 💭 **思考**：用户问加密解密用哪个类，这是在问 Godot 代码库中的加密解密相关的类。我需要在 Godot core/ 中搜索相关的符号。

根据指示，我应该：
1. 使用 cmm_search 工具搜索加密解密相关的类
2. 一旦找到相关符号，就立即用符号名作答
3. 答案要简短，直接给类名

让我搜索一下加密解密相关的类。

**🔧 `cmm_search`**({"query": "加密 解密 encrypt decrypt"})

> 💭 **思考**：中文搜索没有结果，让我用英文搜索。

**🔧 `cmm_search`**({"query": "CryptoKey"})

> 💭 **思考**：找到了 CryptoKey，让我再搜索看看是否有其他加密相关的类，比如 Crypto 或 X509 等。

**🔧 `cmm_search`**({"query": "Crypto"})

> 💭 **思考**：搜索结果只显示了一些方法，让我直接搜索 Crypto 类本身的定义。

**🔧 `cmm_search`**({"query": "class Crypto encrypt decrypt"})

> 💭 **思考**：从之前的搜索结果可以看到有 CryptoKey 和 Crypto 类。让我查看一下 crypto.h 文件来确认主要的加密类名称。

**🔧 `read_file`**({"path": "crypto/crypto.h"})

> 💭 **思考**：路径可能不对，让我用搜索结果中的完整路径。

**🔧 `read_file`**({"path": "/Users/ks_128/Documents/godot-src/core/crypto/crypto.h"})

> 💭 **思考**：我需要搜索更具体的加密相关的类。从搜索结果来看，有 CryptoKey 和可能存在的 Crypto 类。让我直接搜索 Crypto 类的完整定义。

**🔧 `cmm_search`**({"query": "Crypto class core"})

> 💭 **思考**：从搜索结果中可以看出有 Crypto 类存在。让我再搜索一下是否有 X509 或其他证书相关的类。

**🔧 `cmm_search`**({"query": "X509"})

> 💭 **思考**：让我搜索 certificate 相关的类。

**🔧 `cmm_search`**({"query": "certificate cert"})

> 💭 **思考**：找到了 TLSOptions 类。让我再搜索一下关于 TLS 或 SSL 的类。

**🔧 `cmm_search`**({"query": "TLS SSL"})

> 💭 **思考**：现在我已经有足够的信息来回答用户的问题了。在 Godot 中，加密解密主要使用以下类：

1. `Crypto` - 主要的加密类，用于加密解密操作
2. `CryptoKey` - 密钥管理
3. `TLSOptions` - TLS 选项和证书管理
4. `StreamPeerTLS` - TLS 流对等体

用户问的是加密解密用哪个类，最直接的答案是 `Crypto` 类。

**🤖 Agent**：`Crypto`、`CryptoKey`

**📋 工具结果**：
```
(no results)
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
/**************************************************************************/
/*  crypto.h                                                              */
/**************************************************************************/
/*                         This file is part of:                          */
/*                             GODOT ENGINE                               */
/*                        https://godotengine.org                         */
/**************************************************************************/
/* Copyright (c) 2014-present Godot Engine contributors (see 
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
(no results)
```

**📋 工具结果**：
```
- get_own_certificate  (Users-ks_128-Documents-godot-src-core.crypto.crypto.TLSOptions.get_own_certificate)  crypto/crypto.h
- own_certificate  (Users-ks_128-Documents-godot-src-core.crypto.crypto.TLSOptions.own_certificate)  crypto/crypto.h
```

**📋 工具结果**：
```
- create  (Users-ks_128-Documents-godot-src-core.io.stream_peer_tls.StreamPeerTLS.create)  io/stream_peer_tls.cpp
- is_available  (Users-ks_128-Documents-godot-src-core.io.stream_peer_tls.StreamPeerTLS.is_available)  io/stream_peer_tls.cpp
- _bind_methods  (Users-ks_128-Documents-godot-src-core.io.stream_peer_tls.StreamPeerTLS._bind_methods)  io/stream_peer_tls.cpp
- TLSData  (Users-ks_128-Documents-godot-src-core.os.safe_binary_mutex.SafeBinaryMutex.TLSData.TLSData)  os/safe_binary_mutex.h
- StreamPeerTLS  (Users-ks_128-Documents-godot-src-core.io.stream_peer_tls.StreamPeerTLS)  io/stream_pee
```


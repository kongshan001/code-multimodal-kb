# q24 · code_retrieval · arm: `kb+superpowers`

**题**：加密解密用哪个类？  ·  **gold**：Crypto
**答对**：✓  ·  **答案**：Godot 的加密解密涉及以下核心类（`core/crypto/` 下）：

| 用途 | 类/方法 |
|------|---------|
| **高层加密门面** | `Crypto` — 统一入口，提供 `encrypt()`、`d
**指标**：tokens=943 · llm_calls=4 · tool_steps=3 · 耗时=29.12s · 截断=否

---

**👤 用户**：加密解密用哪个类？

> 💭 **思考**：The user is asking about which class is used for encryption/decryption in Godot. Let me search for it.

**🔧 `cmm_search`**({"query": "encryption decryption"})

> 💭 **思考**：That result doesn't seem directly relevant. Let me search more specifically for crypto/encryption classes in Godot core.

**🔧 `cmm_search`**({"query": "crypto AES encrypt decrypt"})

> 💭 **思考**：Let me also check for a Crypto class.

**🔧 `cmm_search`**({"query": "Crypto class generate random key HMAC hashing"})

**🤖 Agent**：Godot 的加密解密涉及以下核心类（`core/crypto/` 下）：

| 用途 | 类/方法 |
|------|---------|
| **高层加密门面** | `Crypto` — 统一入口，提供 `encrypt()`、`decrypt()`、`generate_random_bytes()`、`hmac_digest()` 等 |
| **AES 加解密** | `AESContext` — 低层 AES 块加密，通过 `start()`/`update()`/`finish()` 分步操作 |
| **RSA 非对称加密** | `CryptoKey` — 加载/管理 RS

**📋 工具结果**：
```
- encryption_key_builder  (Users-ks_128-Documents-godot-src-core.core_builders.encryption_key_builder)  core_builders.py
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
- hmac_digest  (Users-ks_128-Documents-godot-src-core.crypto.crypto.Crypto.hmac_digest)  crypto/crypto.cpp
- ~HashingContext  (Users-ks_128-Documents-godot-src-core.crypto.hashing_context.HashingContext.~HashingContext)  crypto/hashing_context.cpp
- ~HMACContext  (Users-ks_128-Documents-godot-src-core.crypto.crypto.HMACContext.~HMACContext)  crypto/crypto.h
- start  (Users-ks_128-Documents-godot-src-core.crypto.hashing_context.HashingContext.start)  crypto/hashing_context.cpp
- update  (Users-ks_128-Documents-godot-src-core.crypto.hashing_context.HashingContext.update)  crypto/hashing_context.
```


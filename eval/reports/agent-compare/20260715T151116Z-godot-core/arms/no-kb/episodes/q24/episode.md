# q24 · code_retrieval · arm: `no-kb`

**题**：加密解密用哪个类？  ·  **gold**：Crypto
**答对**：✓  ·  **答案**：主要用 **`Crypto`**（`core/crypto/crypto.h`）。

相关辅助类还有：
- **`AESContext`** — AES 对称加解密
- **`HashingContext`** — 哈希计算（SHA-1/S
**指标**：tokens=1270 · llm_calls=2 · tool_steps=1 · 耗时=13.51s · 截断=否

---

**👤 用户**：加密解密用哪个类？

> 💭 **思考**：用户问加密解密用哪个类。让我在 Godot core/ 源码中搜索加密相关的类。

**🔧 `grep_code`**({"pattern": "Crypto"})

> 💭 **思考**：Found it. The main class is `Crypto` in core/crypto/crypto.h.

**🤖 Agent**：主要用 **`Crypto`**（`core/crypto/crypto.h`）。

相关辅助类还有：
- **`AESContext`** — AES 对称加解密
- **`HashingContext`** — 哈希计算（SHA-1/SHA-256）
- **`CryptoKey`** — 密钥（`crypto_core.h` 中）
- **`FileAccessEncrypted`** — 加密文件读写

**📋 工具结果**：
```
matched 20 files:
/Users/ks_128/Documents/godot-src/core/crypto/hashing_context.cpp
/Users/ks_128/Documents/godot-src/core/crypto/crypto_resource_format.cpp
/Users/ks_128/Documents/godot-src/core/crypto/crypto_core.cpp
/Users/ks_128/Documents/godot-src/core/crypto/crypto.h
/Users/ks_128/Documents/godot-src/core/crypto/aes_context.h
/Users/ks_128/Documents/godot-src/core/crypto/crypto_resource_format.h
/Users/ks_128/Documents/godot-src/core/crypto/crypto_core.h
/Users/ks_128/Documents/godot-src/core/crypto/crypto.cpp
/Users/ks_128/Documents/godot-src/core/extension/gdextension_special_compat_ha
```


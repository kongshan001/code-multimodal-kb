# q24 · code_retrieval · arm: `kb`

**题**：加密解密用哪个类？  ·  **gold**：Crypto
**答对**：✓  ·  **答案**：加密解密使用 **`Crypto`** 类（位于 `core/crypto/crypto.cpp`）。

主要方法包括：
- `Crypto::generate_random_bytes()` — 生成随机字节
- `Crypto::gen
**指标**：tokens=1013 · llm_calls=2 · tool_steps=1 · 耗时=12.35s · 截断=否

---

**👤 用户**：加密解密用哪个类？

**🔧 `cmm_search`**({"query": "encryption decryption crypto cipher"})

**📋 工具结果**：
```
- encryption_key_builder  (Users-ks_128-Documents-godot-src-core.core_builders.encryption_key_builder)  core_builders.py
- create  (Users-ks_128-Documents-godot-src-core.crypto.crypto.Crypto.create)  crypto/crypto.cpp
- hmac_digest  (Users-ks_128-Documents-godot-src-core.crypto.crypto.Crypto.hmac_digest)  crypto/crypto.cpp
- _bind_methods  (Users-ks_128-Documents-godot-src-core.crypto.crypto.Crypto._bind_methods)  crypto/crypto.cpp
- load_default_certificates  (Users-ks_128-Documents-godot-src-core.crypto.crypto.Crypto.load_default_certificates)  crypto/crypto.cpp
```

**🤖 Agent**：加密解密使用 **`Crypto`** 类（位于 `core/crypto/crypto.cpp`）。

主要方法包括：
- `Crypto::generate_random_bytes()` — 生成随机字节
- `Crypto::generate_rsa()` — 生成 RSA 密钥
- `Crypto::generate_self_signed_certificate()` — 生成自签名证书
- `Crypto::encrypt()` / `Crypto::decrypt()` — 加密/解密
- `Crypto::hmac_digest()` — HMAC 摘要

此外还涉及辅助类 


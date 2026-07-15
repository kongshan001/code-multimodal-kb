# q24 · code_retrieval · arm: `kb+openspec`

**题**：加密解密用哪个类？  ·  **gold**：Crypto
**答对**：✓  ·  **答案**：`Crypto` 类（`core/crypto/crypto.cpp`），相关方法有 `create`、`generate_random_bytes`、`encrypt`、`decrypt`、`hmac_digest` 等。

配套还有 `
**指标**：tokens=1351 · llm_calls=2 · tool_steps=1 · 耗时=15.04s · 截断=否

---

**👤 用户**：加密解密用哪个类？

> 💭 **思考**：The user is asking about which class is used for encryption and decryption in Godot core.

**🔧 `cmm_search`**({"query": "encryption decryption cipher crypto"})

> 💭 **思考**：The result shows `Crypto` class in `crypto/crypto.cpp`. Let me answer directly with the symbol name.

**🤖 Agent**：`Crypto` 类（`core/crypto/crypto.cpp`），相关方法有 `create`、`generate_random_bytes`、`encrypt`、`decrypt`、`hmac_digest` 等。

配套还有 `CryptoKey`（管理密钥对）。

**📋 工具结果**：
```
- encryption_key_builder  (Users-ks_128-Documents-godot-src-core.core_builders.encryption_key_builder)  core_builders.py
- create  (Users-ks_128-Documents-godot-src-core.crypto.crypto.Crypto.create)  crypto/crypto.cpp
- hmac_digest  (Users-ks_128-Documents-godot-src-core.crypto.crypto.Crypto.hmac_digest)  crypto/crypto.cpp
- _bind_methods  (Users-ks_128-Documents-godot-src-core.crypto.crypto.Crypto._bind_methods)  crypto/crypto.cpp
- load_default_certificates  (Users-ks_128-Documents-godot-src-core.crypto.crypto.Crypto.load_default_certificates)  crypto/crypto.cpp
```


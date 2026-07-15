# q24 · code_retrieval · arm: `kb`

**题**：加密解密用哪个类？  ·  **gold**：Crypto
**答对**：✓  ·  **答案**：`Crypto` 类（定义于 `core/crypto/crypto.cpp`），提供加密、解密、HMAC 摘要等功能。
**指标**：tokens=1014 · llm_calls=2 · tool_steps=1 · 耗时=11.35s · 截断=否

---

**👤 用户**：加密解密用哪个类？

> 💭 **思考**：The user is asking about which class is used for encryption/decryption in Godot core/.

**🔧 `cmm_search`**({"query": "encryption decryption crypto"})

> 💭 **思考**：The answer is clear: the `Crypto` class.

**🤖 Agent**：`Crypto` 类（定义于 `core/crypto/crypto.cpp`），提供加密、解密、HMAC 摘要等功能。

**📋 工具结果**：
```
- encryption_key_builder  (Users-ks_128-Documents-godot-src-core.core_builders.encryption_key_builder)  core_builders.py
- create  (Users-ks_128-Documents-godot-src-core.crypto.crypto.Crypto.create)  crypto/crypto.cpp
- hmac_digest  (Users-ks_128-Documents-godot-src-core.crypto.crypto.Crypto.hmac_digest)  crypto/crypto.cpp
- _bind_methods  (Users-ks_128-Documents-godot-src-core.crypto.crypto.Crypto._bind_methods)  crypto/crypto.cpp
- load_default_certificates  (Users-ks_128-Documents-godot-src-core.crypto.crypto.Crypto.load_default_certificates)  crypto/crypto.cpp
```


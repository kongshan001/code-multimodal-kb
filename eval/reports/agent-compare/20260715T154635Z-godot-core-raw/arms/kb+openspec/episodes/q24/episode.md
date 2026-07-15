# q24 · code_retrieval · arm: `kb+openspec`

**题**：加密解密用哪个类？  ·  **gold**：Crypto
**答对**：✓  ·  **答案**：加密解密用 **`Crypto`** 类（`core/crypto/crypto.cpp`）。

主要方法包括：
- **`Crypto::create`** — 创建加密密钥/对象
- **`Crypto::hmac_digest`** 
**指标**：tokens=981 · llm_calls=2 · tool_steps=1 · 耗时=6.84s · 截断=否

---

**👤 用户**：加密解密用哪个类？

**🔧 `cmm_search`**({"query": "encryption decryption crypto"})

**📋 工具结果**：
```
- encryption_key_builder  (Users-ks_128-Documents-godot-src-core.core_builders.encryption_key_builder)  core_builders.py
- create  (Users-ks_128-Documents-godot-src-core.crypto.crypto.Crypto.create)  crypto/crypto.cpp
- hmac_digest  (Users-ks_128-Documents-godot-src-core.crypto.crypto.Crypto.hmac_digest)  crypto/crypto.cpp
- _bind_methods  (Users-ks_128-Documents-godot-src-core.crypto.crypto.Crypto._bind_methods)  crypto/crypto.cpp
- load_default_certificates  (Users-ks_128-Documents-godot-src-core.crypto.crypto.Crypto.load_default_certificates)  crypto/crypto.cpp
```

**🤖 Agent**：加密解密用 **`Crypto`** 类（`core/crypto/crypto.cpp`）。

主要方法包括：
- **`Crypto::create`** — 创建加密密钥/对象
- **`Crypto::hmac_digest`** — HMAC 摘要
- **`Crypto::generate_random_bytes`** — 生成随机字节
- **`Crypto::encrypt` / `Crypto::decrypt`** — 加解密操作

相关辅助类还有 **`CryptoKey`**（密钥管理）和 **`HashingContext`**（哈希计算）。


# q24 · code_retrieval · arm: `kb+superpowers`

**题**：加密解密用哪个类？  ·  **gold**：Crypto
**答对**：✓  ·  **答案**：加密解密用 **`Crypto`** 类（`core/crypto/crypto.cpp`）。

主要方法包括：
- `Crypto::create()` — 创建实例
- `Crypto::hmac_digest()` — HMAC 摘要
**指标**：tokens=349 · llm_calls=2 · tool_steps=1 · 耗时=15.43s · 截断=否

---

**👤 用户**：加密解密用哪个类？

> 💭 **思考**：用户问加密解密用哪个类。让我搜索一下。

**🔧 `cmm_search`**({"query": "encryption decryption crypto"})

> 💭 **思考**：结果是 `Crypto` 类。

**🤖 Agent**：加密解密用 **`Crypto`** 类（`core/crypto/crypto.cpp`）。

主要方法包括：
- `Crypto::create()` — 创建实例
- `Crypto::hmac_digest()` — HMAC 摘要
- `Crypto::load_default_certificates()` — 加载默认证书

**📋 工具结果**：
```
- encryption_key_builder  (Users-ks_128-Documents-godot-src-core.core_builders.encryption_key_builder)  core_builders.py
- create  (Users-ks_128-Documents-godot-src-core.crypto.crypto.Crypto.create)  crypto/crypto.cpp
- hmac_digest  (Users-ks_128-Documents-godot-src-core.crypto.crypto.Crypto.hmac_digest)  crypto/crypto.cpp
- _bind_methods  (Users-ks_128-Documents-godot-src-core.crypto.crypto.Crypto._bind_methods)  crypto/crypto.cpp
- load_default_certificates  (Users-ks_128-Documents-godot-src-core.crypto.crypto.Crypto.load_default_certificates)  crypto/crypto.cpp
```


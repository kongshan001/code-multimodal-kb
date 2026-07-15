# q24 · code_retrieval · arm: `kb+openspec`

**题**：加密解密用哪个类？  ·  **gold**：Crypto
**答对**：✓  ·  **答案**：Godot 中加密解密主要用以下类（均在 `core/crypto/` 下）：

- **`Crypto`** — 高层加密工具类（`generate_random_bytes`、`generate_self_signed_certific
**指标**：tokens=1569 · llm_calls=3 · tool_steps=2 · 耗时=26.11s · 截断=否

---

**👤 用户**：加密解密用哪个类？

> 💭 **思考**：The user is asking about which class is used for encryption/decryption in Godot.

**🔧 `cmm_search`**({"query": "encryption decryption cipher"})

> 💭 **思考**：The search didn't return very relevant results. Let me search more specifically for crypto/aes related classes.

**🔧 `cmm_search`**({"query": "crypto AES hash HMAC"})

**🤖 Agent**：Godot 中加密解密主要用以下类（均在 `core/crypto/` 下）：

- **`Crypto`** — 高层加密工具类（`generate_random_bytes`、`generate_self_signed_certificate`、`hmac_digest` 等）
- **`AESContext`** — AES 对称加密/解密（`start` → `update` → `finish`）
- **`HMACContext`** — HMAC 消息认证码（用于完整性校验）

如果需要对称加密解密，核心是 **`AESContext`**。

**📋 工具结果**：
```
- encryption_key_builder  (Users-ks_128-Documents-godot-src-core.core_builders.encryption_key_builder)  core_builders.py
```

**📋 工具结果**：
```
- hmac_digest  (Users-ks_128-Documents-godot-src-core.crypto.crypto.Crypto.hmac_digest)  crypto/crypto.cpp
- ~HMACContext  (Users-ks_128-Documents-godot-src-core.crypto.crypto.HMACContext.~HMACContext)  crypto/crypto.h
- start  (Users-ks_128-Documents-godot-src-core.crypto.aes_context.AESContext.start)  crypto/aes_context.cpp
- update  (Users-ks_128-Documents-godot-src-core.crypto.aes_context.AESContext.update)  crypto/aes_context.cpp
- finish  (Users-ks_128-Documents-godot-src-core.crypto.aes_context.AESContext.finish)  crypto/aes_context.cpp
```


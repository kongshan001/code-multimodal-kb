# q24 · code_retrieval · arm: `no-kb`

**题**：加密解密用哪个类？  ·  **gold**：Crypto
**答对**：✓  ·  **答案**：加密解密用 **`Crypto`** 类（定义于 `core/crypto/crypto.h`），底层辅助类为 `CryptoCore`（`core/crypto/crypto_core.h`）。

- `Crypto` — 对外暴露的高层
**指标**：tokens=1078 · llm_calls=3 · tool_steps=2 · 耗时=16.32s · 截断=否

---

**👤 用户**：加密解密用哪个类？

> 💭 **思考**：用户问加密解密用哪个类。让我在 Godot core 源码里搜索相关内容。

**🔧 `grep_code`**({"pattern": "class.*Crypto"})

**🔧 `grep_code`**({"pattern": "encrypt|decrypt"})

> 💭 **思考**：Found the crypto-related files. The main class is `Crypto` in `crypto.h`.

**🤖 Agent**：加密解密用 **`Crypto`** 类（定义于 `core/crypto/crypto.h`），底层辅助类为 `CryptoCore`（`core/crypto/crypto_core.h`）。

- `Crypto` — 对外暴露的高层 API，提供 `generate_random_bytes`、`generate_rsa`、`encrypt`、`decrypt` 等方法。
- `CryptoCore` — 底层封装（AES、RSA、MD5、SHA 等）。

脚本层通过 `OS.get_singleton()->get_native_interface()` 或直接使用 `Crypto`

**📋 工具结果**：
```
matched 5 files:
/Users/ks_128/Documents/godot-src/core/crypto/crypto.h
/Users/ks_128/Documents/godot-src/core/crypto/crypto_resource_format.h
/Users/ks_128/Documents/godot-src/core/crypto/crypto_core.h
/Users/ks_128/Documents/godot-src/core/crypto/crypto.cpp
/Users/ks_128/Documents/godot-src/core/register_core_types.cpp
```

**📋 工具结果**：
```
(no matches)
```


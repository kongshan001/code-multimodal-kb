# q14 · code_retrieval · arm: `kb`

**题**：保存资源用哪个类？  ·  **gold**：ResourceSaver
**答对**：✓  ·  **答案**：`ResourceSaver`
**指标**：tokens=977 · llm_calls=2 · tool_steps=1 · 耗时=9.75s · 截断=否

---

**👤 用户**：保存资源用哪个类？

> 💭 **思考**：用户问保存资源用哪个类。让我搜索一下。

**🔧 `cmm_search`**({"query": "save resource"})

**🤖 Agent**：`ResourceSaver`

**📋 工具结果**：
```
- save  (Users-ks_128-Documents-godot-src-core.io.resource_saver.ResourceFormatSaver.save)  io/resource_saver.cpp
- save  (Users-ks_128-Documents-godot-src-core.io.resource_saver.ResourceSaver.save)  io/resource_saver.cpp
- save  (Users-ks_128-Documents-godot-src-core.crypto.crypto_resource_format.ResourceFormatSaverCrypto.save)  crypto/crypto_resource_format.cpp
- save  (Users-ks_128-Documents-godot-src-core.io.json_resource_format.ResourceFormatSaverJSON.save)  io/json_resource_format.cpp
- save  (Users-ks_128-Documents-godot-src-core.io.resource_format_binary.ResourceFormatSaverBinaryInstan
```


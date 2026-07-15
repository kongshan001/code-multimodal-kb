# q14 · code_retrieval · arm: `kb+superpowers`

**题**：保存资源用哪个类？  ·  **gold**：ResourceSaver
**答对**：✓  ·  **答案**：保存资源用 **`ResourceSaver`**（核心入口类），具体格式由 `ResourceFormatSaver` 子类实现，如 `ResourceFormatSaverBinaryInstance`、`ResourceFormatS
**指标**：tokens=1368 · llm_calls=2 · tool_steps=1 · 耗时=13.21s · 截断=否

---

**👤 用户**：保存资源用哪个类？

> 💭 **思考**：用户问保存资源用哪个类。让我搜索一下。

**🔧 `cmm_search`**({"query": "save resource"})

**🤖 Agent**：保存资源用 **`ResourceSaver`**（核心入口类），具体格式由 `ResourceFormatSaver` 子类实现，如 `ResourceFormatSaverBinaryInstance`、`ResourceFormatSaverJSON`、`ResourceFormatSaverCrypto`。

**📋 工具结果**：
```
- save  (Users-ks_128-Documents-godot-src-core.io.resource_saver.ResourceFormatSaver.save)  io/resource_saver.cpp
- save  (Users-ks_128-Documents-godot-src-core.io.resource_saver.ResourceSaver.save)  io/resource_saver.cpp
- save  (Users-ks_128-Documents-godot-src-core.crypto.crypto_resource_format.ResourceFormatSaverCrypto.save)  crypto/crypto_resource_format.cpp
- save  (Users-ks_128-Documents-godot-src-core.io.json_resource_format.ResourceFormatSaverJSON.save)  io/json_resource_format.cpp
- save  (Users-ks_128-Documents-godot-src-core.io.resource_format_binary.ResourceFormatSaverBinaryInstan
```


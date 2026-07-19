# q14 · code_retrieval · arm: `kb+openspec`

- **题**：保存资源用哪个类？
- **gold**：ResourceSaver
- **答对**：✓
- **答案**：ResourceSaver
- **指标**：tokens=3957 · llm_calls=3 · tool_steps=2 · 耗时=9.46s · 截断=否

---

**👤 用户**：保存资源用哪个类？

> 💭 **思考**：用户问"保存资源用哪个类？"这是关于 Godot 引擎的问题，需要找到保存资源相关的类。

让我搜索一下相关的类或函数。

**🔧 `cmm_search`**({"query": "保存资源 save resource"})

> 💭 **思考**：搜索结果中出现了 `ResourceSaver` 类，这应该就是保存资源的主要类。让我进一步确认一下。

**🔧 `cmm_search`**({"query": "ResourceSaver"})

> 💭 **思考**：确认了，保存资源用的是 `ResourceSaver` 类。根据搜索结果，这个类位于 core_bind.h 中，并且有 save 方法。

让我直接回答用户。

**🤖 Agent**：ResourceSaver

**📋 工具结果**：
```
- save  (Users-ks_128-Documents-godot-src-core.io.resource_saver.ResourceFormatSaver.save)  io/resource_saver.cpp
- save  (Users-ks_128-Documents-godot-src-core.io.resource_saver.ResourceSaver.save)  io/resource_saver.cpp
- save  (Users-ks_128-Documents-godot-src-core.crypto.crypto_resource_format.ResourceFormatSaverCrypto.save)  crypto/crypto_resource_format.cpp
- save  (Users-ks_128-Documents-godot-src-core.io.json_resource_format.ResourceFormatSaverJSON.save)  io/json_resource_format.cpp
- save  (Users-ks_128-Documents-godot-src-core.io.resource_format_binary.ResourceFormatSaverBinaryInstan
```

**📋 工具结果**：
```
- ResourceSaver  (Users-ks_128-Documents-godot-src-core.core_bind.ResourceSaver.ResourceSaver)  core_bind.h
- save  (Users-ks_128-Documents-godot-src-core.core_bind.ResourceSaver.save)  core_bind.cpp
- save  (Users-ks_128-Documents-godot-src-core.io.resource_saver.ResourceSaver.save)  io/resource_saver.cpp
- set_uid  (Users-ks_128-Documents-godot-src-core.core_bind.ResourceSaver.set_uid)  core_bind.cpp
- _bind_methods  (Users-ks_128-Documents-godot-src-core.core_bind.ResourceSaver._bind_methods)  core_bind.cpp
```


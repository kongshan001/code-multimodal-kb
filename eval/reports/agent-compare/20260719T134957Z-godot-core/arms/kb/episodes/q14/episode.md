# q14 · code_retrieval · arm: `kb`

- **题**：保存资源用哪个类？
- **gold**：ResourceSaver
- **答对**：✓
- **答案**：`ResourceSaver`
- **指标**：tokens=3268 · llm_calls=3 · tool_steps=2 · 耗时=10.27s · 截断=否

---

**👤 用户**：保存资源用哪个类？

> 💭 **思考**：用户问"保存资源用哪个类？"，这是在问 Godot 代码库中保存资源相关的类。

我需要用 cmm_search 工具搜索相关的符号。让我搜索 "save resource" 或 "ResourceSaver" 相关的内容。

**🔧 `cmm_search`**({"query": "save resource"})

> 💭 **思考**：搜索结果显示了多个与保存资源相关的符号。最相关的是 `ResourceSaver` 类，这是 Godot 中用于保存资源的主要类。

从结果看：
- `ResourceSaver.save` - 这是主要的资源保存类
- `ResourceFormatSaver` - 这是资源格式保存器

让我再搜索一下 `ResourceSaver` 类本身。

**🔧 `cmm_search`**({"query": "ResourceSaver"})

> 💭 **思考**：从搜索结果可以确认，保存资源使用的是 `ResourceSaver` 类。这是 Godot 中用于保存资源的核心类。

**🤖 Agent**：`ResourceSaver`

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


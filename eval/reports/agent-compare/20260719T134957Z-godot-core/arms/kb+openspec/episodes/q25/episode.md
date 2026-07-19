# q25 · code_retrieval · arm: `kb+openspec`

- **题**：翻译/本地化服务器用哪个类？
- **gold**：TranslationServer
- **答对**：✓
- **答案**：`TranslationServer`
- **指标**：tokens=2552 · llm_calls=2 · tool_steps=1 · 耗时=6.22s · 截断=否

---

**👤 用户**：翻译/本地化服务器用哪个类？

> 💭 **思考**：用户问"翻译/本地化服务器用哪个类？"，这是在问 Godot 代码库中用于翻译/本地化的服务器类。

这是一个直接的问题，需要查找 Godot core/ 中相关的翻译/本地化服务器类。我应该使用 cmm_search 工具来查找。

让我搜索相关的符号，关键词可以是 "translation"、"localization"、"locale" 等。

**🔧 `cmm_search`**({"query": "translation localization server"})

> 💭 **思考**：很好，找到了！Godot 中用于翻译/本地化的服务器类是 `TranslationServer`。这个类位于 `string/translation_server.cpp` 中，提供了翻译相关的各种方法如 `add_translation`、`remove_translation` 等。

根据我的指示，应该用符号名作答，答案要简短直接。

**🤖 Agent**：`TranslationServer`

**📋 工具结果**：
```
- TranslationServer  (Users-ks_128-Documents-godot-src-core.string.translation_server.TranslationServer.TranslationServer)  string/translation_server.cpp
- add_translation  (Users-ks_128-Documents-godot-src-core.string.translation_server.TranslationServer.add_translation)  string/translation_server.cpp
- remove_translation  (Users-ks_128-Documents-godot-src-core.string.translation_server.TranslationServer.remove_translation)  string/translation_server.cpp
- has_translation  (Users-ks_128-Documents-godot-src-core.string.translation_server.TranslationServer.has_translation)  string/translation_s
```


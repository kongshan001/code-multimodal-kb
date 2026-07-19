# q25 · code_retrieval · arm: `kb+superpowers`

- **题**：翻译/本地化服务器用哪个类？
- **gold**：TranslationServer
- **答对**：✓
- **答案**：`TranslationServer`
- **指标**：tokens=2612 · llm_calls=2 · tool_steps=1 · 耗时=7.32s · 截断=否

---

**👤 用户**：翻译/本地化服务器用哪个类？

> 💭 **思考**：用户问"翻译/本地化服务器用哪个类？"，这是在问Godot代码库中负责翻译/本地化功能的类。

让我搜索相关的符号。在Godot中，本地化通常和"Translation"、"Localization"相关。

我应该搜索一下相关的类名。

**🔧 `cmm_search`**({"query": "translation localization server"})

> 💭 **思考**：搜索结果显示了 `TranslationServer` 类，这应该就是用户问的翻译/本地化服务器类。

根据指令，一旦工具返回了相关符号就立刻用符号名作答，不要反复查。查到即答。

答案应该简短：直接给类名，不要长解释。

**🤖 Agent**：`TranslationServer`

**📋 工具结果**：
```
- TranslationServer  (Users-ks_128-Documents-godot-src-core.string.translation_server.TranslationServer.TranslationServer)  string/translation_server.cpp
- add_translation  (Users-ks_128-Documents-godot-src-core.string.translation_server.TranslationServer.add_translation)  string/translation_server.cpp
- remove_translation  (Users-ks_128-Documents-godot-src-core.string.translation_server.TranslationServer.remove_translation)  string/translation_server.cpp
- has_translation  (Users-ks_128-Documents-godot-src-core.string.translation_server.TranslationServer.has_translation)  string/translation_s
```


# q25 · code_retrieval · arm: `kb`

- **题**：翻译/本地化服务器用哪个类？
- **gold**：TranslationServer
- **答对**：✓
- **答案**：`TranslationServer`
- **指标**：tokens=1948 · llm_calls=2 · tool_steps=1 · 耗时=8.77s · 截断=否

---

**👤 用户**：翻译/本地化服务器用哪个类？

> 💭 **思考**：用户问"翻译/本地化服务器用哪个类？"，这是在问 Godot 代码库中与翻译/本地化相关的服务器类。

我需要在 Godot core/ 代码库中搜索相关的类名。通常翻译/本地化相关的类名可能包含 "Translation"、"Localization"、"Locale" 等关键词。

让我用 cmm_search 查找相关符号。

**🔧 `cmm_search`**({"query": "TranslationServer LocalizationServer"})

> 💭 **思考**：找到了！Godot 使用 `TranslationServer` 类作为翻译/本地化服务器。

**🤖 Agent**：`TranslationServer`

**📋 工具结果**：
```
- TranslationServer  (Users-ks_128-Documents-godot-src-core.string.translation_server.TranslationServer.TranslationServer)  string/translation_server.cpp
- clear  (Users-ks_128-Documents-godot-src-core.string.translation_server.TranslationServer.clear)  string/translation_server.cpp
- translate  (Users-ks_128-Documents-godot-src-core.string.translation_server.TranslationServer.translate)  string/translation_server.cpp
- setup  (Users-ks_128-Documents-godot-src-core.string.translation_server.TranslationServer.setup)  string/translation_server.cpp
- pseudolocalize  (Users-ks_128-Documents-godot-
```


# q25 · code_retrieval · arm: `kb+openspec`

**题**：翻译/本地化服务器用哪个类？  ·  **gold**：TranslationServer
**答对**：✓  ·  **答案**：`TranslationServer`（定义在 `core/string/translation_server.cpp`）。

主要方法包括：
- `add_translation` / `remove_translation` / `ha
**指标**：tokens=1534 · llm_calls=2 · tool_steps=1 · 耗时=8.48s · 截断=否

---

**👤 用户**：翻译/本地化服务器用哪个类？

**🔧 `cmm_search`**({"query": "translation localization server"})

**📋 工具结果**：
```
- TranslationServer  (Users-ks_128-Documents-godot-src-core.string.translation_server.TranslationServer.TranslationServer)  string/translation_server.cpp
- add_translation  (Users-ks_128-Documents-godot-src-core.string.translation_server.TranslationServer.add_translation)  string/translation_server.cpp
- remove_translation  (Users-ks_128-Documents-godot-src-core.string.translation_server.TranslationServer.remove_translation)  string/translation_server.cpp
- has_translation  (Users-ks_128-Documents-godot-src-core.string.translation_server.TranslationServer.has_translation)  string/translation_s
```

**🤖 Agent**：`TranslationServer`（定义在 `core/string/translation_server.cpp`）。

主要方法包括：
- `add_translation` / `remove_translation` / `has_translation` — 管理翻译资源
- `get_translation_object` — 获取翻译对象
- 此外还有 `translate`、`set_locale`、`get_locale` 等常用方法。


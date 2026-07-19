# q19 · code_retrieval · arm: `kb`

- **题**：主循环基类叫什么？
- **gold**：MainLoop
- **答对**：✓
- **答案**：`MainLoop`
- **指标**：tokens=1933 · llm_calls=2 · tool_steps=1 · 耗时=6.79s · 截断=否

---

**👤 用户**：主循环基类叫什么？

> 💭 **思考**：用户问"主循环基类叫什么？"，这是在问 Godot 引擎中的主循环基类的名称。

我需要用代码知识库搜索相关的符号。可能的关键词包括：
- "主循环"
- "main loop"
- "MainLoop"

让我用 cmm_search 来查找。

**🔧 `cmm_search`**({"query": "main loop base class"})

> 💭 **思考**：搜索结果显示主循环基类是 `MainLoop`，位于 `os/main_loop.h` 文件中。

根据指示，我需要简短地用符号名作答，不要长解释。

**🤖 Agent**：`MainLoop`

**📋 工具结果**：
```
- ~MainLoop  (Users-ks_128-Documents-godot-src-core.os.main_loop.MainLoop.~MainLoop)  os/main_loop.h
- get_main_loop  (Users-ks_128-Documents-godot-src-core.core_bind.Engine.get_main_loop)  core_bind.cpp
- _register_main_loop_callbacks  (Users-ks_128-Documents-godot-src-core.extension.gdextension.GDExtension._register_main_loop_callbacks)  extension/gdextension.cpp
- initialize  (Users-ks_128-Documents-godot-src-core.os.main_loop.MainLoop.initialize)  os/main_loop.cpp
- process  (Users-ks_128-Documents-godot-src-core.os.main_loop.MainLoop.process)  os/main_loop.cpp
```


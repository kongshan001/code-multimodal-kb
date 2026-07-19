# q19 · code_retrieval · arm: `kb+superpowers`

- **题**：主循环基类叫什么？
- **gold**：MainLoop
- **答对**：✓
- **答案**：`MainLoop`
- **指标**：tokens=2543 · llm_calls=2 · tool_steps=1 · 耗时=7.45s · 截断=否

---

**👤 用户**：主循环基类叫什么？

> 💭 **思考**：用户问"主循环基类叫什么？"这是在问 Godot 引擎中的主循环基类的名称。

让我用代码知识库搜索来找到这个信息。我需要搜索与 main loop 相关的类。

**🔧 `cmm_search`**({"query": "main loop base class"})

> 💭 **思考**：搜索结果显示主循环基类是 `MainLoop`，位于 os/main_loop.h 文件。这正是用户问的。

**🤖 Agent**：`MainLoop`

**📋 工具结果**：
```
- ~MainLoop  (Users-ks_128-Documents-godot-src-core.os.main_loop.MainLoop.~MainLoop)  os/main_loop.h
- get_main_loop  (Users-ks_128-Documents-godot-src-core.core_bind.Engine.get_main_loop)  core_bind.cpp
- _register_main_loop_callbacks  (Users-ks_128-Documents-godot-src-core.extension.gdextension.GDExtension._register_main_loop_callbacks)  extension/gdextension.cpp
- initialize  (Users-ks_128-Documents-godot-src-core.os.main_loop.MainLoop.initialize)  os/main_loop.cpp
- process  (Users-ks_128-Documents-godot-src-core.os.main_loop.MainLoop.process)  os/main_loop.cpp
```


# q19 · code_retrieval · arm: `kb+openspec`

**题**：主循环基类叫什么？  ·  **gold**：MainLoop
**答对**：✓  ·  **答案**：`MainLoop`（定义在 `os/main_loop.h`）。
**指标**：tokens=1313 · llm_calls=2 · tool_steps=1 · 耗时=19.63s · 截断=否

---

**👤 用户**：主循环基类叫什么？

> 💭 **思考**：The user is asking about the main loop base class in Godot. Let me search for it.

**🔧 `cmm_search`**({"query": "main loop base class"})

> 💭 **思考**：The answer is clear: `MainLoop`.

**🤖 Agent**：`MainLoop`（定义在 `os/main_loop.h`）。

**📋 工具结果**：
```
- ~MainLoop  (Users-ks_128-Documents-godot-src-core.os.main_loop.MainLoop.~MainLoop)  os/main_loop.h
- get_main_loop  (Users-ks_128-Documents-godot-src-core.core_bind.Engine.get_main_loop)  core_bind.cpp
- _register_main_loop_callbacks  (Users-ks_128-Documents-godot-src-core.extension.gdextension.GDExtension._register_main_loop_callbacks)  extension/gdextension.cpp
- initialize  (Users-ks_128-Documents-godot-src-core.os.main_loop.MainLoop.initialize)  os/main_loop.cpp
- process  (Users-ks_128-Documents-godot-src-core.os.main_loop.MainLoop.process)  os/main_loop.cpp
```


# q18 · code_retrieval · arm: `kb+superpowers`

**题**：引擎主类叫什么？  ·  **gold**：Engine
**答对**：✓  ·  **答案**：引擎主类是 **`core_bind::Engine`**（绑定到 GDScript 中的 `Engine` 单例），核心方法如 `get_main_loop()` 用于获取主循环。
**指标**：tokens=370 · llm_calls=2 · tool_steps=1 · 耗时=8.96s · 截断=否

---

**👤 用户**：引擎主类叫什么？

> 💭 **思考**：用户问引擎主类叫什么。在 Godot 中，引擎主类是 `Engine`。让我搜索确认一下。

**🔧 `cmm_search`**({"query": "engine main class"})

> 💭 **思考**：搜索结果显示 `core_bind.Engine` 类，包含 `get_main_loop` 方法。让我进一步确认。

**🤖 Agent**：引擎主类是 **`core_bind::Engine`**（绑定到 GDScript 中的 `Engine` 单例），核心方法如 `get_main_loop()` 用于获取主循环。

**📋 工具结果**：
```
- get_main_loop  (Users-ks_128-Documents-godot-src-core.core_bind.Engine.get_main_loop)  core_bind.cpp
- ~MainLoop  (Users-ks_128-Documents-godot-src-core.os.main_loop.MainLoop.~MainLoop)  os/main_loop.h
- is_main_thread  (Users-ks_128-Documents-godot-src-core.core_bind.Thread.is_main_thread)  core_bind.cpp
- get_main_diagonal  (Users-ks_128-Documents-godot-src-core.math.basis.Basis.get_main_diagonal)  math/basis.h
- make_main_thread  (Users-ks_128-Documents-godot-src-core.os.thread.Thread.make_main_thread)  os/thread.h
```


# q18 · code_retrieval · arm: `kb+openspec`

**题**：引擎主类叫什么？  ·  **gold**：Engine
**答对**：✓  ·  **答案**：引擎主类是 **`Engine`**，定义在 `core/core_bind.h`，属于 `core_bind` 命名空间，通过 `Engine::get_singleton()` 获取实例。
**指标**：tokens=1600 · llm_calls=3 · tool_steps=2 · 耗时=14.98s · 截断=否

---

**👤 用户**：引擎主类叫什么？

> 💭 **思考**：The user is asking about the main engine class name in Godot. Let me search for it.

**🔧 `cmm_search`**({"query": "engine main class"})

> 💭 **思考**：The search didn't directly show the main engine class. Let me search more specifically.

**🔧 `cmm_search`**({"query": "Engine class core_bind"})

**🤖 Agent**：引擎主类是 **`Engine`**，定义在 `core/core_bind.h`，属于 `core_bind` 命名空间，通过 `Engine::get_singleton()` 获取实例。

**📋 工具结果**：
```
- get_main_loop  (Users-ks_128-Documents-godot-src-core.core_bind.Engine.get_main_loop)  core_bind.cpp
- ~MainLoop  (Users-ks_128-Documents-godot-src-core.os.main_loop.MainLoop.~MainLoop)  os/main_loop.h
- is_main_thread  (Users-ks_128-Documents-godot-src-core.core_bind.Thread.is_main_thread)  core_bind.cpp
- get_main_diagonal  (Users-ks_128-Documents-godot-src-core.math.basis.Basis.get_main_diagonal)  math/basis.h
- make_main_thread  (Users-ks_128-Documents-godot-src-core.os.thread.Thread.make_main_thread)  os/thread.h
```

**📋 工具结果**：
```
- Engine  (Users-ks_128-Documents-godot-src-core.core_bind.Engine.Engine)  core_bind.h
- ~EngineDebugger  (Users-ks_128-Documents-godot-src-core.core_bind.EngineDebugger.~EngineDebugger)  core_bind.cpp
- EngineDebugger  (Users-ks_128-Documents-godot-src-core.core_bind.EngineDebugger.EngineDebugger)  core_bind.h
- Engine  (Users-ks_128-Documents-godot-src-core.core_bind.Engine)  core_bind.h
- has_singleton  (Users-ks_128-Documents-godot-src-core.core_bind.Engine.has_singleton)  core_bind.cpp
```


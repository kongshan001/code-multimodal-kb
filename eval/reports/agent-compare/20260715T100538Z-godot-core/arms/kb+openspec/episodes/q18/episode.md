# q18 · code_retrieval · arm: `kb+openspec`

**题**：引擎主类叫什么？  ·  **gold**：Engine
**答对**：✓  ·  **答案**：Godot 的引擎主类是 **`Engine`**（C++ 内为 `core_bind::Engine`，位于 `core/core_bind.cpp`），它是暴露给脚本层的引擎单例，提供版本、主循环、帧率等全局信息。

与之相关的核心抽象
**指标**：tokens=1489 · llm_calls=2 · tool_steps=1 · 耗时=18.24s · 截断=否

---

**👤 用户**：引擎主类叫什么？

> 💭 **思考**：The user is asking about the main engine class in Godot. Let me search for it.

**🔧 `cmm_search`**({"query": "engine main class"})

> 💭 **思考**：The search returned `core_bind.Engine` which is the scripting API binding for the engine. The actual C++ engine main class is likely `Engine` in `core_bind.cpp`, but the user might be asking about the core engine class. Let me provide the answer based on what was found.

The main engine class in God

**🤖 Agent**：Godot 的引擎主类是 **`Engine`**（C++ 内为 `core_bind::Engine`，位于 `core/core_bind.cpp`），它是暴露给脚本层的引擎单例，提供版本、主循环、帧率等全局信息。

与之相关的核心抽象还有 `MainLoop`（主循环基类，`core/os/main_loop.h`）。

**📋 工具结果**：
```
- get_main_loop  (Users-ks_128-Documents-godot-src-core.core_bind.Engine.get_main_loop)  core_bind.cpp
- ~MainLoop  (Users-ks_128-Documents-godot-src-core.os.main_loop.MainLoop.~MainLoop)  os/main_loop.h
- is_main_thread  (Users-ks_128-Documents-godot-src-core.core_bind.Thread.is_main_thread)  core_bind.cpp
- get_main_diagonal  (Users-ks_128-Documents-godot-src-core.math.basis.Basis.get_main_diagonal)  math/basis.h
- make_main_thread  (Users-ks_128-Documents-godot-src-core.os.thread.Thread.make_main_thread)  os/thread.h
```


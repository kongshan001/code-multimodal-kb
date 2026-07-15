# q18 · code_retrieval · arm: `kb`

**题**：引擎主类叫什么？  ·  **gold**：Engine
**答对**：✓  ·  **答案**：引擎主类是 **`Engine`**（C++ 实现为 `core_bind::Engine`，定义在 `core_bind.cpp`，是暴露给脚本的 `Engine` 单例）。

- 关键方法：`Engine::get_main_loop(
**指标**：tokens=1221 · llm_calls=2 · tool_steps=1 · 耗时=20.46s · 截断=否

---

**👤 用户**：引擎主类叫什么？

> 💭 **思考**：The user is asking about the main engine class in Godot. Let me search for it.

**🔧 `cmm_search`**({"query": "engine main class"})

> 💭 **思考**：The search returned some results but not exactly what I'm looking for. The user is asking about the "engine main class". In Godot, the main engine class exposed to scripting is `core_bind::Engine` (which is the `Engine` singleton). But there's also `Main` in `main/main.cpp`. Let me check what's the 

**🤖 Agent**：引擎主类是 **`Engine`**（C++ 实现为 `core_bind::Engine`，定义在 `core_bind.cpp`，是暴露给脚本的 `Engine` 单例）。

- 关键方法：`Engine::get_main_loop()` 返回当前的 `MainLoop`。

**📋 工具结果**：
```
- get_main_loop  (Users-ks_128-Documents-godot-src-core.core_bind.Engine.get_main_loop)  core_bind.cpp
- ~MainLoop  (Users-ks_128-Documents-godot-src-core.os.main_loop.MainLoop.~MainLoop)  os/main_loop.h
- is_main_thread  (Users-ks_128-Documents-godot-src-core.core_bind.Thread.is_main_thread)  core_bind.cpp
- get_main_diagonal  (Users-ks_128-Documents-godot-src-core.math.basis.Basis.get_main_diagonal)  math/basis.h
- make_main_thread  (Users-ks_128-Documents-godot-src-core.os.thread.Thread.make_main_thread)  os/thread.h
```


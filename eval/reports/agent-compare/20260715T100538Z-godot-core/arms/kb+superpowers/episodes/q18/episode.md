# q18 · code_retrieval · arm: `kb+superpowers`

**题**：引擎主类叫什么？  ·  **gold**：Engine
**答对**：✓  ·  **答案**：引擎的主类是 **`Engine`**，定义在 `core_bind.cpp` / `core_bind.h` 中（即 `core_bind.Engine`），是暴露给脚本的引擎信息单例。

此外还有：
- **`MainLoop`**（`
**指标**：tokens=1537 · llm_calls=2 · tool_steps=1 · 耗时=17.0s · 截断=否

---

**👤 用户**：引擎主类叫什么？

> 💭 **思考**：The user is asking what the main engine class is called in Godot. Let me search for this.

**🔧 `cmm_search`**({"query": "main engine entry point class"})

> 💭 **思考**：The search shows `core_bind.cpp` has an `Engine` class. Let me also check `MainLoop` and the `Engine` class more specifically. The user asks for the "引擎主类" (main engine class). In Godot, the singleton exposed to scripts is `Engine` (in `core_bind.cpp`), and there's also `MainLoop` in `os/main_loop.h

**🤖 Agent**：引擎的主类是 **`Engine`**，定义在 `core_bind.cpp` / `core_bind.h` 中（即 `core_bind.Engine`），是暴露给脚本的引擎信息单例。

此外还有：
- **`MainLoop`**（`os/main_loop.h`）——引擎主循环基类，`SceneTree` 继承自它。

**📋 工具结果**：
```
- get_main_loop  (Users-ks_128-Documents-godot-src-core.core_bind.Engine.get_main_loop)  core_bind.cpp
- ~MainLoop  (Users-ks_128-Documents-godot-src-core.os.main_loop.MainLoop.~MainLoop)  os/main_loop.h
- is_main_thread  (Users-ks_128-Documents-godot-src-core.core_bind.Thread.is_main_thread)  core_bind.cpp
- get_main_diagonal  (Users-ks_128-Documents-godot-src-core.math.basis.Basis.get_main_diagonal)  math/basis.h
- make_main_thread  (Users-ks_128-Documents-godot-src-core.os.thread.Thread.make_main_thread)  os/thread.h
```


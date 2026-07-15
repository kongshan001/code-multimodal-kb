# q18 · code_retrieval · arm: `kb+superpowers`

**题**：引擎主类叫什么？  ·  **gold**：Engine
**答对**：✓  ·  **答案**：引擎主类是 **`core_bind::Engine`**（在 `core_bind.cpp` 中），即脚本层暴露的 `Engine` 单例类。
**指标**：tokens=1578 · llm_calls=2 · tool_steps=1 · 耗时=15.53s · 截断=否

---

**👤 用户**：引擎主类叫什么？

**🔧 `cmm_search`**({"query": "engine main class"})

**📋 工具结果**：
```
- get_main_loop  (Users-ks_128-Documents-godot-src-core.core_bind.Engine.get_main_loop)  core_bind.cpp
- ~MainLoop  (Users-ks_128-Documents-godot-src-core.os.main_loop.MainLoop.~MainLoop)  os/main_loop.h
- is_main_thread  (Users-ks_128-Documents-godot-src-core.core_bind.Thread.is_main_thread)  core_bind.cpp
- get_main_diagonal  (Users-ks_128-Documents-godot-src-core.math.basis.Basis.get_main_diagonal)  math/basis.h
- make_main_thread  (Users-ks_128-Documents-godot-src-core.os.thread.Thread.make_main_thread)  os/thread.h
```

**🤖 Agent**：引擎主类是 **`core_bind::Engine`**（在 `core_bind.cpp` 中），即脚本层暴露的 `Engine` 单例类。


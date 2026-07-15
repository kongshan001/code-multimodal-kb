# q18 · code_retrieval · arm: `no-kb`

**题**：引擎主类叫什么？  ·  **gold**：Engine
**答对**：✓  ·  **答案**：引擎主类是 **`Engine`**，定义在 `core/config/engine.h`。
**指标**：tokens=929 · llm_calls=2 · tool_steps=1 · 耗时=8.64s · 截断=否

---

**👤 用户**：引擎主类叫什么？

> 💭 **思考**：用户问的是引擎的主类名称。在 Godot 中，引擎的主类是 `Engine`。让我快速确认一下。

**🔧 `grep_code`**({"pattern": "class Engine"})

> 💭 **思考**：核心引擎主类是 `Engine`，定义在 `core/config/engine.h`。

**🤖 Agent**：引擎主类是 **`Engine`**，定义在 `core/config/engine.h`。

**📋 工具结果**：
```
matched 4 files:
/Users/ks_128/Documents/godot-src/core/config/engine.h
/Users/ks_128/Documents/godot-src/core/debugger/engine_debugger.h
/Users/ks_128/Documents/godot-src/core/debugger/engine_profiler.h
/Users/ks_128/Documents/godot-src/core/core_bind.h
```


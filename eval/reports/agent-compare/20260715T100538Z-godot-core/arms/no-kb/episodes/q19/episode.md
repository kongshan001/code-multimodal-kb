# q19 · code_retrieval · arm: `no-kb`

**题**：主循环基类叫什么？  ·  **gold**：MainLoop
**答对**：✓  ·  **答案**：Godot 的主循环基类是 **`MainLoop`**，定义在 `core/os/main_loop.h` 中。
**指标**：tokens=893 · llm_calls=2 · tool_steps=1 · 耗时=10.23s · 截断=否

---

**👤 用户**：主循环基类叫什么？

> 💭 **思考**：The user is asking about the main loop base class in Godot. Let me search for it.

**🔧 `grep_code`**({"pattern": "class MainLoop"})

> 💭 **思考**：Found it.

**🤖 Agent**：Godot 的主循环基类是 **`MainLoop`**，定义在 `core/os/main_loop.h` 中。

**📋 工具结果**：
```
matched 3 files:
/Users/ks_128/Documents/godot-src/core/os/os.h
/Users/ks_128/Documents/godot-src/core/os/main_loop.h
/Users/ks_128/Documents/godot-src/core/core_bind.h
```


# q05 · code_retrieval · arm: `no-kb`

**题**：操作系统抽象层用哪个类？  ·  **gold**：OS
**答对**：✓  ·  **答案**：`OS`

定义在 `core/os/os.h`，是 Godot 的操作系统抽象层（单例），封装文件系统、时间、线程、内存、环境变量等平台相关接口。`core_bind.h` 中的 `OS`（即 `_OS`）则是暴露给脚本的绑定版本。
**指标**：tokens=922 · llm_calls=2 · tool_steps=1 · 耗时=10.13s · 截断=否

---

**👤 用户**：操作系统抽象层用哪个类？

> 💭 **思考**：用户问的是 Godot 中"操作系统抽象层"用哪个类。让我搜索一下。

**🔧 `grep_code`**({"pattern": "class OS"})

> 💭 **思考**：The class is `OS`, defined in `core/os/os.h`.

**🤖 Agent**：`OS`

定义在 `core/os/os.h`，是 Godot 的操作系统抽象层（单例），封装文件系统、时间、线程、内存、环境变量等平台相关接口。`core_bind.h` 中的 `OS`（即 `_OS`）则是暴露给脚本的绑定版本。

**📋 工具结果**：
```
matched 2 files:
/Users/ks_128/Documents/godot-src/core/os/os.h
/Users/ks_128/Documents/godot-src/core/core_bind.h
```


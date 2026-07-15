# q05 · code_retrieval · arm: `kb+superpowers`

**题**：操作系统抽象层用哪个类？  ·  **gold**：OS
**答对**：✓  ·  **答案**：操作系统抽象层用 **`OS`** 类，定义在 `core/os/os.h`，是跨平台 OS 接口的基类。

另外 `core_bind::OS`（在 `core_bind.cpp` 中）是暴露给脚本层的绑定封装。
**指标**：tokens=1439 · llm_calls=2 · tool_steps=1 · 耗时=8.75s · 截断=否

---

**👤 用户**：操作系统抽象层用哪个类？

> 💭 **思考**：The user is asking about which class is used as the OS abstraction layer in Godot's core.

**🔧 `cmm_search`**({"query": "operating system abstraction layer"})

> 💭 **思考**：The search results show `os/os.OS` and `core_bind.OS`. The primary OS abstraction layer class in Godot is `OS` (defined in `core/os/os.h`). There's also `core_bind::OS` which is the GDScript-facing binding. Let me give a concise answer.

**🤖 Agent**：操作系统抽象层用 **`OS`** 类，定义在 `core/os/os.h`，是跨平台 OS 接口的基类。

另外 `core_bind::OS`（在 `core_bind.cpp` 中）是暴露给脚本层的绑定封装。

**📋 工具结果**：
```
- get_system_fonts  (Users-ks_128-Documents-godot-src-core.core_bind.OS.get_system_fonts)  core_bind.cpp
- get_system_dir  (Users-ks_128-Documents-godot-src-core.core_bind.OS.get_system_dir)  core_bind.cpp
- get_system_dir  (Users-ks_128-Documents-godot-src-core.os.os.OS.get_system_dir)  os/os.cpp
- get_system_fonts  (Users-ks_128-Documents-godot-src-core.os.os.OS.get_system_fonts)  os/os.h
- get_system_ca_certificates  (Users-ks_128-Documents-godot-src-core.core_bind.OS.get_system_ca_certificates)  core_bind.cpp
```


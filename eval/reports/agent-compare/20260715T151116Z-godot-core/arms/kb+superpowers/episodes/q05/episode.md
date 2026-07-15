# q05 · code_retrieval · arm: `kb+superpowers`

**题**：操作系统抽象层用哪个类？  ·  **gold**：OS
**答对**：✓  ·  **答案**：操作系统抽象层的核心类是 **`OS`**（定义于 `os/os.h` / `os/os.cpp`）。

它是 Godot 跨平台抽象层的主接口，各具体平台（`OS_Unix`、`OS_Windows` 等）继承自它。脚本层通过 **`co
**指标**：tokens=413 · llm_calls=2 · tool_steps=1 · 耗时=12.62s · 截断=否

---

**👤 用户**：操作系统抽象层用哪个类？

> 💭 **思考**：用户问的是 Godot 代码库中操作系统抽象层用哪个类。让我搜索一下。

**🔧 `cmm_search`**({"query": "operating system abstraction layer"})

> 💭 **思考**：The search results show `OS` class in `os/os.h` and `os/os.cpp`. Let me confirm this is the operating system abstraction layer.

**🤖 Agent**：操作系统抽象层的核心类是 **`OS`**（定义于 `os/os.h` / `os/os.cpp`）。

它是 Godot 跨平台抽象层的主接口，各具体平台（`OS_Unix`、`OS_Windows` 等）继承自它。脚本层通过 **`core_bind::OS`**（`core_bind.cpp`）暴露给 GDScript。

**📋 工具结果**：
```
- get_system_fonts  (Users-ks_128-Documents-godot-src-core.core_bind.OS.get_system_fonts)  core_bind.cpp
- get_system_dir  (Users-ks_128-Documents-godot-src-core.core_bind.OS.get_system_dir)  core_bind.cpp
- get_system_dir  (Users-ks_128-Documents-godot-src-core.os.os.OS.get_system_dir)  os/os.cpp
- get_system_fonts  (Users-ks_128-Documents-godot-src-core.os.os.OS.get_system_fonts)  os/os.h
- get_system_ca_certificates  (Users-ks_128-Documents-godot-src-core.core_bind.OS.get_system_ca_certificates)  core_bind.cpp
```


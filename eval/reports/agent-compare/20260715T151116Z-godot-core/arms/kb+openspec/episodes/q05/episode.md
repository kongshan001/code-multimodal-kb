# q05 · code_retrieval · arm: `kb+openspec`

**题**：操作系统抽象层用哪个类？  ·  **gold**：OS
**答对**：✓  ·  **答案**：操作系统抽象层用的是 **`OS`** 类（定义于 `core/os/os.h` / `core/os/os.cpp`）。各平台提供其子类（如 `OS_Unix`、`OS_Windows` 等）实现具体平台行为。
**指标**：tokens=1377 · llm_calls=2 · tool_steps=1 · 耗时=7.19s · 截断=否

---

**👤 用户**：操作系统抽象层用哪个类？

> 💭 **思考**：The user is asking about which class represents the OS abstraction layer in Godot's core. Let me search for it.

**🔧 `cmm_search`**({"query": "OS abstraction layer operating system"})

> 💭 **思考**：The OS abstraction layer class is `OS`, defined in `core/os/os.h` and `core/os/os.cpp`.

**🤖 Agent**：操作系统抽象层用的是 **`OS`** 类（定义于 `core/os/os.h` / `core/os/os.cpp`）。各平台提供其子类（如 `OS_Unix`、`OS_Windows` 等）实现具体平台行为。

**📋 工具结果**：
```
- get_system_dir  (Users-ks_128-Documents-godot-src-core.os.os.OS.get_system_dir)  os/os.cpp
- get_system_fonts  (Users-ks_128-Documents-godot-src-core.os.os.OS.get_system_fonts)  os/os.h
- get_system_ca_certificates  (Users-ks_128-Documents-godot-src-core.os.os.OS.get_system_ca_certificates)  os/os.h
- get_system_font_path  (Users-ks_128-Documents-godot-src-core.os.os.OS.get_system_font_path)  os/os.h
- get_system_font_path_for_text  (Users-ks_128-Documents-godot-src-core.os.os.OS.get_system_font_path_for_text)  os/os.h
```


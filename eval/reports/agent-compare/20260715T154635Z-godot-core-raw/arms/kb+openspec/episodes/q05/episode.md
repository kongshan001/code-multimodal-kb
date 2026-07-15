# q05 · code_retrieval · arm: `kb+openspec`

**题**：操作系统抽象层用哪个类？  ·  **gold**：OS
**答对**：✓  ·  **答案**：操作系统抽象层使用的是 **`OS`** 类（定义在 `core/os/os.h` / `core/os/os.cpp`）。

它提供了对底层操作系统的统一抽象接口，包括：
- 文件系统操作（`get_system_dir`、`get_sy
**指标**：tokens=1596 · llm_calls=2 · tool_steps=1 · 耗时=10.24s · 截断=否

---

**👤 用户**：操作系统抽象层用哪个类？

**🔧 `cmm_search`**({"query": "operating system abstraction layer OS"})

**📋 工具结果**：
```
- get_system_dir  (Users-ks_128-Documents-godot-src-core.os.os.OS.get_system_dir)  os/os.cpp
- get_system_fonts  (Users-ks_128-Documents-godot-src-core.os.os.OS.get_system_fonts)  os/os.h
- get_system_ca_certificates  (Users-ks_128-Documents-godot-src-core.os.os.OS.get_system_ca_certificates)  os/os.h
- get_system_font_path  (Users-ks_128-Documents-godot-src-core.os.os.OS.get_system_font_path)  os/os.h
- get_system_font_path_for_text  (Users-ks_128-Documents-godot-src-core.os.os.OS.get_system_font_path_for_text)  os/os.h
```

**🤖 Agent**：操作系统抽象层使用的是 **`OS`** 类（定义在 `core/os/os.h` / `core/os/os.cpp`）。

它提供了对底层操作系统的统一抽象接口，包括：
- 文件系统操作（`get_system_dir`、`get_system_font_path` 等）
- 系统字体（`get_system_fonts`）
- 系统证书（`get_system_ca_certificates`）
- 命令行参数、环境变量、线程、时间等

各平台（Windows、Linux、macOS、Android、iOS 等）通过继承 `OS` 来实现各自的平台特定逻辑（如 `OS_Unix`、`OS


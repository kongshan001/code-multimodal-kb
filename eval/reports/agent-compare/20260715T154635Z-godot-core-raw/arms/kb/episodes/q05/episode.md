# q05 · code_retrieval · arm: `kb`

**题**：操作系统抽象层用哪个类？  ·  **gold**：OS
**答对**：✓  ·  **答案**：操作系统抽象层使用的是 **`OS`** 类（定义在 `core/os/os.h` / `core/os/os.cpp`）。

它是 Godot 对底层操作系统的统一抽象接口，提供文件系统路径、系统字体、系统目录、CA 证书等平台无关的访问
**指标**：tokens=673 · llm_calls=2 · tool_steps=1 · 耗时=15.6s · 截断=否

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

它是 Godot 对底层操作系统的统一抽象接口，提供文件系统路径、系统字体、系统目录、CA 证书等平台无关的访问接口。各平台（Windows、Linux、macOS、Android 等）通过继承 `OS` 类来实现各自的具体逻辑（如 `OS_Unix`、`OS_Windows` 等）。


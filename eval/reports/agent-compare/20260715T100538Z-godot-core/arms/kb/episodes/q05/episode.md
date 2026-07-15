# q05 · code_retrieval · arm: `kb`

**题**：操作系统抽象层用哪个类？  ·  **gold**：OS
**答对**：✓  ·  **答案**：`OS`（定义于 `core/os/os.h` / `os.cpp`）

所有平台特定的功能（文件系统、环境变量、时间、命令行、内存、打印等）都通过这个抽象基类暴露，具体平台通过派生子类（如 `OS_Unix`、`OS_Windows` 等
**指标**：tokens=1052 · llm_calls=2 · tool_steps=1 · 耗时=10.97s · 截断=否

---

**👤 用户**：操作系统抽象层用哪个类？

> 💭 **思考**：The user is asking about which class represents the OS abstraction layer in Godot core/. Let me search for it.

**🔧 `cmm_search`**({"query": "OS abstraction layer"})

> 💭 **思考**：The answer is clear: the `OS` class is the OS abstraction layer.

**🤖 Agent**：`OS`（定义于 `core/os/os.h` / `os.cpp`）

所有平台特定的功能（文件系统、环境变量、时间、命令行、内存、打印等）都通过这个抽象基类暴露，具体平台通过派生子类（如 `OS_Unix`、`OS_Windows` 等）实现细节。

**📋 工具结果**：
```
- OS  (Users-ks_128-Documents-godot-src-core.os.os.OS.OS)  os/os.cpp
- ~OS  (Users-ks_128-Documents-godot-src-core.os.os.OS.~OS)  os/os.cpp
- print  (Users-ks_128-Documents-godot-src-core.os.os.OS.print)  os/os.cpp
- printerr  (Users-ks_128-Documents-godot-src-core.os.os.OS.printerr)  os/os.cpp
- alert  (Users-ks_128-Documents-godot-src-core.os.os.OS.alert)  os/os.cpp
```


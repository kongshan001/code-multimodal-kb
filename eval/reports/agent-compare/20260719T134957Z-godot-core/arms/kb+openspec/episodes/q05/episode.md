# q05 · code_retrieval · arm: `kb+openspec`

- **题**：操作系统抽象层用哪个类？
- **gold**：OS
- **答对**：✓
- **答案**：`OS`
- **指标**：tokens=3965 · llm_calls=3 · tool_steps=2 · 耗时=9.17s · 截断=否

---

**👤 用户**：操作系统抽象层用哪个类？

> 💭 **思考**：用户在问"操作系统抽象层用哪个类？"，这是关于 Godot 代码库的问题。我需要使用 cmm_search 工具来查找相关的类。

根据我的理解，Godot 中操作系统抽象层应该是 OS 类。让我搜索一下确认。

**🔧 `cmm_search`**({"query": "OS operating system abstraction"})

> 💭 **思考**：搜索结果指向 OS 类。让我搜索 OS 类本身。

**🔧 `cmm_search`**({"query": "class OS"})

> 💭 **思考**：找到了。根据搜索结果，Godot 的操作系统抽象层是 `OS` 类，位于 os/os.h 和 os/os.cpp 中。这是答案。

**🤖 Agent**：`OS`

**📋 工具结果**：
```
- get_system_dir  (Users-ks_128-Documents-godot-src-core.os.os.OS.get_system_dir)  os/os.cpp
- get_system_fonts  (Users-ks_128-Documents-godot-src-core.os.os.OS.get_system_fonts)  os/os.h
- get_system_ca_certificates  (Users-ks_128-Documents-godot-src-core.os.os.OS.get_system_ca_certificates)  os/os.h
- get_system_font_path  (Users-ks_128-Documents-godot-src-core.os.os.OS.get_system_font_path)  os/os.h
- get_system_font_path_for_text  (Users-ks_128-Documents-godot-src-core.os.os.OS.get_system_font_path_for_text)  os/os.h
```

**📋 工具结果**：
```
- OS  (Users-ks_128-Documents-godot-src-core.os.os.OS.OS)  os/os.cpp
- ~OS  (Users-ks_128-Documents-godot-src-core.os.os.OS.~OS)  os/os.cpp
- print  (Users-ks_128-Documents-godot-src-core.os.os.OS.print)  os/os.cpp
- printerr  (Users-ks_128-Documents-godot-src-core.os.os.OS.printerr)  os/os.cpp
- alert  (Users-ks_128-Documents-godot-src-core.os.os.OS.alert)  os/os.cpp
```


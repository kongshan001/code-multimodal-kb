# q05 · code_retrieval · arm: `kb`

- **题**：操作系统抽象层用哪个类？
- **gold**：OS
- **答对**：✓
- **答案**：`OS`
- **指标**：tokens=3167 · llm_calls=3 · tool_steps=2 · 耗时=8.27s · 截断=否

---

**👤 用户**：操作系统抽象层用哪个类？

> 💭 **思考**：用户问"操作系统抽象层用哪个类？"这是在问Godot代码库中的操作系统抽象层。

我需要用代码知识库搜索相关的类。在Godot中，操作系统抽象层通常与OS相关的类有关。

让我搜索一下：

**🔧 `cmm_search`**({"query": "操作系统抽象层 OS abstract"})

> 💭 **思考**：搜索结果显示了`OS`类，这应该就是操作系统抽象层的类。让我再搜索一下更具体的信息：

**🔧 `cmm_search`**({"query": "OS class operating system"})

> 💭 **思考**：搜索结果证实了`OS`类就是操作系统抽象层。根据要求，我应该直接用符号名作答，不要长解释。答案简短，直接给类名。

**🤖 Agent**：`OS`

**📋 工具结果**：
```
- is_abstract  (Users-ks_128-Documents-godot-src-core.object.class_db.ClassDB.is_abstract)  object/class_db.cpp
- is_abstract  (Users-ks_128-Documents-godot-src-core.object.script_language_extension.ScriptExtension.is_abstract)  object/script_language_extension.h
- is_global_class_abstract  (Users-ks_128-Documents-godot-src-core.object.script_language.ScriptServer.is_global_class_abstract)  object/script_language.cpp
- OS  (Users-ks_128-Documents-godot-src-core.os.os.OS.OS)  os/os.cpp
- ~OS  (Users-ks_128-Documents-godot-src-core.os.os.OS.~OS)  os/os.cpp
```

**📋 工具结果**：
```
- get_system_dir  (Users-ks_128-Documents-godot-src-core.os.os.OS.get_system_dir)  os/os.cpp
- get_system_fonts  (Users-ks_128-Documents-godot-src-core.os.os.OS.get_system_fonts)  os/os.h
- get_system_ca_certificates  (Users-ks_128-Documents-godot-src-core.os.os.OS.get_system_ca_certificates)  os/os.h
- get_system_font_path  (Users-ks_128-Documents-godot-src-core.os.os.OS.get_system_font_path)  os/os.h
- get_system_font_path_for_text  (Users-ks_128-Documents-godot-src-core.os.os.OS.get_system_font_path_for_text)  os/os.h
```


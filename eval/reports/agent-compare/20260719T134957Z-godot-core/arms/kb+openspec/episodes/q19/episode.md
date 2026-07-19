# q19 · code_retrieval · arm: `kb+openspec`

- **题**：主循环基类叫什么？
- **gold**：MainLoop
- **答对**：✓
- **答案**：`MainLoop`
- **指标**：tokens=5564 · llm_calls=4 · tool_steps=3 · 耗时=9.25s · 截断=否

---

**👤 用户**：主循环基类叫什么？

> 💭 **思考**：用户问"主循环基类叫什么？"这是在问Godot引擎中主循环的基类名称。

我需要在Godot代码库中搜索主循环相关的类。在Godot中，主循环通常涉及MainLoop或类似的概念。

让我搜索一下。

**🔧 `cmm_search`**({"query": "MainLoop base class"})

> 💭 **思考**：搜索结果显示了 `MainLoop` 类，这就是主循环基类。让我确认一下这个类的定义。

**🔧 `read_file`**({"path": "os/main_loop.h"})

> 💭 **思考**：路径错误。让我根据搜索结果中的完整路径再试一下。

**🔧 `cmm_search`**({"query": "class MainLoop"})

> 💭 **思考**：好的，搜索结果显示了 `MainLoop` 类，这个类定义在 `os/main_loop.h` 中。虽然之前读取文件失败，但从搜索结果可以明确看到：

1. `MainLoop` 类本身
2. 它的方法如 `initialize` 和 `process`
3. 析构函数 `~MainLoop`

这个类就是Godot的主循环基类。答案很明确，就是 `MainLoop`。

**🤖 Agent**：`MainLoop`

**📋 工具结果**：
```
- ~MainLoop  (Users-ks_128-Documents-godot-src-core.os.main_loop.MainLoop.~MainLoop)  os/main_loop.h
- get_global_class_base  (Users-ks_128-Documents-godot-src-core.object.script_language.ScriptServer.get_global_class_base)  object/script_language.cpp
- get_global_class_native_base  (Users-ks_128-Documents-godot-src-core.object.script_language.ScriptServer.get_global_class_native_base)  object/script_language.cpp
- add_resource_base_extension  (Users-ks_128-Documents-godot-src-core.object.class_db.ClassDB.add_resource_base_extension)  object/class_db.cpp
- get_resource_base_extensions  (Users-
```

**📋 工具结果**：
```
(read error: [Errno 2] No such file or directory: 'os/main_loop.h')
```

**📋 工具结果**：
```
- ~MainLoop  (Users-ks_128-Documents-godot-src-core.os.main_loop.MainLoop.~MainLoop)  os/main_loop.h
- MainLoop  (Users-ks_128-Documents-godot-src-core.core_bind.MainLoop)  core_bind.h
- MainLoop  (Users-ks_128-Documents-godot-src-core.os.os.MainLoop)  os/os.h
- initialize  (Users-ks_128-Documents-godot-src-core.os.main_loop.MainLoop.initialize)  os/main_loop.cpp
- process  (Users-ks_128-Documents-godot-src-core.os.main_loop.MainLoop.process)  os/main_loop.cpp
```


# q18 · code_retrieval · arm: `kb+superpowers`

- **题**：引擎主类叫什么？
- **gold**：Engine
- **答对**：✓
- **答案**：`Engine`
- **指标**：tokens=7448 · llm_calls=5 · tool_steps=4 · 耗时=11.81s · 截断=否

---

**👤 用户**：引擎主类叫什么？

> 💭 **思考**：用户问"引擎主类叫什么？"，这是在问 Godot 引擎的核心类。我需要搜索 Godot 代码库来找到这个主类。

让我用 cmm_search 来搜索相关的符号。

**🔧 `cmm_search`**({"query": "engine main class core"})

> 💭 **思考**：这个搜索没有直接返回引擎主类。让我换个方式搜索，搜索 "Engine" 类：

**🔧 `cmm_search`**({"query": "Engine class"})

> 💭 **思考**：好的，找到了 `Engine` 类。看起来是 `core/config/engine/engine.h` 中定义的 `Engine` 类。让我再读取一下文件确认：

**🔧 `read_file`**({"path": "core/config/engine/engine.h"})

> 💭 **思考**：文件路径不对。让我尝试读取正确的路径：

**🔧 `read_file`**({"path": "config/engine.h"})

> 💭 **思考**：路径还是不对。让我直接从搜索结果看，有几个匹配：
- `core/config/engine.Engine.Engine`
- `core_bind.Engine.Engine`

看起来 `Engine` 就是 Godot 引擎的主类。我应该直接回答用户。

**🤖 Agent**：`Engine`

**📋 工具结果**：
```
- get_main_loop  (Users-ks_128-Documents-godot-src-core.core_bind.Engine.get_main_loop)  core_bind.cpp
- ~MainLoop  (Users-ks_128-Documents-godot-src-core.os.main_loop.MainLoop.~MainLoop)  os/main_loop.h
- is_main_thread  (Users-ks_128-Documents-godot-src-core.core_bind.Thread.is_main_thread)  core_bind.cpp
- get_main_diagonal  (Users-ks_128-Documents-godot-src-core.math.basis.Basis.get_main_diagonal)  math/basis.h
- make_main_thread  (Users-ks_128-Documents-godot-src-core.os.thread.Thread.make_main_thread)  os/thread.h
```

**📋 工具结果**：
```
- Engine  (Users-ks_128-Documents-godot-src-core.config.engine.Engine.Engine)  config/engine.cpp
- ~Engine  (Users-ks_128-Documents-godot-src-core.config.engine.Engine.~Engine)  config/engine.cpp
- Engine  (Users-ks_128-Documents-godot-src-core.core_bind.Engine.Engine)  core_bind.h
- print_header  (Users-ks_128-Documents-godot-src-core.config.engine.Engine.print_header)  config/engine.cpp
- add_singleton  (Users-ks_128-Documents-godot-src-core.config.engine.Engine.add_singleton)  config/engine.cpp
```

**📋 工具结果**：
```
(read error: [Errno 2] No such file or directory: 'core/config/engine/engine.h')
```

**📋 工具结果**：
```
(read error: [Errno 2] No such file or directory: 'config/engine.h')
```


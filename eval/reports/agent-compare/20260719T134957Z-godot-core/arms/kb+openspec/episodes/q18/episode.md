# q18 · code_retrieval · arm: `kb+openspec`

- **题**：引擎主类叫什么？
- **gold**：Engine
- **答对**：✓
- **答案**：`Engine`
- **指标**：tokens=9119 · llm_calls=6 · tool_steps=5 · 耗时=13.02s · 截断=否

---

**👤 用户**：引擎主类叫什么？

> 💭 **思考**：用户问"引擎主类叫什么？"，这是在问 Godot 引擎的核心类名。

我需要使用代码知识库搜索 Godot core/ 的相关符号。让我搜索一下引擎主类相关的信息。

**🔧 `cmm_search`**({"query": "引擎主类 core engine main class"})

> 💭 **思考**：搜索结果不太直接。让我尝试搜索 "Engine" 类本身：

**🔧 `cmm_search`**({"query": "Engine class"})

> 💭 **思考**：好的，看起来 `Engine` 类是引擎的主要类。根据搜索结果，有两个位置：
1. `config/engine.cpp` 中的 `Engine` 类
2. `core_bind.h` 中的 `Engine` 类

让我读一下相关文件来确认：

**🔧 `read_file`**({"path": "core/core_bind.h"})

> 💭 **思考**：路径不对。让我直接用搜索结果显示的路径格式试试：

**🔧 `read_file`**({"path": "config/engine.h"})

> 💭 **思考**：看起来我需要使用正确的路径格式。让我重新搜索看看正确的文件位置：

**🔧 `cmm_search`**({"query": "class Engine"})

> 💭 **思考**：根据搜索结果，Godot 引擎的主类是 `Engine`。这个类出现在两个位置：
1. `config/engine.cpp` 中的 `Engine` 类（看起来是配置相关的）
2. `core_bind.h` 中的 `Engine` 类（看起来是核心绑定）

用户问的是"引擎主类"，答案应该是 `Engine`。

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
(read error: [Errno 2] No such file or directory: 'core/core_bind.h')
```

**📋 工具结果**：
```
(read error: [Errno 2] No such file or directory: 'config/engine.h')
```

**📋 工具结果**：
```
- Engine  (Users-ks_128-Documents-godot-src-core.config.engine.Engine.Engine)  config/engine.cpp
- ~Engine  (Users-ks_128-Documents-godot-src-core.config.engine.Engine.~Engine)  config/engine.cpp
- Engine  (Users-ks_128-Documents-godot-src-core.core_bind.Engine.Engine)  core_bind.h
- print_header  (Users-ks_128-Documents-godot-src-core.config.engine.Engine.print_header)  config/engine.cpp
- add_singleton  (Users-ks_128-Documents-godot-src-core.config.engine.Engine.add_singleton)  config/engine.cpp
```


# q18 · code_retrieval · arm: `kb`

- **题**：引擎主类叫什么？
- **gold**：Engine
- **答对**：✓
- **答案**：`Engine`
- **指标**：tokens=12654 · llm_calls=9 · tool_steps=8 · 耗时=17.81s · 截断=否

---

**👤 用户**：引擎主类叫什么？

> 💭 **思考**：用户问"引擎主类叫什么？"，这是关于Godot引擎的。我需要查找Godot core代码库中的引擎主类。

让我搜索一下相关的类。通常游戏引擎的主类可能叫Engine、Core、Game之类的。让我先搜索看看。

**🔧 `cmm_search`**({"query": "engine main class core"})

> 💭 **思考**：搜索结果显示了 `MainLoop` 类，这可能是引擎的主类。让我再搜索一下看看是否有更明确的Engine类。

**🔧 `cmm_search`**({"query": "Engine class"})

> 💭 **思考**：好的，找到了 `Engine` 类。这应该是Godot引擎的主类。让我再验证一下。

**🔧 `read_file`**({"path": "config/engine.h"})

> 💭 **思考**：路径不对，让我用完整路径再试试。

**🔧 `read_file`**({"path": "core/config/engine.h"})

> 💭 **思考**：让我直接从搜索结果中看到的路径来读取。根据搜索结果，Engine类在config/engine.cpp中，同时也有core_bind.h中也有Engine的引用。让我尝试读取。

**🔧 `read_file`**({"path": "/Users/ks_128/Documents/godot/src/core/config/engine.h"})

> 💭 **思考**：路径可能不对，让我尝试不同的路径格式。

**🔧 `read_file`**({"path": "config/engine.cpp"})

> 💭 **思考**：看起来我无法直接读取文件，但是从搜索结果中我已经找到了 `Engine` 类。根据搜索结果，在 Godot 代码库中有一个 `Engine` 类，这应该是引擎的主类。让我再确认一下是否有其他可能的候选类。

**🔧 `cmm_search`**({"query": "Godot main class initialize"})

> 💭 **思考**：从搜索结果来看，`Engine` 类很可能是Godot引擎的主类。这是配置和核心引擎功能的中心类。根据搜索结果，Engine类存在于 `core/config/engine.cpp` 和 `core/core_bind.h` 中。

让我再快速验证一下是否有其他的候选类。

**🔧 `cmm_search`**({"query": "Core godot main"})

> 💭 **思考**：从所有的搜索结果来看，`Engine` 类应该是Godot引擎的主类。这个类包含了引擎的核心功能，包括获取主循环（`get_main_loop`）等。

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
(read error: [Errno 2] No such file or directory: 'config/engine.h')
```

**📋 工具结果**：
```
(read error: [Errno 2] No such file or directory: 'core/config/engine.h')
```

**📋 工具结果**：
```
(read error: [Errno 2] No such file or directory: '/Users/ks_128/Documents/godot/src/core/config/engine.h')
```

**📋 工具结果**：
```
(read error: [Errno 2] No such file or directory: 'config/engine.cpp')
```

**📋 工具结果**：
```
- initialize  (Users-ks_128-Documents-godot-src-core.os.main_loop.MainLoop.initialize)  os/main_loop.cpp
- initialize_class  (Users-ks_128-Documents-godot-src-core.object.object.Object.initialize_class)  object/object.cpp
- initialize  (Users-ks_128-Documents-godot-src-core.object.gdtype.GDType.initialize)  object/gdtype.cpp
- _initialize  (Users-ks_128-Documents-godot-src-core.object.object.Object._initialize)  object/object.cpp
- initialize  (Users-ks_128-Documents-godot-src-core.extension.godot_instance.GodotInstance.initialize)  extension/godot_instance.cpp
```

**📋 工具结果**：
```
- ~MainLoop  (Users-ks_128-Documents-godot-src-core.os.main_loop.MainLoop.~MainLoop)  os/main_loop.h
- is_main_thread  (Users-ks_128-Documents-godot-src-core.core_bind.Thread.is_main_thread)  core_bind.cpp
- get_main_loop  (Users-ks_128-Documents-godot-src-core.core_bind.Engine.get_main_loop)  core_bind.cpp
- get_main_diagonal  (Users-ks_128-Documents-godot-src-core.math.basis.Basis.get_main_diagonal)  math/basis.h
- make_main_thread  (Users-ks_128-Documents-godot-src-core.os.thread.Thread.make_main_thread)  os/thread.h
```


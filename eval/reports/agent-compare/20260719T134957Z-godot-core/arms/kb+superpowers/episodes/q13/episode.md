# q13 · code_retrieval · arm: `kb+superpowers`

- **题**：加载资源用哪个类？
- **gold**：ResourceLoader
- **答对**：✓
- **答案**：`ResourceLoader`
- **指标**：tokens=2623 · llm_calls=2 · tool_steps=1 · 耗时=8.77s · 截断=否

---

**👤 用户**：加载资源用哪个类？

> 💭 **思考**：用户问"加载资源用哪个类？"，这是关于 Godot 代码库的问题。我需要搜索与资源加载相关的类。

根据我的知识，在 Godot 中加载资源通常使用 ResourceLoader 类，但让我用工具搜索一下来确认。

用户要求直接给类名，不要长解释，并且要求收敛纪律——一旦工具返回了相关符号就立刻用符号名作答。

**🔧 `cmm_search`**({"query": "load resource ResourceLoader"})

> 💭 **思考**：工具返回了 ResourceLoader 类的多个方法。最相关的符号是 ResourceLoader 类。根据用户要求，我应该直接给出类名，不要长解释。

**🤖 Agent**：`ResourceLoader`

**📋 工具结果**：
```
- _load  (Users-ks_128-Documents-godot-src-core.io.resource_loader.ResourceLoader._load)  io/resource_loader.cpp
- load  (Users-ks_128-Documents-godot-src-core.io.resource_loader.ResourceLoader.load)  io/resource_loader.cpp
- _load_start  (Users-ks_128-Documents-godot-src-core.io.resource_loader.ResourceLoader._load_start)  io/resource_loader.cpp
- _load_complete  (Users-ks_128-Documents-godot-src-core.io.resource_loader.ResourceLoader._load_complete)  io/resource_loader.cpp
- _run_load_task  (Users-ks_128-Documents-godot-src-core.io.resource_loader.ResourceLoader._run_load_task)  io/resource_
```


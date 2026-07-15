# q17 · code_retrieval · arm: `no-kb`

**题**：消息队列用哪个类？  ·  **gold**：MessageQueue
**答对**：✓  ·  **答案**：`MessageQueue`
**指标**：tokens=947 · llm_calls=2 · tool_steps=1 · 耗时=24.53s · 截断=否

---

**👤 用户**：消息队列用哪个类？

> 💭 **思考**：用户问的是 Godot 4.7 core 源码中"消息队列"用哪个类。让我搜索一下。

**🔧 `grep_code`**({"pattern": "MessageQueue"})

**🤖 Agent**：`MessageQueue`

**📋 工具结果**：
```
matched 7 files:
/Users/ks_128/Documents/godot-src/core/config/project_settings.cpp
/Users/ks_128/Documents/godot-src/core/io/resource_loader.cpp
/Users/ks_128/Documents/godot-src/core/object/worker_thread_pool.cpp
/Users/ks_128/Documents/godot-src/core/object/object.cpp
/Users/ks_128/Documents/godot-src/core/object/message_queue.cpp
/Users/ks_128/Documents/godot-src/core/object/message_queue.h
/Users/ks_128/Documents/godot-src/core/variant/callable.cpp
```


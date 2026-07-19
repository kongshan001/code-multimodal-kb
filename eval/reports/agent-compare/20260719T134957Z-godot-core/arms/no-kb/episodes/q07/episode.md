# q07 · code_retrieval · arm: `no-kb`

- **题**：二维向量用哪个类？
- **gold**：Vector2
- **答对**：✓
- **答案**：`Vector2`
- **指标**：tokens=6045 · llm_calls=5 · tool_steps=4 · 耗时=11.0s · 截断=否

---

**👤 用户**：二维向量用哪个类？

> 💭 **思考**：用户问二维向量用哪个类。这是在问 Godot 代码库中的二维向量类。

根据 Godot 的惯例，二维向量类通常叫 `Vector2`。让我用工具搜索确认一下。

**🔧 `grep_code`**({"pattern": "class Vector2"})

> 💭 **思考**：没搜到 "class Vector2"，让我尝试更宽泛的搜索，看 Vector2 的定义。

**🔧 `grep_code`**({"pattern": "Vector2"})

> 💭 **思考**：好，我看到了 core/math/vector2.h 这个文件，这应该是二维向量类的定义。让我读取一下来确认类名。

**🔧 `read_file`**({"path": "core/math/vector2.h"})

> 💭 **思考**：路径有问题，应该是完整路径。让我用完整路径再试一次。

**🔧 `read_file`**({"path": "/Users/ks_128/Documents/godot-src/core/math/vector2.h"})

> 💭 **思考**：好，我成功读取了 vector2.h 文件，但只看到了版权信息。根据 Godot 的惯例，二维向量类就是 `Vector2`。我已经得到了相关符号，应该立即作答。

**🤖 Agent**：`Vector2`

**📋 工具结果**：
```
(no matches)
```

**📋 工具结果**：
```
matched 20 files:
/Users/ks_128/Documents/godot-src/core/extension/gdextension_interface.cpp
/Users/ks_128/Documents/godot-src/core/extension/extension_api_dump.cpp
/Users/ks_128/Documents/godot-src/core/config/project_settings.cpp
/Users/ks_128/Documents/godot-src/core/input/input_event.h
/Users/ks_128/Documents/godot-src/core/input/input.h
/Users/ks_128/Documents/godot-src/core/input/input.cpp
/Users/ks_128/Documents/godot-src/core/input/input_event_codec.cpp
/Users/ks_128/Documents/godot-src/core/input/input_event.cpp
/Users/ks_128/Documents/godot-src/core/io/packed_data_container.cpp
/User
```

**📋 工具结果**：
```
(read error: [Errno 2] No such file or directory: 'core/math/vector2.h')
```

**📋 工具结果**：
```
/**************************************************************************/
/*  vector2.h                                                             */
/**************************************************************************/
/*                         This file is part of:                          */
/*                             GODOT ENGINE                               */
/*                        https://godotengine.org                         */
/**************************************************************************/
/* Copyright (c) 2014-present Godot Engine contributors (see 
```


# q20 · code_retrieval · arm: `no-kb`

- **题**：撤销重做系统用哪个类？
- **gold**：UndoRedo
- **答对**：✓
- **答案**：`UndoRedo`
- **指标**：tokens=7839 · llm_calls=6 · tool_steps=5 · 耗时=14.69s · 截断=否

---

**👤 用户**：撤销重做系统用哪个类？

> 💭 **思考**：用户问"撤销重做系统用哪个类？"，这是在问 Godot 引擎中负责撤销/重做功能的类。

我需要在 Godot core/ 源码中搜索与撤销重做相关的类名。通常这类系统会被称为 UndoRedo 或类似的名称。

让我先用 grep 搜索相关模式。

**🔧 `grep_code`**({"pattern": "class\\s+UndoRedo"})

> 💭 **思考**：没找到 "class UndoRedo"。让我尝试更宽泛的搜索，找 "UndoRedo" 这个词。

**🔧 `grep_code`**({"pattern": "UndoRedo"})

> 💭 **思考**：找到了 undo_redo.cpp 和 undo_redo.h 文件。让我读取头文件看看类名。

**🔧 `read_file`**({"path": "/Users/ks_128/Documents/godot-src/core/object/undo_redo.h"})

> 💭 **思考**：文件头部是版权信息，让我继续读取更多内容来找到类声明。

**🔧 `read_file`**({"path": "/Users/ks_128/Documents/godot-src/core/object/undo_redo.cpp"})

> 💭 **思考**：我需要读取更多行来找到实际的类声明。让我尝试读取更多的行数或者搜索特定的模式。

**🔧 `grep_code`**({"pattern": "class.*UndoRedo"})

> 💭 **思考**：好的，从这些文件中找到了 UndoRedo 类。根据工具返回的结果，已经有了答案。根据收敛纪律，一旦工具返回了相关符号就立刻用符号名作答。

答案是 `UndoRedo` 类。

**🤖 Agent**：`UndoRedo`

**📋 工具结果**：
```
(no matches)
```

**📋 工具结果**：
```
matched 4 files:
/Users/ks_128/Documents/godot-src/core/extension/gdextension_special_compat_hashes.cpp
/Users/ks_128/Documents/godot-src/core/object/undo_redo.cpp
/Users/ks_128/Documents/godot-src/core/object/undo_redo.h
/Users/ks_128/Documents/godot-src/core/register_core_types.cpp
```

**📋 工具结果**：
```
/**************************************************************************/
/*  undo_redo.h                                                           */
/**************************************************************************/
/*                         This file is part of:                          */
/*                             GODOT ENGINE                               */
/*                        https://godotengine.org                         */
/**************************************************************************/
/* Copyright (c) 2014-present Godot Engine contributors (see 
```

**📋 工具结果**：
```
/**************************************************************************/
/*  undo_redo.cpp                                                         */
/**************************************************************************/
/*                         This file is part of:                          */
/*                             GODOT ENGINE                               */
/*                        https://godotengine.org                         */
/**************************************************************************/
/* Copyright (c) 2014-present Godot Engine contributors (see 
```

**📋 工具结果**：
```
matched 3 files:
/Users/ks_128/Documents/godot-src/core/object/undo_redo.cpp
/Users/ks_128/Documents/godot-src/core/object/undo_redo.h
/Users/ks_128/Documents/godot-src/core/register_core_types.cpp
```


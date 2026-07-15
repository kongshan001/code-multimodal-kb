# q20 · code_retrieval · arm: `kb+openspec`

**题**：撤销重做系统用哪个类？  ·  **gold**：UndoRedo
**答对**：✓  ·  **答案**：撤销重做系统用的类是 **`UndoRedo`**（定义在 `core/object/undo_redo.cpp`），核心方法包括：

- `undo()` — 撤销
- `redo()` — 重做
- `discard_redo()` —
**指标**：tokens=1409 · llm_calls=2 · tool_steps=1 · 耗时=16.01s · 截断=否

---

**👤 用户**：撤销重做系统用哪个类？

> 💭 **思考**：The user is asking about which class handles the undo/redo system in Godot. Let me search for this.

**🔧 `cmm_search`**({"query": "undo redo system"})

**🤖 Agent**：撤销重做系统用的类是 **`UndoRedo`**（定义在 `core/object/undo_redo.cpp`），核心方法包括：

- `undo()` — 撤销
- `redo()` — 重做
- `discard_redo()` — 丢弃重做栈

在编辑器上下文中，通常通过 `EditorUndoRedoManager` 来间接管理多个 `UndoRedo` 实例。

**📋 工具结果**：
```
- _redo  (Users-ks_128-Documents-godot-src-core.object.undo_redo.UndoRedo._redo)  object/undo_redo.cpp
- redo  (Users-ks_128-Documents-godot-src-core.object.undo_redo.UndoRedo.redo)  object/undo_redo.cpp
- undo  (Users-ks_128-Documents-godot-src-core.object.undo_redo.UndoRedo.undo)  object/undo_redo.cpp
- ~UndoRedo  (Users-ks_128-Documents-godot-src-core.object.undo_redo.UndoRedo.~UndoRedo)  object/undo_redo.cpp
- discard_redo  (Users-ks_128-Documents-godot-src-core.object.undo_redo.UndoRedo.discard_redo)  object/undo_redo.cpp
```


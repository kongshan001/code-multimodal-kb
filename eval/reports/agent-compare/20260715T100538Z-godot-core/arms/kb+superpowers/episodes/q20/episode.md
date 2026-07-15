# q20 · code_retrieval · arm: `kb+superpowers`

**题**：撤销重做系统用哪个类？  ·  **gold**：UndoRedo
**答对**：✓  ·  **答案**：**`UndoRedo`**（`core/object/undo_redo.cpp`）

核心方法：`create_action()`、`add_do_method()`、`add_undo_method()`、`commit_action
**指标**：tokens=1421 · llm_calls=2 · tool_steps=1 · 耗时=14.12s · 截断=否

---

**👤 用户**：撤销重做系统用哪个类？

> 💭 **思考**：用户问撤销重做系统用哪个类。这在 Godot 中应该是 `UndoRedo` 类。让我搜索确认一下。

**🔧 `cmm_search`**({"query": "undo redo system"})

> 💭 **思考**：Found it.

**🤖 Agent**：**`UndoRedo`**（`core/object/undo_redo.cpp`）

核心方法：`create_action()`、`add_do_method()`、`add_undo_method()`、`commit_action()`、`undo()`、`redo()`。

**📋 工具结果**：
```
- _redo  (Users-ks_128-Documents-godot-src-core.object.undo_redo.UndoRedo._redo)  object/undo_redo.cpp
- redo  (Users-ks_128-Documents-godot-src-core.object.undo_redo.UndoRedo.redo)  object/undo_redo.cpp
- undo  (Users-ks_128-Documents-godot-src-core.object.undo_redo.UndoRedo.undo)  object/undo_redo.cpp
- ~UndoRedo  (Users-ks_128-Documents-godot-src-core.object.undo_redo.UndoRedo.~UndoRedo)  object/undo_redo.cpp
- discard_redo  (Users-ks_128-Documents-godot-src-core.object.undo_redo.UndoRedo.discard_redo)  object/undo_redo.cpp
```


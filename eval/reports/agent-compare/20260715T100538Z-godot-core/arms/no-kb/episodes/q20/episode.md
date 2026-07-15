# q20 · code_retrieval · arm: `no-kb`

**题**：撤销重做系统用哪个类？  ·  **gold**：UndoRedo
**答对**：✓  ·  **答案**：`UndoRedo`

Godot 中的撤销/重做系统由 **`UndoRedo`** 类实现（位于 `core/variant/undo_redo.cpp`）。此外编辑器层还提供了 **`EditorUndoRedoManager`** 
**指标**：tokens=811 · llm_calls=1 · tool_steps=0 · 耗时=8.65s · 截断=否

---

**👤 用户**：撤销重做系统用哪个类？

> 💭 **思考**：用户问的是撤销重做系统用哪个类。在 Godot 中，这是 `UndoRedo` 类。让我快速确认一下。

**🤖 Agent**：`UndoRedo`

Godot 中的撤销/重做系统由 **`UndoRedo`** 类实现（位于 `core/variant/undo_redo.cpp`）。此外编辑器层还提供了 **`EditorUndoRedoManager`** 来管理多个 `UndoRedo` 历史。


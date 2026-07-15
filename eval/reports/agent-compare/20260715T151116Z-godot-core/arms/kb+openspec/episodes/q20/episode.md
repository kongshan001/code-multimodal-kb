# q20 · code_retrieval · arm: `kb+openspec`

**题**：撤销重做系统用哪个类？  ·  **gold**：UndoRedo
**答对**：✓  ·  **答案**：`UndoRedo`（`core/object/undo_redo.cpp`）
**指标**：tokens=1319 · llm_calls=2 · tool_steps=1 · 耗时=7.44s · 截断=否

---

**👤 用户**：撤销重做系统用哪个类？

> 💭 **思考**：用户问的是撤销重做系统用哪个类。让我搜索一下。

**🔧 `cmm_search`**({"query": "undo redo system"})

**🤖 Agent**：`UndoRedo`（`core/object/undo_redo.cpp`）

**📋 工具结果**：
```
- _redo  (Users-ks_128-Documents-godot-src-core.object.undo_redo.UndoRedo._redo)  object/undo_redo.cpp
- redo  (Users-ks_128-Documents-godot-src-core.object.undo_redo.UndoRedo.redo)  object/undo_redo.cpp
- undo  (Users-ks_128-Documents-godot-src-core.object.undo_redo.UndoRedo.undo)  object/undo_redo.cpp
- ~UndoRedo  (Users-ks_128-Documents-godot-src-core.object.undo_redo.UndoRedo.~UndoRedo)  object/undo_redo.cpp
- discard_redo  (Users-ks_128-Documents-godot-src-core.object.undo_redo.UndoRedo.discard_redo)  object/undo_redo.cpp
```


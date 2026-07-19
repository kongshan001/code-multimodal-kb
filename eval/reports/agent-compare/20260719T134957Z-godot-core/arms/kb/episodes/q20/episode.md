# q20 · code_retrieval · arm: `kb`

- **题**：撤销重做系统用哪个类？
- **gold**：UndoRedo
- **答对**：✓
- **答案**：`UndoRedo`
- **指标**：tokens=1968 · llm_calls=2 · tool_steps=1 · 耗时=8.24s · 截断=否

---

**👤 用户**：撤销重做系统用哪个类？

> 💭 **思考**：用户问"撤销重做系统用哪个类？"，这是关于 Godot 引擎的撤销重做（Undo/Redo）系统。我需要在 Godot core/ 代码库中搜索相关的类。

让我用代码知识库搜索一下。

**🔧 `cmm_search`**({"query": "撤销重做 undo redo system"})

> 💭 **思考**：搜索结果直接显示了 `UndoRedo` 类和相关的方法，包括 `undo`、`redo`、`_redo`、`discard_redo` 等。这个类位于 `object/undo_redo.cpp` 文件中。

根据收敛纪律，工具已经返回了相关符号，我应该立即用符号名作答。

**🤖 Agent**：`UndoRedo`

**📋 工具结果**：
```
- _redo  (Users-ks_128-Documents-godot-src-core.object.undo_redo.UndoRedo._redo)  object/undo_redo.cpp
- redo  (Users-ks_128-Documents-godot-src-core.object.undo_redo.UndoRedo.redo)  object/undo_redo.cpp
- undo  (Users-ks_128-Documents-godot-src-core.object.undo_redo.UndoRedo.undo)  object/undo_redo.cpp
- ~UndoRedo  (Users-ks_128-Documents-godot-src-core.object.undo_redo.UndoRedo.~UndoRedo)  object/undo_redo.cpp
- discard_redo  (Users-ks_128-Documents-godot-src-core.object.undo_redo.UndoRedo.discard_redo)  object/undo_redo.cpp
```


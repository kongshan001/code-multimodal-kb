# q20 · code_retrieval · arm: `kb+openspec`

- **题**：撤销重做系统用哪个类？
- **gold**：UndoRedo
- **答对**：✓
- **答案**：`UndoRedo`
- **指标**：tokens=2555 · llm_calls=2 · tool_steps=1 · 耗时=6.32s · 截断=否

---

**👤 用户**：撤销重做系统用哪个类？

> 💭 **思考**：用户问"撤销重做系统用哪个类？"，这是在问 Godot 引擎中撤销/重做（undo/redo）功能使用哪个类。

这是一个直接的问题，需要我查找 Godot 代码库中与撤销/重做相关的类。我应该使用 cmm_search 工具来搜索。

让我搜索与 undo/redo 相关的类。

**🔧 `cmm_search`**({"query": "undo redo"})

> 💭 **思考**：搜索结果显示有一个 `UndoRedo` 类，它包含 `undo`、`redo` 等方法。这显然就是 Godot 中用于撤销/重做系统的类。

根据我的指示，我需要简短回答，直接给出类名，不要长解释。

**🤖 Agent**：`UndoRedo`

**📋 工具结果**：
```
- _redo  (Users-ks_128-Documents-godot-src-core.object.undo_redo.UndoRedo._redo)  object/undo_redo.cpp
- redo  (Users-ks_128-Documents-godot-src-core.object.undo_redo.UndoRedo.redo)  object/undo_redo.cpp
- undo  (Users-ks_128-Documents-godot-src-core.object.undo_redo.UndoRedo.undo)  object/undo_redo.cpp
- ~UndoRedo  (Users-ks_128-Documents-godot-src-core.object.undo_redo.UndoRedo.~UndoRedo)  object/undo_redo.cpp
- discard_redo  (Users-ks_128-Documents-godot-src-core.object.undo_redo.UndoRedo.discard_redo)  object/undo_redo.cpp
```


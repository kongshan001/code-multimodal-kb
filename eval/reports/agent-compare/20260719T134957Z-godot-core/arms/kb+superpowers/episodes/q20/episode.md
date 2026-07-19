# q20 · code_retrieval · arm: `kb+superpowers`

- **题**：撤销重做系统用哪个类？
- **gold**：UndoRedo
- **答对**：✓
- **答案**：`UndoRedo`
- **指标**：tokens=2604 · llm_calls=2 · tool_steps=1 · 耗时=8.44s · 截断=否

---

**👤 用户**：撤销重做系统用哪个类？

> 💭 **思考**：用户问的是撤销重做系统用哪个类。这是在问 Godot 引擎中的撤销/重做（Undo/Redo）功能。

让我使用代码知识库搜索相关的符号。

**🔧 `cmm_search`**({"query": "撤销 重做 undo redo"})

> 💭 **思考**：搜索结果显示了 `UndoRedo` 类的相关方法，包括 undo、redo、_redo、discard_redo 等。这清楚地表明撤销重做系统使用的类是 `UndoRedo`。

根据我的指示，一旦工具返回了相关符号就立刻用符号名作答，不要反复查。查到即答。

**🤖 Agent**：`UndoRedo`

**📋 工具结果**：
```
- _redo  (Users-ks_128-Documents-godot-src-core.object.undo_redo.UndoRedo._redo)  object/undo_redo.cpp
- redo  (Users-ks_128-Documents-godot-src-core.object.undo_redo.UndoRedo.redo)  object/undo_redo.cpp
- undo  (Users-ks_128-Documents-godot-src-core.object.undo_redo.UndoRedo.undo)  object/undo_redo.cpp
- ~UndoRedo  (Users-ks_128-Documents-godot-src-core.object.undo_redo.UndoRedo.~UndoRedo)  object/undo_redo.cpp
- discard_redo  (Users-ks_128-Documents-godot-src-core.object.undo_redo.UndoRedo.discard_redo)  object/undo_redo.cpp
```


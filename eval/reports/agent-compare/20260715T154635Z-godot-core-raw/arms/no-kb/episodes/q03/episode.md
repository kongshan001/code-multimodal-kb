# q03 · code_retrieval · arm: `no-kb`

**题**：删除对象、释放内存用哪个函数？  ·  **gold**：memdelete
**答对**：✓  ·  **答案**：在 Godot 中，删除对象/释放内存主要使用以下函数：

- **`memdelete()`** — 释放通过 `memnew()` 创建的 C++ 对象（`Object` 及其子类等）。
- **`Object::free()`** —
**指标**：tokens=467 · llm_calls=1 · tool_steps=0 · 耗时=4.45s · 截断=否

---

**👤 用户**：删除对象、释放内存用哪个函数？

**🤖 Agent**：在 Godot 中，删除对象/释放内存主要使用以下函数：

- **`memdelete()`** — 释放通过 `memnew()` 创建的 C++ 对象（`Object` 及其子类等）。
- **`Object::free()`** — 对继承自 `Object` 的对象调用，内部最终也会走到 `memdelete()`。
- **`Reference` / `RefCounted`** — 引用计数对象，引用归零时自动释放，无需手动删除。

核心用法：

```cpp
Object *obj = memnew(Object);
// ...
memdelete(obj);
```


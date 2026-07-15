# q03 · code_retrieval · arm: `kb+openspec`

**题**：删除对象、释放内存用哪个函数？  ·  **gold**：memdelete
**答对**：✓  ·  **答案**：## Godot C++ 中删除对象/释放内存

取决于对象类型：

### 1. 手动 `memnew` 创建的对象 → `memdelete`
```cpp
Object *obj = memnew(Object);
memdelete
**指标**：tokens=830 · llm_calls=1 · tool_steps=0 · 耗时=9.57s · 截断=否

---

**👤 用户**：删除对象、释放内存用哪个函数？

**🤖 Agent**：## Godot C++ 中删除对象/释放内存

取决于对象类型：

### 1. 手动 `memnew` 创建的对象 → `memdelete`
```cpp
Object *obj = memnew(Object);
memdelete(obj);
```

### 2. 引用计数对象（`RefCounted` 及其子类）→ 自动释放
- 通过 `Ref<T>` 智能指针管理，引用计数归零时自动 `memdelete`
- 不需要手动调用任何函数

### 3. 核心相关符号

| 用途 | 符号 |
|------|------|
| 分配内存 | `memnew` / `memnew_


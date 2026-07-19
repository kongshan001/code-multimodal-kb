# q09 · code_retrieval · arm: `kb`

- **题**：四元数用哪个类？
- **gold**：Quaternion
- **答对**：✓
- **答案**：`Quaternion`
- **指标**：tokens=1935 · llm_calls=2 · tool_steps=1 · 耗时=7.52s · 截断=否

---

**👤 用户**：四元数用哪个类？

> 💭 **思考**：用户问"四元数用哪个类？"，这是在询问Godot代码库中表示四元数的类。

我需要在Godot core/代码库中搜索四元数相关的类。四元数在3D引擎中通常用来表示旋转。

让我使用cmm_search工具搜索"quaternion"或相关关键词。

**🔧 `cmm_search`**({"query": "quaternion"})

> 💭 **思考**：搜索结果显示四元数使用的是 `Quaternion` 类，位于 core/math/quaternion.h 文件。

根据我的指示，我应该简短回答，直接给出类名即可，不需要长解释。一旦工具返回了相关符号就立刻用符号名作答。

**🤖 Agent**：`Quaternion`

**📋 工具结果**：
```
- Quaternion  (Users-ks_128-Documents-godot-src-core.math.quaternion.Quaternion.Quaternion)  math/quaternion.h
- length  (Users-ks_128-Documents-godot-src-core.math.quaternion.Quaternion.length)  math/quaternion.cpp
- normalize  (Users-ks_128-Documents-godot-src-core.math.quaternion.Quaternion.normalize)  math/quaternion.cpp
- normalized  (Users-ks_128-Documents-godot-src-core.math.quaternion.Quaternion.normalized)  math/quaternion.cpp
- inverse  (Users-ks_128-Documents-godot-src-core.math.quaternion.Quaternion.inverse)  math/quaternion.cpp
```


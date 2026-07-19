# q09 · code_retrieval · arm: `kb+superpowers`

- **题**：四元数用哪个类？
- **gold**：Quaternion
- **答对**：✓
- **答案**：`Quaternion`
- **指标**：tokens=2621 · llm_calls=2 · tool_steps=1 · 耗时=6.83s · 截断=否

---

**👤 用户**：四元数用哪个类？

> 💭 **思考**：用户问"四元数用哪个类"，这是在问 Godot 代码库中四元数相关的类。

根据我的角色定义，我是代码定位助手，需要用工具查找，然后用符号名作答，答案要简短。

我需要搜索 Godot core/ 中的四元数相关类。四元数通常是 "Quaternion"。让我用 cmm_search 工具搜索。

**🔧 `cmm_search`**({"query": "Quaternion"})

> 💭 **思考**：搜索到了 Quaternion 类，位于 math/quaternion.h。根据我的角色定义，一旦工具返回了相关符号就立刻用符号名作答，不要反复查。

用户问"四元数用哪个类"，答案就是 `Quaternion`。

**🤖 Agent**：`Quaternion`

**📋 工具结果**：
```
- Quaternion  (Users-ks_128-Documents-godot-src-core.math.quaternion.Quaternion.Quaternion)  math/quaternion.h
- length  (Users-ks_128-Documents-godot-src-core.math.quaternion.Quaternion.length)  math/quaternion.cpp
- normalize  (Users-ks_128-Documents-godot-src-core.math.quaternion.Quaternion.normalize)  math/quaternion.cpp
- normalized  (Users-ks_128-Documents-godot-src-core.math.quaternion.Quaternion.normalized)  math/quaternion.cpp
- inverse  (Users-ks_128-Documents-godot-src-core.math.quaternion.Quaternion.inverse)  math/quaternion.cpp
```


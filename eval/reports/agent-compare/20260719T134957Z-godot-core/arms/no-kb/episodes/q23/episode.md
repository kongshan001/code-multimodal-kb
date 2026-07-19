# q23 · code_retrieval · arm: `no-kb`

- **题**：随机数生成器用哪个类？
- **gold**：RandomNumberGenerator
- **答对**：✓
- **答案**：`RandomNumberGenerator`
- **指标**：tokens=1876 · llm_calls=2 · tool_steps=1 · 耗时=6.87s · 截断=否

---

**👤 用户**：随机数生成器用哪个类？

> 💭 **思考**：用户问的是"随机数生成器用哪个类？"，这是在询问 Godot core/ 源码中用于随机数生成的类。

我需要在 Godot core/ 源码中查找随机数相关的类。常见的随机数类可能是 `RandomNumberGenerator` 或类似的名字。

让我先 grep 一下相关的模式。

**🔧 `grep_code`**({"pattern": "RandomNumberGenerator"})

> 💭 **思考**：找到了！Godot 中用于随机数生成的类是 `RandomNumberGenerator`。

根据搜索结果，这个类的头文件和实现文件位于：
- core/math/random_number_generator.h
- core/math/random_number_generator.cpp

用户问的是"随机数生成器用哪个类？"，答案就是 `RandomNumberGenerator`。

按照指令要求，我应该直接给出符号名作为答案，简短回答，不要长解释。

**🤖 Agent**：`RandomNumberGenerator`

**📋 工具结果**：
```
matched 3 files:
/Users/ks_128/Documents/godot-src/core/math/random_number_generator.h
/Users/ks_128/Documents/godot-src/core/math/random_number_generator.cpp
/Users/ks_128/Documents/godot-src/core/register_core_types.cpp
```


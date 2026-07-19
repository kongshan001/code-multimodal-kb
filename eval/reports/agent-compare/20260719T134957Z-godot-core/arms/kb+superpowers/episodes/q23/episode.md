# q23 · code_retrieval · arm: `kb+superpowers`

- **题**：随机数生成器用哪个类？
- **gold**：RandomNumberGenerator
- **答对**：✓
- **答案**：`RandomNumberGenerator`
- **指标**：tokens=2644 · llm_calls=2 · tool_steps=1 · 耗时=7.05s · 截断=否

---

**👤 用户**：随机数生成器用哪个类？

> 💭 **思考**：用户问"随机数生成器用哪个类"，这是在问Godot代码库中的随机数生成器类。

我需要搜索Godot core/中的随机数生成器相关代码。常见的随机数生成器类可能是`RandomNumberGenerator`或类似的名称。

让我用cmm_search工具搜索一下。

**🔧 `cmm_search`**({"query": "random number generator class"})

> 💭 **思考**：找到了！Godot的随机数生成器类是`RandomNumberGenerator`。工具返回了相关的符号信息，包括类本身以及一些方法如randomize、randi、randf等。

根据指令，我应该直接用符号名作答，不要长解释。一旦工具返回了相关符号就立刻用符号名作答，不要反复查。

**🤖 Agent**：`RandomNumberGenerator`

**📋 工具结果**：
```
- RandomNumberGenerator  (Users-ks_128-Documents-godot-src-core.math.random_number_generator.RandomNumberGenerator.RandomNumberGenerator)  math/random_number_generator.h
- RandomNumberGenerator  (Users-ks_128-Documents-godot-src-core.math.random_number_generator.RandomNumberGenerator)  math/random_number_generator.h
- randomize  (Users-ks_128-Documents-godot-src-core.math.random_number_generator.RandomNumberGenerator.randomize)  math/random_number_generator.h
- randi  (Users-ks_128-Documents-godot-src-core.math.random_number_generator.RandomNumberGenerator.randi)  math/random_number_generator.
```


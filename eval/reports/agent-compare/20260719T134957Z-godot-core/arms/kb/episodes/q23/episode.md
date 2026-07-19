# q23 · code_retrieval · arm: `kb`

- **题**：随机数生成器用哪个类？
- **gold**：RandomNumberGenerator
- **答对**：✓
- **答案**：`RandomNumberGenerator`
- **指标**：tokens=1924 · llm_calls=2 · tool_steps=1 · 耗时=6.7s · 截断=否

---

**👤 用户**：随机数生成器用哪个类？

> 💭 **思考**：用户问的是"随机数生成器用哪个类？"。这是在问 Godot 代码库中用于随机数生成的类。我需要使用 cmm_search 工具来查找相关的类。

让我搜索一下随机数生成器相关的类。

**🔧 `cmm_search`**({"query": "随机数生成器 random number generator"})

> 💭 **思考**：搜索结果直接返回了 RandomNumberGenerator 类，这就是 Godot 的随机数生成器。按照要求，我直接用符号名作答，不需要长篇解释。

**🤖 Agent**：`RandomNumberGenerator`

**📋 工具结果**：
```
- RandomNumberGenerator  (Users-ks_128-Documents-godot-src-core.math.random_number_generator.RandomNumberGenerator.RandomNumberGenerator)  math/random_number_generator.h
- randomize  (Users-ks_128-Documents-godot-src-core.math.random_number_generator.RandomNumberGenerator.randomize)  math/random_number_generator.h
- randi  (Users-ks_128-Documents-godot-src-core.math.random_number_generator.RandomNumberGenerator.randi)  math/random_number_generator.h
- randf  (Users-ks_128-Documents-godot-src-core.math.random_number_generator.RandomNumberGenerator.randf)  math/random_number_generator.h
- randfn
```


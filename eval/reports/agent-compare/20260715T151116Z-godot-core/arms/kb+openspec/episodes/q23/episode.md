# q23 · code_retrieval · arm: `kb+openspec`

**题**：随机数生成器用哪个类？  ·  **gold**：RandomNumberGenerator
**答对**：✓  ·  **答案**：`RandomNumberGenerator`（定义在 `math/random_number_generator.h`）。

主要方法：`randi()`（整数）、`randf()`（浮点）、`randfn()`（正态分布）、`rando
**指标**：tokens=1367 · llm_calls=2 · tool_steps=1 · 耗时=9.61s · 截断=否

---

**👤 用户**：随机数生成器用哪个类？

> 💭 **思考**：The user is asking which class is used for random number generation in Godot. Let me search for this.

**🔧 `cmm_search`**({"query": "random number generator"})

> 💭 **思考**：Got it. The answer is `RandomNumberGenerator`.

**🤖 Agent**：`RandomNumberGenerator`（定义在 `math/random_number_generator.h`）。

主要方法：`randi()`（整数）、`randf()`（浮点）、`randfn()`（正态分布）、`randomize()`（随机种子）。

**📋 工具结果**：
```
- RandomNumberGenerator  (Users-ks_128-Documents-godot-src-core.math.random_number_generator.RandomNumberGenerator.RandomNumberGenerator)  math/random_number_generator.h
- randomize  (Users-ks_128-Documents-godot-src-core.math.random_number_generator.RandomNumberGenerator.randomize)  math/random_number_generator.h
- randi  (Users-ks_128-Documents-godot-src-core.math.random_number_generator.RandomNumberGenerator.randi)  math/random_number_generator.h
- randf  (Users-ks_128-Documents-godot-src-core.math.random_number_generator.RandomNumberGenerator.randf)  math/random_number_generator.h
- randfn
```


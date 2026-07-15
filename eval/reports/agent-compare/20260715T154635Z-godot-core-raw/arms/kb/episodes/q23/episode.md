# q23 · code_retrieval · arm: `kb`

**题**：随机数生成器用哪个类？  ·  **gold**：RandomNumberGenerator
**答对**：✓  ·  **答案**：使用 **`RandomNumberGenerator`** 类（定义在 `core/math/random_number_generator.h`）。

主要方法：
- `randomize()` — 随机化种子
- `randi()` 
**指标**：tokens=980 · llm_calls=2 · tool_steps=1 · 耗时=16.79s · 截断=否

---

**👤 用户**：随机数生成器用哪个类？

**🔧 `cmm_search`**({"query": "random number generator"})

**📋 工具结果**：
```
- RandomNumberGenerator  (Users-ks_128-Documents-godot-src-core.math.random_number_generator.RandomNumberGenerator.RandomNumberGenerator)  math/random_number_generator.h
- randomize  (Users-ks_128-Documents-godot-src-core.math.random_number_generator.RandomNumberGenerator.randomize)  math/random_number_generator.h
- randi  (Users-ks_128-Documents-godot-src-core.math.random_number_generator.RandomNumberGenerator.randi)  math/random_number_generator.h
- randf  (Users-ks_128-Documents-godot-src-core.math.random_number_generator.RandomNumberGenerator.randf)  math/random_number_generator.h
- randfn
```

**🤖 Agent**：使用 **`RandomNumberGenerator`** 类（定义在 `core/math/random_number_generator.h`）。

主要方法：
- `randomize()` — 随机化种子
- `randi()` — 随机整数
- `randf()` — 随机浮点数 [0, 1)
- `randfn()` — 正态分布随机数


# q23 · code_retrieval · arm: `kb`

**题**：随机数生成器用哪个类？  ·  **gold**：RandomNumberGenerator
**答对**：✓  ·  **答案**：用 **`RandomNumberGenerator`**（定义在 `math/random_number_generator.h`）。

主要方法：
- `randomize()` — 设置随机种子
- `randi()` — 随机整数

**指标**：tokens=1060 · llm_calls=2 · tool_steps=1 · 耗时=7.3s · 截断=否

---

**👤 用户**：随机数生成器用哪个类？

> 💭 **思考**：用户问随机数生成器用哪个类。让我搜索一下。

**🔧 `cmm_search`**({"query": "random number generator"})

**🤖 Agent**：用 **`RandomNumberGenerator`**（定义在 `math/random_number_generator.h`）。

主要方法：
- `randomize()` — 设置随机种子
- `randi()` — 随机整数
- `randf()` — 随机浮点数 [0,1]
- `randfn()` — 正态分布随机数

**📋 工具结果**：
```
- RandomNumberGenerator  (Users-ks_128-Documents-godot-src-core.math.random_number_generator.RandomNumberGenerator.RandomNumberGenerator)  math/random_number_generator.h
- randomize  (Users-ks_128-Documents-godot-src-core.math.random_number_generator.RandomNumberGenerator.randomize)  math/random_number_generator.h
- randi  (Users-ks_128-Documents-godot-src-core.math.random_number_generator.RandomNumberGenerator.randi)  math/random_number_generator.h
- randf  (Users-ks_128-Documents-godot-src-core.math.random_number_generator.RandomNumberGenerator.randf)  math/random_number_generator.h
- randfn
```


# q23 · code_retrieval · arm: `kb+openspec`

- **题**：随机数生成器用哪个类？
- **gold**：RandomNumberGenerator
- **答对**：✓
- **答案**：`RandomNumberGenerator`
- **指标**：tokens=2527 · llm_calls=2 · tool_steps=1 · 耗时=9.16s · 截断=否

---

**👤 用户**：随机数生成器用哪个类？

> 💭 **思考**：用户问的是 Godot 中随机数生成器用哪个类。这是个简单的回答问题，不需要 subagent，直接查即可。

我需要在 Godot core/ 代码库中搜索随机数相关的类。Godot 中常见的随机数生成器类是 `RandomNumberGenerator` 或者简称 `RandomPG`、`RefRandom` 等。

让我用 cmm_search 查一下。

**🔧 `cmm_search`**({"query": "随机数生成器 RandomNumberGenerator"})

> 💭 **思考**：找到了，是 `RandomNumberGenerator` 类。按照要求，我直接给出符号名即可，不要长解释。

**🤖 Agent**：`RandomNumberGenerator`

**📋 工具结果**：
```
- RandomNumberGenerator  (Users-ks_128-Documents-godot-src-core.math.random_number_generator.RandomNumberGenerator.RandomNumberGenerator)  math/random_number_generator.h
- randomize  (Users-ks_128-Documents-godot-src-core.math.random_number_generator.RandomNumberGenerator.randomize)  math/random_number_generator.h
- randi  (Users-ks_128-Documents-godot-src-core.math.random_number_generator.RandomNumberGenerator.randi)  math/random_number_generator.h
- randf  (Users-ks_128-Documents-godot-src-core.math.random_number_generator.RandomNumberGenerator.randf)  math/random_number_generator.h
- randfn
```


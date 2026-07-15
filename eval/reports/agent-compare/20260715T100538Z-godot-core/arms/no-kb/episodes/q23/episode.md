# q23 · code_retrieval · arm: `no-kb`

**题**：随机数生成器用哪个类？  ·  **gold**：RandomNumberGenerator
**答对**：✓  ·  **答案**：Godot 核心提供了两个层级的类：

- **`RandomNumberGenerator`**（`core/math/random_number_generator.h`）— 对外暴露给脚本的随机数生成器，推荐使用。
- **`Rand
**指标**：tokens=1113 · llm_calls=3 · tool_steps=2 · 耗时=16.34s · 截断=否

---

**👤 用户**：随机数生成器用哪个类？

> 💭 **思考**：用户问的是 Godot 核心代码库里随机数生成器用哪个类。让我搜索一下。

**🔧 `grep_code`**({"pattern": "class RandomNumberGenerator"})

**🔧 `grep_code`**({"pattern": "RandomPCG"})

> 💭 **思考**：两个类：
1. `RandomNumberGenerator` — 暴露给脚本的随机数生成器类
2. `RandomPCG` — 底层 PCG 随机数实现

让我直接回答。

**🤖 Agent**：Godot 核心提供了两个层级的类：

- **`RandomNumberGenerator`**（`core/math/random_number_generator.h`）— 对外暴露给脚本的随机数生成器，推荐使用。
- **`RandomPCG`**（`core/math/random_pcg.h`）— 底层 PCG 算法实现，`RandomNumberGenerator` 内部基于它。

**📋 工具结果**：
```
matched 1 files:
/Users/ks_128/Documents/godot-src/core/math/random_number_generator.h
```

**📋 工具结果**：
```
matched 6 files:
/Users/ks_128/Documents/godot-src/core/io/resource.cpp
/Users/ks_128/Documents/godot-src/core/io/resource_uid.cpp
/Users/ks_128/Documents/godot-src/core/math/random_pcg.cpp
/Users/ks_128/Documents/godot-src/core/math/math_funcs.cpp
/Users/ks_128/Documents/godot-src/core/math/random_number_generator.h
/Users/ks_128/Documents/godot-src/core/math/random_pcg.h
```


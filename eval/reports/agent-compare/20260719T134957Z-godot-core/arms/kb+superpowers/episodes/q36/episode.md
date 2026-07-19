# q36 · code_retrieval · arm: `kb+superpowers`

- **题**：Godot core 里用于动态场景的层次包围盒（bounding volume hierarchy，broadphase 加速结构）的类叫什么？
- **gold**：DynamicBVH
- **答对**：✓
- **答案**：`DynamicBVH`
- **指标**：tokens=2764 · llm_calls=2 · tool_steps=1 · 耗时=9.36s · 截断=否

---

**👤 用户**：Godot core 里用于动态场景的层次包围盒（bounding volume hierarchy，broadphase 加速结构）的类叫什么？

> 💭 **思考**：用户询问 Godot core 中用于动态场景的层次包围盒（bounding volume hierarchy，broadphase 加速结构）的类名。

这是一个关于代码库的定位问题。我需要使用 `mcp__bench__cmm_search` 工具来搜索相关的符号。

关键词可能是：
- BVH (Bounding Volume Hierarchy)
- broadphase
- dynamic scene
- bounding volume

让我先搜索 "BVH broadphase" 或 "bvh broadphase dynamic" 相关的内容。

**🔧 `cmm_search`**({"query": "BVH broadphase dynamic scene"})

> 💭 **思考**：搜索结果显示了 `DynamicBVH` 类，这正是用于动态场景的层次包围盒结构。该类在 `math/dynamic_bvh.cpp` 中实现，有析构函数、split、bounds、clear、insert等方法。

这正是用户询问的类名。根据指示，我应该直接用符号名作答，不要长解释。

**🤖 Agent**：`DynamicBVH`

**📋 工具结果**：
```
- ~DynamicBVH  (Users-ks_128-Documents-godot-src-core.math.dynamic_bvh.DynamicBVH.~DynamicBVH)  math/dynamic_bvh.cpp
- _split  (Users-ks_128-Documents-godot-src-core.math.dynamic_bvh.DynamicBVH._split)  math/dynamic_bvh.cpp
- _bounds  (Users-ks_128-Documents-godot-src-core.math.dynamic_bvh.DynamicBVH._bounds)  math/dynamic_bvh.cpp
- clear  (Users-ks_128-Documents-godot-src-core.math.dynamic_bvh.DynamicBVH.clear)  math/dynamic_bvh.cpp
- insert  (Users-ks_128-Documents-godot-src-core.math.dynamic_bvh.DynamicBVH.insert)  math/dynamic_bvh.cpp
```


# q36 · code_retrieval · arm: `kb+openspec`

- **题**：Godot core 里用于动态场景的层次包围盒（bounding volume hierarchy，broadphase 加速结构）的类叫什么？
- **gold**：DynamicBVH
- **答对**：✓
- **答案**：`DynamicBVH`
- **指标**：tokens=2593 · llm_calls=2 · tool_steps=1 · 耗时=8.32s · 截断=否

---

**👤 用户**：Godot core 里用于动态场景的层次包围盒（bounding volume hierarchy，broadphase 加速结构）的类叫什么？

> 💭 **思考**：用户在问 Godot core 里用于动态场景的层次包围盒（BVH, broadphase 加速结构）的类名。

这是一个代码定位问题，我需要在 Godot core/ 中搜索与 BVH（bounding volume hierarchy）、broadphase 相关的类。

让我先用语义搜索查找相关符号。

**🔧 `cmm_search`**({"query": "BVH bounding volume hierarchy broadphase dynamic scene"})

> 💭 **思考**：搜索结果直接找到了相关符号——DynamicBVH 类（math/dynamic_bvh.h 和 math/dynamic_bvh.cpp）。这应该是用户问的用于动态场景的层次包围盒（broadphase 加速结构）的类。

按照指令，我只需要用符号名直接作答，不要长解释。查到即答。

**🤖 Agent**：`DynamicBVH`

**📋 工具结果**：
```
- _create_node_with_volume  (Users-ks_128-Documents-godot-src-core.math.dynamic_bvh.DynamicBVH._create_node_with_volume)  math/dynamic_bvh.cpp
- contains  (Users-ks_128-Documents-godot-src-core.math.dynamic_bvh.DynamicBVH.Volume.contains)  math/dynamic_bvh.h
- merge  (Users-ks_128-Documents-godot-src-core.math.dynamic_bvh.DynamicBVH.Volume.merge)  math/dynamic_bvh.h
- intersects  (Users-ks_128-Documents-godot-src-core.math.dynamic_bvh.DynamicBVH.Volume.intersects)  math/dynamic_bvh.h
- get_center  (Users-ks_128-Documents-godot-src-core.math.dynamic_bvh.DynamicBVH.Volume.get_center)  math/dynam
```


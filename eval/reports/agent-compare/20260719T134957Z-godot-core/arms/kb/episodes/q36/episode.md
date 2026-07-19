# q36 · code_retrieval · arm: `kb`

- **题**：Godot core 里用于动态场景的层次包围盒（bounding volume hierarchy，broadphase 加速结构）的类叫什么？
- **gold**：DynamicBVH
- **答对**：✓
- **答案**：`DynamicBVH`
- **指标**：tokens=2043 · llm_calls=2 · tool_steps=1 · 耗时=7.79s · 截断=否

---

**👤 用户**：Godot core 里用于动态场景的层次包围盒（bounding volume hierarchy，broadphase 加速结构）的类叫什么？

> 💭 **思考**：用户在问 Godot core 里用于动态场景的层次包围盒（BVH，broadphase 加速结构）的类名。

这应该是一个关于空间划分、碰撞检测加速的数据结构。在游戏引擎中，BVH 通常用于物理碰撞检测的 broadphase 阶段。

让我搜索一下相关的类。

**🔧 `cmm_search`**({"query": "broadphase bounding volume hierarchy BVH dynamic scene"})

> 💭 **思考**：搜索结果返回了 DynamicBVH 相关的符号。看起来这就是用于动态场景的层次包围盒结构。从文件路径 `math/dynamic_bvh.cpp` 和 `math/dynamic_bvh.h` 可以确认这个类就是 `DynamicBVH`。

用户问的是类名，答案应该就是 `DynamicBVH`。

**🤖 Agent**：`DynamicBVH`

**📋 工具结果**：
```
- _create_node_with_volume  (Users-ks_128-Documents-godot-src-core.math.dynamic_bvh.DynamicBVH._create_node_with_volume)  math/dynamic_bvh.cpp
- contains  (Users-ks_128-Documents-godot-src-core.math.dynamic_bvh.DynamicBVH.Volume.contains)  math/dynamic_bvh.h
- merge  (Users-ks_128-Documents-godot-src-core.math.dynamic_bvh.DynamicBVH.Volume.merge)  math/dynamic_bvh.h
- intersects  (Users-ks_128-Documents-godot-src-core.math.dynamic_bvh.DynamicBVH.Volume.intersects)  math/dynamic_bvh.h
- get_center  (Users-ks_128-Documents-godot-src-core.math.dynamic_bvh.DynamicBVH.Volume.get_center)  math/dynam
```


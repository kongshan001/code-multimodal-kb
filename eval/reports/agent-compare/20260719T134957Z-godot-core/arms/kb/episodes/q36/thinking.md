# thinking

用户在问 Godot core 里用于动态场景的层次包围盒（BVH，broadphase 加速结构）的类名。

这应该是一个关于空间划分、碰撞检测加速的数据结构。在游戏引擎中，BVH 通常用于物理碰撞检测的 broadphase 阶段。

让我搜索一下相关的类。

---

搜索结果返回了 DynamicBVH 相关的符号。看起来这就是用于动态场景的层次包围盒结构。从文件路径 `math/dynamic_bvh.cpp` 和 `math/dynamic_bvh.h` 可以确认这个类就是 `DynamicBVH`。

用户问的是类名，答案应该就是 `DynamicBVH`。

---

`DynamicBVH`

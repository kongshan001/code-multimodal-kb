# thinking

用户在问 Godot core 里用于动态场景的层次包围盒（BVH, broadphase 加速结构）的类名。

这是一个代码定位问题，我需要在 Godot core/ 中搜索与 BVH（bounding volume hierarchy）、broadphase 相关的类。

让我先用语义搜索查找相关符号。

---

搜索结果直接找到了相关符号——DynamicBVH 类（math/dynamic_bvh.h 和 math/dynamic_bvh.cpp）。这应该是用户问的用于动态场景的层次包围盒（broadphase 加速结构）的类。

按照指令，我只需要用符号名直接作答，不要长解释。查到即答。

---

`DynamicBVH`

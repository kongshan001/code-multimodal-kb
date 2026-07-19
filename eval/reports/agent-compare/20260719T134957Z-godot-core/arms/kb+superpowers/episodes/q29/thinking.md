# thinking

用户问的是 Godot 中负责计算 A* 寻路路径的类。我需要在 Godot core/ 代码库中查找与 A* 寻路相关的类。

让我先搜索 A* 寻路相关的代码。

---

找到了！Godot 中负责 A* 寻路的是：
- `AStar2D` 类（2D 寻路）
- `AStar3D` 类（3D 寻路）

这些类在 `math/a_star.cpp` 和 `math/a_star.h` 中定义。

用户问的是"负责计算寻路路径的是哪个类"，应该直接给出这两个类的名称。

---

`AStar2D` / `AStar3D`

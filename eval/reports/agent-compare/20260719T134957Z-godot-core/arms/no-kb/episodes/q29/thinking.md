# thinking

用户问的是 Godot 中负责计算 A* 寻路路径的类。我需要在 Godot core/ 源码中查找相关的代码。

A* 寻路通常涉及的关键词：
- AStar
- A_star
- pathfinding
- navigation

让我先搜索 AStar 相关的类。

---

找到了 AStar 相关的类，让我查看这些头文件来确定具体的类名。

---

我需要看到更多内容来确定类名。让我再读取更多行来看到类定义。

---

让我用不同的方式搜索，直接找类名。

---

好的，所以 AStar2D 和 AStar3D 都在 a_star.h 中定义。让我再搜索 AStarGrid2D。

---

找到了。Godot 中负责计算 A* 寻路路径的类有：
- AStar2D
- AStar3D
- AStarGrid2D

根据用户的描述"两点间返回了错误路径，忽略了一个障碍物"，这更像是 AStarGrid2D 的问题，因为它处理网格上的障碍物。

我应该给出答案了。

---

`AStarGrid2D`（还有 `AStar2D` 和 `AStar3D`）

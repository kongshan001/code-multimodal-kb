# thinking

用户在问 A* 寻路算法用哪个类。这是在 Godot 代码库中的问题。我需要搜索与 A* 寻路相关的代码。

让我先搜索 A* 或 AStar 相关的模式。

---

找到了 AStar 相关的文件。看起来主要有两个类：
1. AStar (a_star.h/cpp)
2. AStarGrid2D (a_star_grid_2d.h/cpp)

让我看一下 a_star.h 文件来确认类名。

---

路径错误，应该是完整路径。让我使用完整路径。

---

文件内容只显示了头部注释，我需要继续读取后面的内容来看类定义。不过从文件名和grep结果来看，类名应该是 `AStar`。让我也看看另一个类。

---

从grep结果可以看到有两个主要的A*相关类：
1. AStar (在 a_star.h/cpp 中)
2. AStarGrid2D (在 a_star_grid_2d.h/cpp 中)

用户问"A* 寻路算法用哪个类"，答案是 `AStar` 和 `AStarGrid2D` 这两个类。根据收敛纪律，我应该立即用符号名作答。

---

`AStar`、`AStarGrid2D`

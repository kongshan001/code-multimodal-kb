# thinking

用户问"二维矩形用哪个类？"，这是在问 Godot 4.7 core/ 源码中用于表示二维矩形的类名。

在 Godot 中，二维矩形通常使用 `Rect2` 或 `Rect2i` 类。让我先 grep 一下确认。

我应该搜索 Rect2 相关的类定义。

---

没找到 `class Rect2`，让我试试直接搜索 `Rect2`。

---

找到了！有两个相关的文件：
- `/Users/ks_128/Documents/godot-src/core/math/rect2.h`
- `/Users/ks_128/Documents/godot-src/core/math/rect2i.h`

看起来 `Rect2` 和 `Rect2i` 是二维矩形类。让我读取其中一个确认。

---

文件太长，我需要看一点内容来确认类名。让我搜索 Rect2 类的定义行。

---

好的，根据搜索结果，我可以看到有两个二维矩形类：
- `Rect2` - 在 rect2.h/cpp 中定义
- `Rect2i` - 在 rect2i.h 中定义

在 Godot 中，`Rect2` 是浮点型的二维矩形类，`Rect2i` 是整数型的二维矩形类。

用户问的是"二维矩形用哪个类"，我应该直接回答类名。根据 Godot 的惯例，主要使用的是 `Rect2`（浮点版本），`Rect2i` 是其整数版本。

我应该简洁地回答这两个类名。

---

`Rect2`、`Rect2i`

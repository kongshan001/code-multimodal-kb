# agent-compare 结果 · target=godot-core · model=glm-5.1
> 29 题 × 1 runs × 4 臂。

## 怎么读懂这份报告（规则，先看）

**4 个臂是什么**：
- `no-kb` = 只给 grep + 读文件（朴素搜索，无知识库）
- `kb` = 给 cmm 代码知识库（语义检索符号）
- `kb+superpowers` / `kb+openspec` = kb + 往 agent 指令里注入 superpowers/openspec 的工程纪律 SOP
  （注入的是**精简 SOP 文本**，不是真 skill 运行时——见末尾诚实边界）

**答对（✓）怎么判**：终答里含 gold 符号或文件名就算对（broad 子串匹配，零 LLM judge）。
**gold 是什么**：每题的标准答案——来自 codegraph 挖出的真实代码符号/文件，构造即正确（不是人拍脑袋写的）。

**某题被标截断（逐题表 `截断` 列 ⚠ / `truncated_rate` > 0）**：agent 跑满步数上限（非 skills 臂 **8 轮**、skills 臂 **12 轮**）没自然收敛，系统**强制要了一个最佳答案**（不让它空着）——所以那题的答案是它的**猜测**，不一定对。多半发生在 no-kb（grep 找不到、烧满步数）。上限是控成本护栏，防无限调工具。

**`thinking` / 思考过程**：GLM-5.1 经这个端点不返独立 thinking block，所以思考 = agent 的推理文本（assistant 回答），不是单独的隐藏思维链——别当成完整思考链。
**`cost_$`**：token × 单价；单价是**占位**（待确认 GLM 定价），勿当真实成本，看相对大小即可。
**`tool_diversity` 高**：可能 agent 在乱试不同工具（没方向），未必好事。

## 谁赢
- **准确率最高**（2 臂并列）：`no-kb` / `kb+openspec`（accuracy=0.931）
- **最省 token**：`kb+superpowers`（mean_total_tokens=1015.1）
- **最省钱**：`no-kb`（mean_cost_$=0.0072）
- **KB vs 无 KB token 压缩**：1.07×（>1 = KB 省）

## 指标怎么看（小白版）
| 指标 | 大白话 |
|---|---|
| `accuracy` | 答对率 = 答对的题 ÷ 总题数。0~1，越高越好 |
| `mean_total_tokens` | 平均每题烧多少 token（≈字数）。越少越省 |
| `mean_llm_calls` | 平均每题调几次大模型。越少越快越省 |
| `mean_tool_steps` | 平均每题用几次工具（cmm/grep/read） |
| `mean_wall_clock_s` | 平均每题跑多久（秒） |
| `mean_cost_$` | 平均每题花多少钱（≈ token × 单价） |
| `tool_diversity` | 平均用了几种不同工具（高了可能在乱试） |
| `truncated_rate` | 多少题没在步数内答完（卡住了）。0 最好 |
| `context_compression` | 有 KB 比无 KB 省几倍 token（>1=KB 省；仅 no-kb+kb 都跑时给） |

## 对比矩阵
| 臂 | accuracy | mean_total_tokens | mean_llm_calls | mean_tool_steps | mean_wall_clock_s | mean_cost_$ | tool_diversity | truncated_rate | n_episodes |
|---|---|---|---|---|---|---|---|---|---|
| `no-kb` | 0.931 | 1163.7 | 2.76 | 1.76 | 16.21 | 0.0072 | 0.55 | 0.069 | 29 |
| `kb` | 0.862 | 1090.8 | 2.21 | 1.21 | 13.96 | 0.0084 | 0.76 | 0.0 | 29 |
| `kb+superpowers` | 0.897 | 1015.1 | 2.14 | 1.14 | 15.55 | 0.0089 | 0.83 | 0.0 | 29 |
| `kb+openspec` | 0.931 | 1542.3 | 2.76 | 1.76 | 19.43 | 0.012 | 1 | 0.0 | 29 |

## 逐题得分对照

> 每题各臂的答对 / 答案 / 指标（29 题 × 4 臂）。看哪题谁答对、谁省 token、谁卡住。

### q01 · code_retrieval
**题**：Godot 里字符串格式化的底层函数叫什么？  ·  **gold**：vformat

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | Godot 字符串格式化的底层函数是 **`String::sprintf`**（定义在 `co | 876 | 4 | 3 | 24.33 |  |
| `kb` | ✗ | Godot 字符串格式化的底层函数是：  **`String::format`**  定义在 ` | 1062 | 2 | 1 | 16.41 |  |
| `kb+superpowers` | ✗ | `String::format`，定义在 `core/string/ustring.cpp` 中 | 1374 | 2 | 1 | 17.2 |  |
| `kb+openspec` | ✗ | 底层函数是 `String::sprintf`（定义在 `core/string/ustring | 1335 | 2 | 1 | 20.68 |  |

### q02 · code_retrieval
**题**：整数转成字符串用哪个函数？  ·  **gold**：itos

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | `itos()`（integer to string），定义在 `ustring.h` / `u | 992 | 3 | 2 | 12.86 |  |
| `kb` | ✓ | `itos` — 定义于 `core/string/ustring.cpp`。 | 1025 | 2 | 1 | 8.82 |  |
| `kb+superpowers` | ✓ | 用 `itos()`（定义在 `core/string/ustring.cpp`），传入整数返回 | 1358 | 2 | 1 | 11.89 |  |
| `kb+openspec` | ✓ | 整数转字符串用 **`itos`**（位于 `string/ustring.cpp`）。 | 1607 | 3 | 2 | 20.77 |  |

### q03 · code_retrieval
**题**：删除对象、释放内存用哪个函数？  ·  **gold**：memdelete

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | `memdelete` — Godot core 的内存释放宏，与 `memnew` 配对，用于 | 1684 | 3 | 2 | 21.63 |  |
| `kb` | ✓ | - **`memdelete`** — 删除通过 `memnew` 创建的对象（最常用） - * | 377 | 2 | 1 | 12.63 |  |
| `kb+superpowers` | ✓ | Godot core 中释放内存/删除对象的主要函数：  / 用途 / 函数/符号 / 位置 / | 1574 | 2 | 1 | 16.63 |  |
| `kb+openspec` | ✓ | 在 Godot core 的 C++ 里，删除对象/释放内存主要用：  - **`memdele | 2147 | 4 | 3 | 20.66 |  |

### q04 · code_retrieval
**题**：A* 寻路算法用哪个类？  ·  **gold**：AStar

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | Godot 中的 A* 寻路算法使用以下类：  - **`AStar`** — 通用的 A* 寻 | 1090 | 2 | 1 | 24.57 |  |
| `kb` | ✓ | A* 寻路算法在 Godot core 中由 `AStar3D`（3D）实现，对应 2D 的变体 | 1062 | 2 | 1 | 13.41 |  |
| `kb+superpowers` | ✓ | A* 寻路算法用 **`AStar3D`**（3D）和 **`AStar2D`**（2D）。核心 | 1079 | 2 | 1 | 9.54 |  |
| `kb+openspec` | ✓ | `AStar3D`（3D）和对应的 `AStar2D`（2D）。核心实现位于 `core/mat | 1366 | 2 | 1 | 13.36 |  |

### q05 · code_retrieval
**题**：操作系统抽象层用哪个类？  ·  **gold**：OS

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | `OS`（定义于 `core/os/os.h`）。 | 884 | 2 | 1 | 9.82 |  |
| `kb` | ✓ | `OS`（定义于 `core/os/os.h` / `os.cpp`）  所有平台特定的功能（文 | 1052 | 2 | 1 | 10.97 |  |
| `kb+superpowers` | ✓ | 操作系统抽象层用 **`OS`** 类，定义在 `core/os/os.h`，是跨平台 OS 接 | 1439 | 2 | 1 | 8.75 |  |
| `kb+openspec` | ✓ | 操作系统抽象层用的是 **`OS`** 类（`core/os/os.h` / `os.cpp`） | 1320 | 2 | 1 | 12.27 |  |

### q06 · code_retrieval
**题**：表示颜色的类叫什么？  ·  **gold**：Color

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | `Color` | 759 | 1 | 0 | 6.95 |  |
| `kb` | ✓ | `Color`，定义在 `core/math/color.h`。 | 994 | 2 | 1 | 13.53 |  |
| `kb+superpowers` | ✓ | `Color`（定义在 `core/math/color.h`）。 | 1359 | 2 | 1 | 11.27 |  |
| `kb+openspec` | ✓ | `Color`（定义于 `core/math/color.h`）。 | 1296 | 2 | 1 | 13.99 |  |

### q07 · code_retrieval
**题**：二维向量用哪个类？  ·  **gold**：Vector2

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | `Vector2` | 747 | 1 | 0 | 5.93 |  |
| `kb` | ✓ | `Vector2` | 742 | 1 | 0 | 6.4 |  |
| `kb+superpowers` | ✓ | **`Vector2`** | 1078 | 1 | 0 | 6.23 |  |
| `kb+openspec` | ✓ | 二维向量用 `Vector2`（定义在 `math/vector2.h`）。 | 1588 | 3 | 2 | 15.46 |  |

### q08 · code_retrieval
**题**：三维向量用哪个类？  ·  **gold**：Vector3

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | `Vector3` | 739 | 1 | 0 | 8.0 |  |
| `kb` | ✓ | `Vector3` | 757 | 1 | 0 | 6.35 |  |
| `kb+superpowers` | ✓ | `Vector3` | 1072 | 1 | 0 | 8.74 |  |
| `kb+openspec` | ✓ | `Vector3` | 1020 | 1 | 0 | 6.13 |  |

### q09 · code_retrieval
**题**：四元数用哪个类？  ·  **gold**：Quaternion

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | **`Quaternion`**（头文件 `core/math/quaternion.h`）。 | 764 | 1 | 0 | 8.09 |  |
| `kb` | ✓ | 四元数用 **`Quaternion`** 类，定义在 `core/math/quaternio | 675 | 2 | 1 | 9.6 |  |
| `kb+superpowers` | ✓ | `Quaternion` | 61 | 1 | 0 | 6.17 |  |
| `kb+openspec` | ✓ | `Quaternion` | 1027 | 1 | 0 | 7.46 |  |

### q10 · code_retrieval
**题**：二维矩形用哪个类？  ·  **gold**：Rect2

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | `Rect2` | 747 | 1 | 0 | 7.76 |  |
| `kb` | ✓ | 二维矩形用 **`Rect2`**（浮点坐标）或 **`Rect2i`**（整数坐标），定义在  | 1368 | 3 | 2 | 13.24 |  |
| `kb+superpowers` | ✓ | `Rect2` | 43 | 1 | 0 | 6.0 |  |
| `kb+openspec` | ✓ | 二维矩形用 **`Rect2`** 类（定义在 `core/math/rect2.h`）。  它 | 1675 | 3 | 2 | 18.74 |  |

### q11 · code_retrieval
**题**：JSON 解析用哪个类？  ·  **gold**：JSON

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | `JSON`（定义在 `core/io/json.h`）。  用法示例： ```cpp JSON | 905 | 2 | 1 | 13.39 |  |
| `kb` | ✓ | `JSON` 类（`core/io/json.cpp`）。核心方法是 `JSON::parse( | 1007 | 2 | 1 | 16.54 |  |
| `kb+superpowers` | ✓ | `JSON`（定义在 `core/io/json.cpp`）。核心方法：  - **`JSON: | 1040 | 2 | 1 | 12.35 |  |
| `kb+openspec` | ✓ | 用 `JSON` 类（`core/io/json.cpp`），主要方法：  - `JSON.pa | 1301 | 2 | 1 | 13.55 |  |

### q12 · code_retrieval
**题**：图像数据用哪个类？  ·  **gold**：Image

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | `Image` | 45 | 1 | 0 | 4.13 |  |
| `kb` | ✓ | 图像数据用 **`Image`** 类（`core/io/image.cpp`）。  关键方法： | 1008 | 2 | 1 | 13.83 |  |
| `kb+superpowers` | ✓ | 图像数据用 **`Image`** 类（`core/io/image.cpp`）。常用方法如 ` | 1344 | 2 | 1 | 14.85 |  |
| `kb+openspec` | ✓ | 图像数据用 **`Image`** 类（`core/io/image.h`、`core/io/i | 1306 | 2 | 1 | 12.24 |  |

### q13 · code_retrieval
**题**：加载资源用哪个类？  ·  **gold**：ResourceLoader

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | `ResourceLoader` | 751 | 1 | 0 | 9.25 |  |
| `kb` | ✓ | `ResourceLoader` | 970 | 2 | 1 | 15.13 |  |
| `kb+superpowers` | ✓ | `ResourceLoader` | 316 | 2 | 1 | 15.64 |  |
| `kb+openspec` | ✓ | 加载资源用 `ResourceLoader`（类），通过其静态方法 `load()` 或内部 ` | 1340 | 2 | 1 | 21.28 |  |

### q14 · code_retrieval
**题**：保存资源用哪个类？  ·  **gold**：ResourceSaver

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | **`ResourceSaver`**（配合 `ResourceFormatSaver` 作为底 | 761 | 1 | 0 | 8.69 |  |
| `kb` | ✓ | 保存资源用 **`ResourceSaver`**（核心实现在 `core/io/resourc | 1341 | 3 | 2 | 18.16 |  |
| `kb+superpowers` | ✓ | 保存资源用 **`ResourceSaver`**（核心入口类），具体格式由 `Resource | 1368 | 2 | 1 | 13.21 |  |
| `kb+openspec` | ✓ | 保存资源用 **`ResourceSaver`**（核心方法 `ResourceSaver.sa | 1648 | 3 | 2 | 20.89 |  |

### q15 · code_retrieval
**题**：文件读写操作用哪个类？  ·  **gold**：FileAccess

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | 文件读写操作的核心类是 **`FileAccess`**（定义在 `core/io/file_a | 1117 | 2 | 1 | 16.14 |  |
| `kb` | ✓ | `FileAccess` | 743 | 1 | 0 | 7.18 |  |
| `kb+superpowers` | ✓ | 文件读写操作用 **`FileAccess`** 类，位于 `core/io/file_acce | 1392 | 2 | 1 | 33.67 |  |
| `kb+openspec` | ✓ | 文件读写操作用 **`FileAccess`** 类（位于 `core/io/file_acce | 1392 | 2 | 1 | 12.69 |  |

### q16 · code_retrieval
**题**：目录操作用哪个类？  ·  **gold**：DirAccess

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | `DirAccess` | 755 | 1 | 0 | 5.92 |  |
| `kb` | ✓ | `DirAccess`（定义于 `io/dir_access.cpp` / `io/dir_ac | 1378 | 3 | 2 | 23.33 |  |
| `kb+superpowers` | ✓ | **`DirAccess`**（`core/io/dir_access.h`）  常用操作： - | 1812 | 3 | 2 | 22.19 |  |
| `kb+openspec` | ✓ | `DirAccess`（`core/io/dir_access.h`），提供 `make_dir | 1600 | 3 | 2 | 17.91 |  |

### q17 · code_retrieval
**题**：消息队列用哪个类？  ·  **gold**：MessageQueue

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | `MessageQueue` | 947 | 2 | 1 | 24.53 |  |
| `kb` | ✓ | 用 `MessageQueue`（定义在 `core/object/message_queue. | 1071 | 2 | 1 | 16.28 |  |
| `kb+superpowers` | ✓ | `MessageQueue`（定义在 `core/object/message_queue.cp | 1334 | 2 | 1 | 13.79 |  |
| `kb+openspec` | ✓ | `MessageQueue`（单例），底层由 `CallQueue` 实现。位于 `core/o | 1312 | 2 | 1 | 12.12 |  |

### q18 · code_retrieval
**题**：引擎主类叫什么？  ·  **gold**：Engine

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | 引擎主类是 `Engine`。 | 759 | 1 | 0 | 7.46 |  |
| `kb` | ✗ | `Main` | 736 | 1 | 0 | 7.76 |  |
| `kb+superpowers` | ✓ | 引擎的主类是 **`Engine`**，定义在 `core_bind.cpp` / `core_ | 1537 | 2 | 1 | 17.0 |  |
| `kb+openspec` | ✓ | Godot 的引擎主类是 **`Engine`**（C++ 内为 `core_bind::Eng | 1489 | 2 | 1 | 18.24 |  |

### q19 · code_retrieval
**题**：主循环基类叫什么？  ·  **gold**：MainLoop

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | Godot 的主循环基类是 **`MainLoop`**，定义在 `core/os/main_l | 893 | 2 | 1 | 10.23 |  |
| `kb` | ✓ | 主循环基类叫 **`MainLoop`**，定义在 `os/main_loop.h`。 | 1019 | 2 | 1 | 15.49 |  |
| `kb+superpowers` | ✓ | **`MainLoop`**（定义在 `os/main_loop.h`）。 | 370 | 2 | 1 | 17.6 |  |
| `kb+openspec` | ✓ | `MainLoop`（定义在 `os/main_loop.h`）。 | 1313 | 2 | 1 | 19.63 |  |

### q20 · code_retrieval
**题**：撤销重做系统用哪个类？  ·  **gold**：UndoRedo

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | `UndoRedo`  Godot 中的撤销/重做系统由 **`UndoRedo`** 类实现（ | 811 | 1 | 0 | 8.65 |  |
| `kb` | ✓ | **`UndoRedo`**（定义于 `core/object/undo_redo.cpp`） | 1045 | 2 | 1 | 8.67 |  |
| `kb+superpowers` | ✓ | **`UndoRedo`**（`core/object/undo_redo.cpp`）  核心方 | 1421 | 2 | 1 | 14.12 |  |
| `kb+openspec` | ✓ | 撤销重做系统用的类是 **`UndoRedo`**（定义在 `core/object/undo_ | 1409 | 2 | 1 | 16.01 |  |

### q21 · code_retrieval
**题**：节点路径用哪个类？  ·  **gold**：NodePath

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | `NodePath` | 754 | 1 | 0 | 6.54 |  |
| `kb` | ✓ | `NodePath` | 750 | 1 | 0 | 6.18 |  |
| `kb+superpowers` | ✓ | `NodePath` | 57 | 1 | 0 | 7.79 |  |
| `kb+openspec` | ✓ | 节点路径用的是 **`NodePath`** 类，定义在 `core/string/node_p | 338 | 2 | 1 | 9.66 |  |

### q22 · code_retrieval
**题**：字符串名（优化版字符串）用哪个类？  ·  **gold**：StringName

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | `StringName` | 746 | 1 | 0 | 6.38 |  |
| `kb` | ✓ | `StringName` | 753 | 1 | 0 | 10.51 |  |
| `kb+superpowers` | ✓ | `StringName`  定义在 `core/string/string_name.h`，是一 | 432 | 2 | 1 | 14.53 |  |
| `kb+openspec` | ✓ | 用 **`StringName`**（定义在 `core/string/string_name. | 1380 | 2 | 1 | 18.08 |  |

### q23 · code_retrieval
**题**：随机数生成器用哪个类？  ·  **gold**：RandomNumberGenerator

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | Godot 核心提供了两个层级的类：  - **`RandomNumberGenerator`* | 1113 | 3 | 2 | 16.34 |  |
| `kb` | ✓ | 用 **`RandomNumberGenerator`**（定义在 `math/random_n | 1060 | 2 | 1 | 7.3 |  |
| `kb+superpowers` | ✓ | `RandomNumberGenerator`，定义在 `core/math/random_nu | 355 | 2 | 1 | 14.06 |  |
| `kb+openspec` | ✓ | `RandomNumberGenerator`（定义于 `math/random_number_ | 1339 | 2 | 1 | 9.35 |  |

### q24 · code_retrieval
**题**：加密解密用哪个类？  ·  **gold**：Crypto

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | 加密解密用 **`Crypto`** 类（定义于 `core/crypto/crypto.h`） | 1078 | 3 | 2 | 16.32 |  |
| `kb` | ✓ | `Crypto` 类（定义于 `core/crypto/crypto.cpp`），提供加密、解密 | 1014 | 2 | 1 | 11.35 |  |
| `kb+superpowers` | ✓ | 加密解密用 **`Crypto`** 类（`core/crypto/crypto.cpp`）。  | 349 | 2 | 1 | 15.43 |  |
| `kb+openspec` | ✓ | Godot 中加密解密主要用以下类（均在 `core/crypto/` 下）：  - **`Cr | 1569 | 3 | 2 | 26.11 |  |

### q25 · code_retrieval
**题**：翻译/本地化服务器用哪个类？  ·  **gold**：TranslationServer

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | `TranslationServer` | 756 | 1 | 0 | 6.09 |  |
| `kb` | ✓ | 翻译/本地化服务器用 **`TranslationServer`** 类，定义在 `core/s | 1014 | 2 | 1 | 12.5 |  |
| `kb+superpowers` | ✓ | **`TranslationServer`** | 54 | 1 | 0 | 3.25 |  |
| `kb+openspec` | ✓ | `TranslationServer`（定义于 `core/string/translation | 1342 | 2 | 1 | 28.45 |  |

### q26 · code_retrieval
**题**：HTTP 客户端用哪个类？  ·  **gold**：HTTPClient

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | `HTTPClient` | 741 | 1 | 0 | 6.97 |  |
| `kb` | ✓ | `HTTPClient` | 743 | 1 | 0 | 7.16 |  |
| `kb+superpowers` | ✓ | `HTTPClient`（低层，位于 `core/io/http_client.h`）。  如果 | 381 | 2 | 1 | 15.14 |  |
| `kb+openspec` | ✓ | `HTTPClient`（定义在 `io/http_client.h` / `io/http_c | 1301 | 2 | 1 | 18.78 |  |

### q27 · bug_fix
**题**：Object memory leak: an object is freed but a dangling reference is still held, causing a use-after-free. Where is the bug most likely fixed?  ·  **gold**：core/memory/memory.h, memdelete

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✗ | `RefCounted`（引用计数机制，`core/object/ref_counted.cpp | 3870 | 14 | 13 | 56.41 | ⚠卡住 |
| `kb` | ✗ | The use-after-free is most likely fixed by repla | 2446 | 5 | 4 | 36.58 |  |
| `kb+superpowers` | ✗ | The bug is most likely fixed by using **`Ref<T>` | 1002 | 3 | 2 | 27.76 |  |
| `kb+openspec` | ✗ | The bug is most likely fixed via the **predelete | 3398 | 9 | 8 | 82.39 |  |

### q28 · bug_fix
**题**：String formatting produces garbled output on a locale edge case. Which formatting routine is the culprit?  ·  **gold**：core/string/print_string.cpp, vformat

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✗ | `String::sprintf` | 5659 | 15 | 14 | 62.12 | ⚠卡住 |
| `kb` | ✗ | 罪魁祸首是 **`String::sprintf`**（`string/ustring.cpp` | 1355 | 3 | 2 | 18.38 |  |
| `kb+superpowers` | ✗ | 罪魁祸首是 **`String::sprintf`**（定义在 `core/string/ust | 3099 | 8 | 7 | 52.75 |  |
| `kb+openspec` | ✓ | 罪魁祸首是 **`String::sprintf`**（`string/ustring.cpp` | 3222 | 8 | 7 | 26.99 |  |

### q29 · bug_fix
**题**：Pathfinding returns a wrong path between two points, ignoring an obstacle. Which class computes the path?  ·  **gold**：AStar, core/math/a_star.h

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | In Godot's `core/`, path computation is handled  | 2005 | 8 | 7 | 54.54 |  |
| `kb` | ✓ | In Godot core, pathfinding between two points is | 3065 | 8 | 7 | 41.28 |  |
| `kb+superpowers` | ✓ | The path is computed by one of these A* pathfind | 1338 | 4 | 3 | 23.52 |  |
| `kb+openspec` | ✓ | Path computation lives in these core classes:  - | 2346 | 5 | 4 | 29.53 |  |

## 各臂速览
- `no-kb`: acc=0.931 · tokens=1163.7 · llm_calls=2.76 · steps=1.76 · t=16.21s · tools=0.55
- `kb`: acc=0.862 · tokens=1090.8 · llm_calls=2.21 · steps=1.21 · t=13.96s · tools=0.76
- `kb+superpowers`: acc=0.897 · tokens=1015.1 · llm_calls=2.14 · steps=1.14 · t=15.55s · tools=0.83
- `kb+openspec`: acc=0.931 · tokens=1542.3 · llm_calls=2.76 · steps=1.76 · t=19.43s · tools=1

## 诚实边界（必须看）
- **accuracy 由 GLM 生成 + GLM 判分**（同家族 self-preference）→ 相对参考值，非绝对回归值。
- **skills 臂注入的是 bundled 精简 SOP 文本**（`eval/arms/skills_bundled/`），**非完整 Claude Code skill 运行时**（无触发机制/hook）。是 headless 可复现近似，不等于真实 skill 效果。
- **`cost_$` 依赖 MODEL_PRICES 单价**，单价未知则 0（占位）；当前价格为占位，勿当真实成本。
- 样本量小（29 题），结论显著性有限——看趋势勿绝对化。
- bug_fix 题仍用 symbol/file broad match 判分（非修复质量 LLM-judge）。

## 怎么看 skills 值不值
对比 `kb+superpowers` / `kb+openspec` vs `kb` 的 accuracy（skills 帮没帮）+ mean_total_tokens（skills 多花多少）。**bug_fix 题上差异最可能显现**（纯 code_retrieval 上 skills 显不出价值）。

详见 `summary.json`（臂×指标矩阵，程序消费用）、各臂 `arms/<arm>/`（config + aggregate + episodes）。

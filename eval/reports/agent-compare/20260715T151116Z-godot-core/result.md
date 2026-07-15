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

**某题被标截断（逐题表 `截断` 列 ⚠ / `truncated_rate` > 0）**：agent 跑满 backstop（**30 轮**，防死循环的安全网）仍未自然给出答案 = **真卡住**。本跑采用 run-until-answer：**不 inject 猜测答案**，那题的 `answer` 是占位（判分即错）。30 轮 backstop 远超正常收敛所需，所以截断率衡量的是 agent 真正卡死的比例，不是被步数上限人为截断。

**`thinking` / 思考过程**：GLM-5.1 经这个端点不返独立 thinking block，所以思考 = agent 的推理文本（assistant 回答），不是单独的隐藏思维链——别当成完整思考链。
**`cost_$`**：token × 单价；单价是**占位**（待确认 GLM 定价），勿当真实成本，看相对大小即可。
**`tool_diversity` 高**：可能 agent 在乱试不同工具（没方向），未必好事。

## 谁赢
- **准确率最高**（2 臂并列）：`kb` / `kb+superpowers`（accuracy=0.966）
- **最省 token**：`kb+superpowers`（mean_total_tokens=679.5）
- **最省钱**：`kb+superpowers`（mean_cost_$=0.0068）
- **KB vs 无 KB token 压缩**：0.94×（>1 = KB 省）

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
| `no-kb` | 0.931 | 996.6 | 2.31 | 1.31 | 14.29 | 0.0075 | 0.62 | 0.0 | 29 |
| `kb` | 0.966 | 1061.7 | 2.03 | 1.03 | 12.39 | 0.0079 | 0.76 | 0.0 | 29 |
| `kb+superpowers` | 0.966 | 679.5 | 2.07 | 1.07 | 14.03 | 0.0068 | 0.69 | 0.0 | 29 |
| `kb+openspec` | 0.931 | 1359.7 | 2.17 | 1.17 | 13.52 | 0.0098 | 0.93 | 0.0 | 29 |

## 逐题得分对照

> 每题各臂的答对 / 答案 / 指标（29 题 × 4 臂）。看哪题谁答对、谁省 token、谁卡住。

### q01 · code_retrieval
**题**：Godot 里字符串格式化的底层函数叫什么？  ·  **gold**：vformat

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✗ | 底层格式化函数是 **`String::sprintf`**（位于 `core/string/u | 1500 | 6 | 5 | 50.55 |  |
| `kb` | ✗ | 字符串格式化的底层函数是 **`String::format`**，定义在 `core/stri | 1048 | 2 | 1 | 11.12 |  |
| `kb+superpowers` | ✗ | 底层格式化函数是 **`String::format`**（`core/string/ustri | 1369 | 2 | 1 | 12.45 |  |
| `kb+openspec` | ✗ | 底层有两个核心函数（定义在 `core/string/ustring.cpp`）：  - **` | 2401 | 2 | 1 | 10.8 |  |

### q02 · code_retrieval
**题**：整数转成字符串用哪个函数？  ·  **gold**：itos

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | 用 **`itos`**（定义在 `core/string/ustring.h` / `ustr | 1292 | 3 | 2 | 14.69 |  |
| `kb` | ✓ | 用 **`itos`**（定义在 `string/ustring.cpp`，`int` → `S | 1323 | 3 | 2 | 15.05 |  |
| `kb+superpowers` | ✓ | 用 **`itos()`**（int → String）。  定义在 `core/string/ | 1666 | 3 | 2 | 21.97 |  |
| `kb+openspec` | ✓ | 用 **`itos`**（定义在 `string/ustring.cpp`，将 int 转为 S | 1340 | 2 | 1 | 11.08 |  |

### q03 · code_retrieval
**题**：删除对象、释放内存用哪个函数？  ·  **gold**：memdelete

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | 删除对象、释放内存用以下函数：  - **`memdelete(T *p_class)`** — | 1673 | 5 | 4 | 24.38 |  |
| `kb` | ✓ | 在 Godot C++ 代码库中，删除对象/释放内存主要用以下函数（均在 `os/memory. | 1570 | 3 | 2 | 18.44 |  |
| `kb+superpowers` | ✓ | 在 Godot core 中，按层次：  / 函数 / 用途 / /---/---/ / **` | 1950 | 3 | 2 | 27.95 |  |
| `kb+openspec` | ✓ | 用 **`memdelete`**（定义在 `core/os/memory.h`）。  补充：  | 1434 | 2 | 1 | 15.23 |  |

### q04 · code_retrieval
**题**：A* 寻路算法用哪个类？  ·  **gold**：AStar

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | `AStar`（2D/3D 通用 A* 寻路）和 `AStarGrid2D`（专门用于 2D 网 | 807 | 1 | 0 | 6.18 |  |
| `kb` | ✓ | **`AStar`**（2D/3D 通用 A* 寻路）和 **`AStarGrid2D`**（专 | 785 | 1 | 0 | 9.55 |  |
| `kb+superpowers` | ✓ | 用 **`AStar3D`**（3D 寻路）和对应的 **`AStar2D`**（2D 寻路）， | 378 | 2 | 1 | 25.01 |  |
| `kb+openspec` | ✓ | Godot 中 A* 寻路用以下两个类：  - **`AStar3D`** — 3D 寻路，核心 | 1427 | 2 | 1 | 13.15 |  |

### q05 · code_retrieval
**题**：操作系统抽象层用哪个类？  ·  **gold**：OS

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | `OS`  定义在 `core/os/os.h`，是 Godot 的操作系统抽象层（单例），封装 | 922 | 2 | 1 | 10.13 |  |
| `kb` | ✓ | 操作系统抽象层用 **`OS`** 类（定义在 `core/os/os.cpp` / `os.h | 988 | 2 | 1 | 12.66 |  |
| `kb+superpowers` | ✓ | 操作系统抽象层的核心类是 **`OS`**（定义于 `os/os.h` / `os/os.cpp | 413 | 2 | 1 | 12.62 |  |
| `kb+openspec` | ✓ | 操作系统抽象层用的是 **`OS`** 类（定义于 `core/os/os.h` / `core | 1377 | 2 | 1 | 7.19 |  |

### q06 · code_retrieval
**题**：表示颜色的类叫什么？  ·  **gold**：Color

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | 表示颜色的类叫 **`Color`**，定义在 `core/math/color.h`。 | 1868 | 6 | 5 | 39.43 |  |
| `kb` | ✓ | `Color`（定义在 `math/color.h`）。 | 979 | 2 | 1 | 12.01 |  |
| `kb+superpowers` | ✓ | **`Color`** | 32 | 1 | 0 | 9.53 |  |
| `kb+openspec` | ✓ | `Color`（定义在 `core/math/color.h`）。 | 1281 | 2 | 1 | 15.49 |  |

### q07 · code_retrieval
**题**：二维向量用哪个类？  ·  **gold**：Vector2

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | `Vector2` | 741 | 1 | 0 | 9.67 |  |
| `kb` | ✓ | `Vector2` | 746 | 1 | 0 | 9.17 |  |
| `kb+superpowers` | ✓ | `Vector2` | 1104 | 1 | 0 | 8.34 |  |
| `kb+openspec` | ✓ | `Vector2` | 1038 | 1 | 0 | 6.19 |  |

### q08 · code_retrieval
**题**：三维向量用哪个类？  ·  **gold**：Vector3

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | `Vector3` | 747 | 1 | 0 | 12.57 |  |
| `kb` | ✓ | 用 `Vector3`（定义于 `math/vector3.h`）。 | 997 | 2 | 1 | 8.7 |  |
| `kb+superpowers` | ✓ | 用 **`Vector3`**（`math/vector3.h`）。 | 580 | 3 | 2 | 16.04 |  |
| `kb+openspec` | ✓ | 三维向量用 **`Vector3`**（`core/math/vector3.h`）。  注：还 | 896 | 4 | 3 | 20.91 |  |

### q09 · code_retrieval
**题**：四元数用哪个类？  ·  **gold**：Quaternion

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | **`Quaternion`**（`core/math/quaternion.h`） | 761 | 1 | 0 | 9.07 |  |
| `kb` | ✓ | `Quaternion` | 749 | 1 | 0 | 6.56 |  |
| `kb+superpowers` | ✓ | `Quaternion` | 40 | 1 | 0 | 6.75 |  |
| `kb+openspec` | ✓ | `Quaternion` | 1012 | 1 | 0 | 5.41 |  |

### q10 · code_retrieval
**题**：二维矩形用哪个类？  ·  **gold**：Rect2

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | `Rect2` | 740 | 1 | 0 | 7.16 |  |
| `kb` | ✓ | `Rect2`（定义在 `core/math/rect2.h`），轴对齐二维矩形，由 `posi | 1664 | 5 | 4 | 30.2 |  |
| `kb+superpowers` | ✓ | `Rect2` | 1070 | 1 | 0 | 6.72 |  |
| `kb+openspec` | ✓ | `Rect2`（`core/math/rect2.h`）。  常用方法：`intersects` | 1333 | 2 | 1 | 16.69 |  |

### q11 · code_retrieval
**题**：JSON 解析用哪个类？  ·  **gold**：JSON

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | `JSON`（定义在 `core/io/json.h`）。 | 876 | 2 | 1 | 16.55 |  |
| `kb` | ✓ | `JSON` | 739 | 1 | 0 | 6.71 |  |
| `kb+superpowers` | ✓ | `JSON` 类（核心方法：`JSON::parse`，定义在 `core/io/json.cp | 339 | 2 | 1 | 13.96 |  |
| `kb+openspec` | ✓ | JSON 解析用 `JSON` 类（`core/io/json.cpp`），核心方法：  - * | 1345 | 2 | 1 | 16.07 |  |

### q12 · code_retrieval
**题**：图像数据用哪个类？  ·  **gold**：Image

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | `Image`（定义在 `core/io/image.h`）。 | 876 | 2 | 1 | 12.96 |  |
| `kb` | ✓ | `Image`（`io/image.cpp`），核心方法包括 `set_data` / `get | 994 | 2 | 1 | 13.13 |  |
| `kb+superpowers` | ✓ | `Image`（core/io/image.h, image.cpp）。图像数据就存在 `Ima | 300 | 2 | 1 | 15.0 |  |
| `kb+openspec` | ✓ | 图像数据用 **`Image`** 类（`core/io/image.h`）。 | 1277 | 2 | 1 | 8.55 |  |

### q13 · code_retrieval
**题**：加载资源用哪个类？  ·  **gold**：ResourceLoader

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | `ResourceLoader` | 744 | 1 | 0 | 5.22 |  |
| `kb` | ✓ | `ResourceLoader` | 747 | 1 | 0 | 6.64 |  |
| `kb+superpowers` | ✓ | `ResourceLoader` | 286 | 2 | 1 | 8.09 |  |
| `kb+openspec` | ✓ | 加载资源用 **`ResourceLoader`**（核心类，位于 `core/io/resou | 1377 | 2 | 1 | 15.43 |  |

### q14 · code_retrieval
**题**：保存资源用哪个类？  ·  **gold**：ResourceSaver

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | `ResourceSaver` | 1031 | 3 | 2 | 19.61 |  |
| `kb` | ✓ | `ResourceSaver` | 977 | 2 | 1 | 9.75 |  |
| `kb+superpowers` | ✓ | `ResourceSaver`（core_bind 版 / 静态 API 版）。核心方法是 `R | 628 | 3 | 2 | 13.07 |  |
| `kb+openspec` | ✓ | 用 **`ResourceSaver`**，核心方法是 `ResourceSaver::save | 1656 | 3 | 2 | 17.28 |  |

### q15 · code_retrieval
**题**：文件读写操作用哪个类？  ·  **gold**：FileAccess

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | `FileAccess` | 741 | 1 | 0 | 6.59 |  |
| `kb` | ✓ | **`FileAccess`**  Godot 核心的文件读写操作统一通过 `FileAcces | 1145 | 2 | 1 | 14.79 |  |
| `kb+superpowers` | ✓ | `FileAccess` | 1073 | 1 | 0 | 5.98 |  |
| `kb+openspec` | ✓ | `FileAccess`  定义在 `core/io/file_access.h`，是 Godo | 1397 | 2 | 1 | 11.02 |  |

### q16 · code_retrieval
**题**：目录操作用哪个类？  ·  **gold**：DirAccess

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | `DirAccess` | 750 | 1 | 0 | 9.33 |  |
| `kb` | ✓ | `DirAccess` | 740 | 1 | 0 | 8.08 |  |
| `kb+superpowers` | ✓ | `DirAccess`（定义在 `io/dir_access.h` / `io/dir_acce | 624 | 3 | 2 | 12.67 |  |
| `kb+openspec` | ✓ | 目录操作用 **`DirAccess`** 类（定义于 `core/io/dir_access. | 1745 | 3 | 2 | 12.46 |  |

### q17 · code_retrieval
**题**：消息队列用哪个类？  ·  **gold**：MessageQueue

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | `MessageQueue`（定义在 `core/object/message_queue.h` | 848 | 2 | 1 | 8.59 |  |
| `kb` | ✓ | 消息队列用的是 **`MessageQueue`**（定义于 `core/object/mess | 1019 | 2 | 1 | 12.86 |  |
| `kb+superpowers` | ✓ | `MessageQueue`（定义于 `core/object/message_queue.cp | 316 | 2 | 1 | 12.28 |  |
| `kb+openspec` | ✓ | `MessageQueue`（`core/object/message_queue.cpp`）。 | 977 | 2 | 1 | 21.02 |  |

### q18 · code_retrieval
**题**：引擎主类叫什么？  ·  **gold**：Engine

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | 引擎主类是 **`Engine`**，定义在 `core/config/engine.h`。 | 929 | 2 | 1 | 8.64 |  |
| `kb` | ✓ | 引擎主类是 **`Engine`**（C++ 实现为 `core_bind::Engine`，定 | 1221 | 2 | 1 | 20.46 |  |
| `kb+superpowers` | ✓ | 引擎主类是 **`core_bind::Engine`**（绑定到 GDScript 中的 `E | 370 | 2 | 1 | 8.96 |  |
| `kb+openspec` | ✓ | 引擎主类是 **`Engine`**，定义在 `core/core_bind.h`，属于 `co | 1600 | 3 | 2 | 14.98 |  |

### q19 · code_retrieval
**题**：主循环基类叫什么？  ·  **gold**：MainLoop

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | `MainLoop` | 748 | 1 | 0 | 7.39 |  |
| `kb` | ✓ | 主循环基类叫 **`MainLoop`**（定义在 `os/main_loop.h`）。 | 1027 | 2 | 1 | 12.2 |  |
| `kb+superpowers` | ✓ | `MainLoop`  Godot 的主循环抽象基类是 `MainLoop`（继承自 `Obje | 1124 | 1 | 0 | 5.19 |  |
| `kb+openspec` | ✓ | 主循环基类是 **`MainLoop`**，定义在 `os/main_loop.h`。 | 1315 | 2 | 1 | 12.79 |  |

### q20 · code_retrieval
**题**：撤销重做系统用哪个类？  ·  **gold**：UndoRedo

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | `UndoRedo` | 753 | 1 | 0 | 8.84 |  |
| `kb` | ✓ | `UndoRedo`（定义在 `core/object/undo_redo.cpp`）。  核心 | 1079 | 2 | 1 | 8.71 |  |
| `kb+superpowers` | ✓ | 撤销重做系统用 `UndoRedo` 类（`core/object/undo_redo.h` / | 402 | 2 | 1 | 15.01 |  |
| `kb+openspec` | ✓ | `UndoRedo`（`core/object/undo_redo.cpp`） | 1319 | 2 | 1 | 7.44 |  |

### q21 · code_retrieval
**题**：节点路径用哪个类？  ·  **gold**：NodePath

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | `NodePath` | 751 | 1 | 0 | 7.43 |  |
| `kb` | ✓ | `NodePath` | 754 | 1 | 0 | 9.14 |  |
| `kb+superpowers` | ✓ | `NodePath` | 56 | 1 | 0 | 6.9 |  |
| `kb+openspec` | ✓ | `NodePath`  定义在 `core/string/node_path.h` / `nod | 970 | 2 | 1 | 8.36 |  |

### q22 · code_retrieval
**题**：字符串名（优化版字符串）用哪个类？  ·  **gold**：StringName

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | `StringName` | 756 | 1 | 0 | 8.09 |  |
| `kb` | ✓ | `StringName` | 760 | 1 | 0 | 6.73 |  |
| `kb+superpowers` | ✓ | `StringName` | 55 | 1 | 0 | 7.69 |  |
| `kb+openspec` | ✓ | `StringName`（定义在 `core/string/string_name.h`）。它是 | 1390 | 2 | 1 | 17.09 |  |

### q23 · code_retrieval
**题**：随机数生成器用哪个类？  ·  **gold**：RandomNumberGenerator

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | `RandomNumberGenerator`，定义在 `core/math/random_nu | 161 | 2 | 1 | 13.79 |  |
| `kb` | ✓ | 用 `RandomNumberGenerator`，定义在 `math/random_numbe | 1024 | 2 | 1 | 10.07 |  |
| `kb+superpowers` | ✓ | `RandomNumberGenerator` | 44 | 1 | 0 | 6.66 |  |
| `kb+openspec` | ✓ | `RandomNumberGenerator`（定义在 `math/random_number_ | 1367 | 2 | 1 | 9.61 |  |

### q24 · code_retrieval
**题**：加密解密用哪个类？  ·  **gold**：Crypto

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | 主要用 **`Crypto`**（`core/crypto/crypto.h`）。  相关辅助类 | 1270 | 2 | 1 | 13.51 |  |
| `kb` | ✓ | `Crypto`（位于 `core/crypto/crypto.cpp`）。  主要方法： -  | 1076 | 2 | 1 | 12.39 |  |
| `kb+superpowers` | ✓ | Godot 的加密解密涉及以下核心类（`core/crypto/` 下）：  / 用途 / 类/ | 943 | 4 | 3 | 29.12 |  |
| `kb+openspec` | ✓ | `Crypto` 类（`core/crypto/crypto.cpp`），相关方法有 `crea | 1351 | 2 | 1 | 15.04 |  |

### q25 · code_retrieval
**题**：翻译/本地化服务器用哪个类？  ·  **gold**：TranslationServer

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | `TranslationServer` | 747 | 1 | 0 | 6.48 |  |
| `kb` | ✓ | `TranslationServer` | 742 | 1 | 0 | 6.72 |  |
| `kb+superpowers` | ✓ | `TranslationServer`（位于 `core/string/translation_ | 321 | 2 | 1 | 9.64 |  |
| `kb+openspec` | ✓ | `TranslationServer`（位于 `core/string/translation_ | 1303 | 2 | 1 | 19.04 |  |

### q26 · code_retrieval
**题**：HTTP 客户端用哪个类？  ·  **gold**：HTTPClient

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | `HTTPClient` | 757 | 1 | 0 | 7.81 |  |
| `kb` | ✓ | `HTTPClient`（定义在 `io/http_client.h`），底层 TCP 实现为  | 1048 | 2 | 1 | 15.39 |  |
| `kb+superpowers` | ✓ | `HTTPClient`（底层）或 `HTTPRequest`（节点级便捷封装）。 | 63 | 1 | 0 | 12.08 |  |
| `kb+openspec` | ✓ | 用 **`HTTPClient`**（`io/http_client.h`）。  其底层 TCP | 392 | 2 | 1 | 7.61 |  |

### q27 · bug_fix
**题**：对象内存泄漏：某对象被释放后仍被引用（use-after-free）。Godot 里删除/释放对象的底层函数叫什么？  ·  **gold**：core/memory/memory.h, memdelete

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | Godot 中删除/释放对象的底层函数主要有：  - **`memdelete(ptr)`**  | 1873 | 4 | 3 | 26.7 |  |
| `kb` | ✓ | Godot 里删除/释放对象涉及的核心函数：  - **`Object::free()`** — | 2122 | 6 | 5 | 24.68 |  |
| `kb+superpowers` | ✓ | Godot 中删除/释放对象的底层函数是：  - **`Object::free()`** —  | 1760 | 7 | 6 | 33.96 |  |
| `kb+openspec` | ✓ | Godot 中删除/释放对象的底层核心函数和机制：  **面向对象层（Script/GDScri | 2162 | 4 | 3 | 29.82 |  |

### q28 · bug_fix
**题**：字符串格式化在某些 locale 边界情况下输出乱码，疑是底层格式化例程的 bug。Godot 里字符串格式化的底层函数叫什么？  ·  **gold**：core/string/print_string.cpp, vformat

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✗ | Godot 字符串格式化的底层函数有两个：  - **`String::format(const | 2169 | 10 | 9 | 33.27 |  |
| `kb` | ✓ | Godot 字符串格式化的底层例程是 **`String::sprintf`**（定义于 `co | 1415 | 3 | 2 | 17.96 |  |
| `kb+superpowers` | ✓ | Godot 字符串格式化的底层例程主要有两个：  - **`String::sprintf`** | 1688 | 2 | 1 | 20.36 |  |
| `kb+openspec` | ✗ | Godot 字符串格式化的底层函数是 `String::format`，位于 `core/str | 1354 | 2 | 1 | 9.45 |  |

### q29 · bug_fix
**题**：A* 寻路在两点间返回了错误路径，忽略了一个障碍物。Godot 里负责计算寻路路径的是哪个类？  ·  **gold**：AStar, core/math/a_star.h

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | 负责 A* 寻路计算的类是：  - **`AStar`** — 定义在 `core/math/a | 1071 | 2 | 1 | 9.7 |  |
| `kb` | ✓ | Godot 中负责 A* 寻路路径计算的有三个类（均在 `core/math/`）：  - ** | 1312 | 2 | 1 | 9.47 |  |
| `kb+superpowers` | ✓ | Godot 中负责 A* 寻路路径计算的类有：  - **`AStar3D`** — 3D 空间 | 712 | 2 | 1 | 22.98 |  |
| `kb+openspec` | ✓ | Godot 中负责 A* 寻路路径计算的类是 **`AStar3D`**（位于 `core/ma | 1595 | 2 | 1 | 17.02 |  |

## 各臂速览
- `no-kb`: acc=0.931 · tokens=996.6 · llm_calls=2.31 · steps=1.31 · t=14.29s · tools=0.62
- `kb`: acc=0.966 · tokens=1061.7 · llm_calls=2.03 · steps=1.03 · t=12.39s · tools=0.76
- `kb+superpowers`: acc=0.966 · tokens=679.5 · llm_calls=2.07 · steps=1.07 · t=14.03s · tools=0.69
- `kb+openspec`: acc=0.931 · tokens=1359.7 · llm_calls=2.17 · steps=1.17 · t=13.52s · tools=0.93

## 诚实边界（必须看）
- **accuracy 由 GLM 生成 + GLM 判分**（同家族 self-preference）→ 相对参考值，非绝对回归值。
- **skills 臂注入的是 bundled 精简 SOP 文本**（`eval/arms/skills_bundled/`），**非完整 Claude Code skill 运行时**（无触发机制/hook）。是 headless 可复现近似，不等于真实 skill 效果。
- **`cost_$` 依赖 MODEL_PRICES 单价**，单价未知则 0（占位）；当前价格为占位，勿当真实成本。
- 样本量小（29 题），结论显著性有限——看趋势勿绝对化。
- bug_fix 题仍用 symbol/file broad match 判分（非修复质量 LLM-judge）。

## 怎么看 skills 值不值
对比 `kb+superpowers` / `kb+openspec` vs `kb` 的 accuracy（skills 帮没帮）+ mean_total_tokens（skills 多花多少）。**bug_fix 题上差异最可能显现**（纯 code_retrieval 上 skills 显不出价值）。

详见 `summary.json`（臂×指标矩阵，程序消费用）、各臂 `arms/<arm>/`（config + aggregate + episodes）。

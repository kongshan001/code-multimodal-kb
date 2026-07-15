# agent-compare 结果 · target=godot-core · model=glm-5.1 · engine=raw
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
- **准确率最高**（3 臂并列）：`no-kb` / `kb` / `kb+openspec`（accuracy=0.966）
- **最省 token**：`kb`（mean_total_tokens=830.7）
- **最省钱**（2 臂并列）：`no-kb` / `kb`（mean_cost_$=0.0006）
- **KB vs 无 KB token 压缩**：1.14×（>1 = KB 省）

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
| `no-kb` | 0.966 | 944.9 | 1.86 | 1.17 | 9.18 | 0.0006 | 0.48 | 0.0 | 29 |
| `kb` | 0.966 | 830.7 | 1.9 | 0.97 | 15.38 | 0.0006 | 0.76 | 0.0 | 29 |
| `kb+superpowers` | 0.931 | 1433 | 2 | 1.03 | 9.86 | 0.001 | 0.76 | 0.0 | 29 |
| `kb+openspec` | 0.966 | 1397.7 | 2.14 | 1.17 | 10.56 | 0.001 | 0.66 | 0.0 | 29 |

## 逐题得分对照

> 每题各臂的答对 / 答案 / 指标（29 题 × 4 臂）。看哪题谁答对、谁省 token、谁卡住。

### q01 · code_retrieval
**题**：Godot 里字符串格式化的底层函数叫什么？  ·  **gold**：vformat

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✗ | Godot 字符串格式化的底层函数主要有两个，都在 `String` 类（`core/strin | 5220 | 9 | 12 | 43.33 |  |
| `kb` | ✗ | 底层字符串格式化函数是 `String::format`，定义在 `core/string/us | 929 | 2 | 1 | 7.14 |  |
| `kb+superpowers` | ✗ | 底层函数是 `String::format`，定义在 `core/string/ustring. | 1588 | 2 | 1 | 7.16 |  |
| `kb+openspec` | ✗ | 字符串格式化的底层函数是 `String::format`，定义在 `core/string/u | 1487 | 2 | 1 | 8.9 |  |

### q02 · code_retrieval
**题**：整数转成字符串用哪个函数？  ·  **gold**：itos

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | 在 Godot core 中，整数转字符串常用的函数：  - **`String::num()` | 442 | 1 | 0 | 10.75 |  |
| `kb` | ✓ | 使用 **`itos()`** 函数（定义在 `string/ustring.cpp`），将整数 | 1676 | 3 | 2 | 14.7 |  |
| `kb+superpowers` | ✓ | 用 **`itos()`**，定义在 `string/ustring.cpp`。它接受一个整数参 | 1821 | 3 | 2 | 11.23 |  |
| `kb+openspec` | ✓ | 用 **`itos()`**，定义在 `core/string/ustring.cpp`。它将  | 2198 | 3 | 2 | 17.46 |  |

### q03 · code_retrieval
**题**：删除对象、释放内存用哪个函数？  ·  **gold**：memdelete

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | 在 Godot 中，删除对象/释放内存主要使用以下函数：  - **`memdelete()`* | 467 | 1 | 0 | 4.45 |  |
| `kb` | ✓ | 在 Godot core 中，删除对象/释放内存主要用以下函数（定义于 `os/memory.h | 1220 | 2 | 2 | 10.34 |  |
| `kb+superpowers` | ✓ | 在 Godot core 中，删除对象/释放内存主要用以下函数：  / 场景 / 函数 / 说明 | 2755 | 3 | 2 | 14.68 |  |
| `kb+openspec` | ✓ | ## Godot C++ 中删除对象/释放内存  取决于对象类型：  ### 1. 手动 `me | 830 | 1 | 0 | 9.57 |  |

### q04 · code_retrieval
**题**：A* 寻路算法用哪个类？  ·  **gold**：AStar

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | `AStar`（2D 网格寻路）和 `AStar3D`（3D 寻路），以及 `AStarGrid | 389 | 1 | 0 | 5.01 |  |
| `kb` | ✓ | A* 寻路算法使用 `AStar3D` 类（3D），对应的还有 `AStar2D` 类（2D）。 | 965 | 2 | 1 | 176.81 |  |
| `kb+superpowers` | ✓ | A* 寻路算法使用 `AStar3D` 类（3D）和 `AStar2D` 类（2D），核心求解逻 | 1306 | 2 | 1 | 7.77 |  |
| `kb+openspec` | ✓ | `AStar`（2D）和 `AStar3D`（3D），以及 `AStarGrid2D`（网格专用 | 661 | 1 | 0 | 3.66 |  |

### q05 · code_retrieval
**题**：操作系统抽象层用哪个类？  ·  **gold**：OS

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | `OS`（定义在 `core/os/os.h`）。 | 757 | 2 | 1 | 6.17 |  |
| `kb` | ✓ | 操作系统抽象层使用的是 **`OS`** 类（定义在 `core/os/os.h` / `cor | 673 | 2 | 1 | 15.6 |  |
| `kb+superpowers` | ✓ | 操作系统抽象层使用的是 **`OS`** 类（定义在 `core/os/os.h` / `cor | 1325 | 2 | 1 | 11.66 |  |
| `kb+openspec` | ✓ | 操作系统抽象层使用的是 **`OS`** 类（定义在 `core/os/os.h` / `cor | 1596 | 2 | 1 | 10.24 |  |

### q06 · code_retrieval
**题**：表示颜色的类叫什么？  ·  **gold**：Color

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | `Color` | 343 | 1 | 0 | 4.1 |  |
| `kb` | ✓ | 表示颜色的类叫 `Color`，定义在 `math/color.h` 中。 | 891 | 2 | 1 | 8.8 |  |
| `kb+superpowers` | ✓ | `Color` | 678 | 1 | 0 | 6.33 |  |
| `kb+openspec` | ✓ | `Color` | 626 | 1 | 0 | 5.0 |  |

### q07 · code_retrieval
**题**：二维向量用哪个类？  ·  **gold**：Vector2

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | `Vector2` | 344 | 1 | 0 | 7.85 |  |
| `kb` | ✓ | `Vector2` | 348 | 1 | 0 | 3.13 |  |
| `kb+superpowers` | ✓ | `Vector2` | 679 | 1 | 0 | 5.81 |  |
| `kb+openspec` | ✓ | `Vector2` | 627 | 1 | 0 | 3.72 |  |

### q08 · code_retrieval
**题**：三维向量用哪个类？  ·  **gold**：Vector3

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | `Vector3` | 24 | 1 | 0 | 3.23 |  |
| `kb` | ✓ | `Vector3` | 348 | 1 | 0 | 2.5 |  |
| `kb+superpowers` | ✓ | `Vector3` | 679 | 1 | 0 | 8.76 |  |
| `kb+openspec` | ✓ | `Vector3` | 627 | 1 | 0 | 5.29 |  |

### q09 · code_retrieval
**题**：四元数用哪个类？  ·  **gold**：Quaternion

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | `Quaternion` | 344 | 1 | 0 | 3.0 |  |
| `kb` | ✓ | `Quaternion` | 348 | 1 | 0 | 3.66 |  |
| `kb+superpowers` | ✓ | `Quaternion` | 679 | 1 | 0 | 3.31 |  |
| `kb+openspec` | ✓ | `Quaternion` | 627 | 1 | 0 | 7.56 |  |

### q10 · code_retrieval
**题**：二维矩形用哪个类？  ·  **gold**：Rect2

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | `Rect2` | 344 | 1 | 0 | 4.7 |  |
| `kb` | ✓ | `Rect2` | 348 | 1 | 0 | 2.86 |  |
| `kb+superpowers` | ✓ | 二维矩形用 **`Rect2`**（浮点坐标），定义在 `core/math/rect2.h`。 | 2741 | 3 | 2 | 14.9 |  |
| `kb+openspec` | ✓ | `Rect2` | 627 | 1 | 0 | 4.91 |  |

### q11 · code_retrieval
**题**：JSON 解析用哪个类？  ·  **gold**：JSON

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | `JSON` | 344 | 1 | 0 | 4.51 |  |
| `kb` | ✓ | JSON 解析使用 **`JSON`** 类（`core/io/json.cpp`），主要方法： | 919 | 2 | 1 | 7.85 |  |
| `kb+superpowers` | ✓ | `JSON` 类（定义在 `core/io/json.cpp`），核心方法：  - **`JSO | 1580 | 2 | 1 | 12.08 |  |
| `kb+openspec` | ✓ | JSON 解析使用 **`JSON`** 类（定义在 `core/io/json.cpp`），核 | 1482 | 2 | 1 | 7.96 |  |

### q12 · code_retrieval
**题**：图像数据用哪个类？  ·  **gold**：Image

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | `Image` | 343 | 1 | 0 | 3.48 |  |
| `kb` | ✓ | 图像数据使用 `Image` 类（定义在 `core/io/image.cpp` / `imag | 904 | 2 | 1 | 6.85 |  |
| `kb+superpowers` | ✓ | 图像数据用 **`Image`** 类（`core/io/image.cpp`）。相关方法包括  | 1570 | 2 | 1 | 7.89 |  |
| `kb+openspec` | ✓ | 图像数据使用 `Image` 类（`core/io/image.cpp`）。相关方法包括 `Im | 1470 | 2 | 1 | 14.22 |  |

### q13 · code_retrieval
**题**：加载资源用哪个类？  ·  **gold**：ResourceLoader

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | `ResourceLoader` | 344 | 1 | 0 | 3.2 |  |
| `kb` | ✓ | 加载资源使用 **`ResourceLoader`** 类（核心静态方法 `ResourceLo | 605 | 2 | 1 | 11.7 |  |
| `kb+superpowers` | ✓ | `ResourceLoader` | 679 | 1 | 0 | 4.64 |  |
| `kb+openspec` | ✓ | `ResourceLoader` | 627 | 1 | 0 | 6.03 |  |

### q14 · code_retrieval
**题**：保存资源用哪个类？  ·  **gold**：ResourceSaver

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | 保存资源使用 `ResourceSaver` 类（定义在 `core/io/resource_s | 769 | 2 | 1 | 15.37 |  |
| `kb` | ✓ | 保存资源使用 **`ResourceSaver`** 类（核心方法：`ResourceSaver | 1681 | 3 | 2 | 15.45 |  |
| `kb+superpowers` | ✓ | 保存资源使用 **`ResourceSaver`** 类（`core/io/resource_s | 1841 | 3 | 2 | 10.05 |  |
| `kb+openspec` | ✓ | 保存资源用 **`ResourceSaver`**（`io/resource_saver.cpp | 2506 | 3 | 2 | 26.72 |  |

### q15 · code_retrieval
**题**：文件读写操作用哪个类？  ·  **gold**：FileAccess

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | 文件读写操作使用 **`FileAccess`** 类（定义在 `core/io/file_ac | 975 | 2 | 1 | 10.21 |  |
| `kb` | ✓ | 文件读写操作使用 **`FileAccess`** 类（位于 `core/io/file_acc | 702 | 2 | 1 | 12.57 |  |
| `kb+superpowers` | ✓ | 文件读写操作使用 **`FileAccess`** 类（`core/io/file_access | 1684 | 2 | 1 | 15.76 |  |
| `kb+openspec` | ✓ | 文件读写操作使用 **`FileAccess`** 类（`core/io/file_access | 1574 | 2 | 1 | 10.64 |  |

### q16 · code_retrieval
**题**：目录操作用哪个类？  ·  **gold**：DirAccess

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | 目录操作使用 **`DirAccess`** 类（定义在 `core/io/dir_access | 768 | 2 | 1 | 13.61 |  |
| `kb` | ✓ | 目录操作使用 **`DirAccess`** 类（位于 `io/dir_access.cpp`  | 1707 | 3 | 2 | 18.63 |  |
| `kb+superpowers` | ✓ | 目录操作用 **`DirAccess`** 类（`core/io/dir_access.h`）。 | 1224 | 3 | 2 | 11.77 |  |
| `kb+openspec` | ✓ | 目录操作用 **`DirAccess`** 类（`io/dir_access.h` / `io/ | 1971 | 3 | 2 | 11.29 |  |

### q17 · code_retrieval
**题**：消息队列用哪个类？  ·  **gold**：MessageQueue

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | 消息队列使用 **`MessageQueue`** 类，定义在 `core/object/mes | 752 | 2 | 1 | 8.87 |  |
| `kb` | ✓ | 消息队列使用 **`MessageQueue`** 类（定义在 `core/object/mes | 913 | 2 | 1 | 15.01 |  |
| `kb+superpowers` | ✓ | 消息队列用 **`MessageQueue`**（定义在 `core/object/messag | 1288 | 2 | 1 | 9.34 |  |
| `kb+openspec` | ✓ | 消息队列用 **`MessageQueue`** 类（定义在 `core/object/mess | 1472 | 2 | 1 | 8.45 |  |

### q18 · code_retrieval
**题**：引擎主类叫什么？  ·  **gold**：Engine

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | 引擎主类是 **`Engine`**，定义在 `core/config/engine.h` 中。 | 798 | 2 | 1 | 10.38 |  |
| `kb` | ✓ | 引擎主类是 `core_bind::Engine`（即 `core_bind.cpp` 中的 ` | 930 | 2 | 1 | 10.35 |  |
| `kb+superpowers` | ✓ | 引擎主类是 **`core_bind::Engine`**（在 `core_bind.cpp`  | 1578 | 2 | 1 | 15.53 |  |
| `kb+openspec` | ✓ | 引擎主类是 **`Engine`**（位于 `core_bind` 命名空间，即 `core_b | 1182 | 2 | 1 | 5.48 |  |

### q19 · code_retrieval
**题**：主循环基类叫什么？  ·  **gold**：MainLoop

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | `MainLoop` | 345 | 1 | 0 | 3.15 |  |
| `kb` | ✓ | 主循环基类是 **`MainLoop`**，定义在 `os/main_loop.h` 中。 | 592 | 2 | 1 | 9.12 |  |
| `kb+superpowers` | ✓ | `MainLoop`（定义在 `os/main_loop.h`）。 | 1566 | 2 | 1 | 9.51 |  |
| `kb+openspec` | ✓ | 主循环基类是 **`MainLoop`**，定义在 `os/main_loop.h` 中。 | 1470 | 2 | 1 | 8.78 |  |

### q20 · code_retrieval
**题**：撤销重做系统用哪个类？  ·  **gold**：UndoRedo

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | `UndoRedo` | 347 | 1 | 0 | 3.38 |  |
| `kb` | ✓ | `UndoRedo` | 31 | 1 | 0 | 2.77 |  |
| `kb+superpowers` | ✓ | `UndoRedo`（定义在 `core/object/undo_redo.cpp`）。 | 1273 | 2 | 1 | 10.83 |  |
| `kb+openspec` | ✓ | 撤销重做系统使用 **`UndoRedo`** 类（定义在 `core/object/undo_ | 1521 | 2 | 1 | 8.97 |  |

### q21 · code_retrieval
**题**：节点路径用哪个类？  ·  **gold**：NodePath

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | `NodePath` | 344 | 1 | 0 | 3.29 |  |
| `kb` | ✓ | `NodePath` | 348 | 1 | 0 | 5.41 |  |
| `kb+superpowers` | ✓ | `NodePath` | 679 | 1 | 0 | 3.07 |  |
| `kb+openspec` | ✓ | `NodePath` | 627 | 1 | 0 | 3.01 |  |

### q22 · code_retrieval
**题**：字符串名（优化版字符串）用哪个类？  ·  **gold**：StringName

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | `StringName` | 349 | 1 | 0 | 5.56 |  |
| `kb` | ✓ | `StringName`（定义在 `core/string/string_name.h`）。 | 905 | 2 | 1 | 13.85 |  |
| `kb+superpowers` | ✓ | `StringName` | 684 | 1 | 0 | 3.08 |  |
| `kb+openspec` | ✓ | `StringName` | 632 | 1 | 0 | 3.87 |  |

### q23 · code_retrieval
**题**：随机数生成器用哪个类？  ·  **gold**：RandomNumberGenerator

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | `RandomNumberGenerator` | 347 | 1 | 0 | 3.27 |  |
| `kb` | ✓ | 使用 **`RandomNumberGenerator`** 类（定义在 `core/math/ | 980 | 2 | 1 | 16.79 |  |
| `kb+superpowers` | ✓ | `RandomNumberGenerator`（定义在 `core/math/random_nu | 1638 | 2 | 1 | 8.29 |  |
| `kb+openspec` | ✓ | 用 **`RandomNumberGenerator`**（定义在 `core/math/ran | 1536 | 2 | 1 | 6.78 |  |

### q24 · code_retrieval
**题**：加密解密用哪个类？  ·  **gold**：Crypto

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | 加密解密主要用以下类：  - **`Crypto`** — 高层加密接口，提供 AES-256- | 1617 | 3 | 2 | 14.96 |  |
| `kb` | ✓ | 加密解密使用 **`Crypto`** 类（位于 `core/crypto/crypto.cpp | 1013 | 2 | 1 | 12.35 |  |
| `kb+superpowers` | ✓ | 加密解密用 **`Crypto`** 类（`core/crypto/crypto.cpp`）。  | 1622 | 2 | 1 | 7.9 |  |
| `kb+openspec` | ✓ | 加密解密用 **`Crypto`** 类（`core/crypto/crypto.cpp`）。  | 981 | 2 | 1 | 6.84 |  |

### q25 · code_retrieval
**题**：翻译/本地化服务器用哪个类？  ·  **gold**：TranslationServer

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | `TranslationServer` | 347 | 1 | 0 | 3.56 |  |
| `kb` | ✓ | `TranslationServer`（定义在 `core/string/translation | 292 | 2 | 1 | 6.16 |  |
| `kb+superpowers` | ✓ | `TranslationServer`（定义在 `core/string/translation | 936 | 2 | 1 | 4.59 |  |
| `kb+openspec` | ✓ | `TranslationServer`（定义在 `core/string/translation | 1534 | 2 | 1 | 8.48 |  |

### q26 · code_retrieval
**题**：HTTP 客户端用哪个类？  ·  **gold**：HTTPClient

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | `HTTPClient` | 27 | 1 | 0 | 2.32 |  |
| `kb` | ✓ | `HTTPClient` | 31 | 1 | 0 | 2.88 |  |
| `kb+superpowers` | ✓ | `HTTPClient`（定义在 `io/http_client.h`）。其 TCP 实现为 ` | 1274 | 2 | 1 | 10.86 |  |
| `kb+openspec` | ✓ | `HTTPClient` | 630 | 1 | 0 | 3.16 |  |

### q27 · bug_fix
**题**：对象内存泄漏：某对象被释放后仍被引用（use-after-free）。Godot 里删除/释放对象的底层函数叫什么？  ·  **gold**：core/memory/memory.h, memdelete

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | Godot 中删除/释放对象的底层函数主要有：  1. **`memdelete()`** —  | 5058 | 6 | 7 | 33.06 |  |
| `kb` | ✓ | Godot 中删除/释放对象的核心底层函数和机制：  1. **`memdelete`**（`o | 1050 | 2 | 2 | 8.19 |  |
| `kb+superpowers` | ✓ | Godot 中删除/释放对象涉及以下关键函数：  ## 脚本层（GDScript / API 可 | 2793 | 3 | 3 | 22.3 |  |
| `kb+openspec` | ✓ | Godot 中删除/释放对象的核心底层函数和机制如下：  ## 关键符号  / 符号 / 所在文 | 4473 | 11 | 11 | 52.49 |  |

### q28 · bug_fix
**题**：字符串格式化在某些 locale 边界情况下输出乱码，疑是底层格式化例程的 bug。Godot 里字符串格式化的底层函数叫什么？  ·  **gold**：core/string/print_string.cpp, vformat

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | Godot 字符串格式化的底层函数主要有两个，都在 `core/string/ustring.c | 3903 | 4 | 6 | 17.51 |  |
| `kb` | ✓ | Godot 字符串格式化的底层核心函数是：  - **`String::sprintf`** — | 1889 | 3 | 2 | 13.93 |  |
| `kb+superpowers` | ✗ | Godot 字符串格式化的底层函数是：  - **`String::format`** — 定义 | 1753 | 2 | 1 | 10.2 |  |
| `kb+openspec` | ✓ | Godot 字符串格式化的底层函数是：  - **`String::sprintf`** — 定 | 2145 | 3 | 2 | 16.27 |  |

### q29 · bug_fix
**题**：A* 寻路在两点间返回了错误路径，忽略了一个障碍物。Godot 里负责计算寻路路径的是哪个类？  ·  **gold**：AStar, core/math/a_star.h

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | 负责 A* 寻路路径计算的类是 **`AStar`**（通用 2D/3D 图寻路，定义在 `co | 952 | 2 | 1 | 13.81 |  |
| `kb` | ✓ | Godot 中负责 A* 寻路路径计算的类有三个：  - **`AStar3D`** — 3D  | 851 | 2 | 1 | 10.64 |  |
| `kb+superpowers` | ✓ | Godot 中负责 A* 寻路路径计算的类有三个，均在 `core/math/` 下：  / 类 | 1644 | 3 | 2 | 16.78 |  |
| `kb+openspec` | ✓ | Godot 中负责 A* 寻路路径计算的类主要有以下几个：  1. **`AStar3D`**  | 2793 | 4 | 3 | 20.58 |  |

## 各臂速览
- `no-kb`: acc=0.966 · tokens=944.9 · llm_calls=1.86 · steps=1.17 · t=9.18s · tools=0.48
- `kb`: acc=0.966 · tokens=830.7 · llm_calls=1.9 · steps=0.97 · t=15.38s · tools=0.76
- `kb+superpowers`: acc=0.931 · tokens=1433 · llm_calls=2 · steps=1.03 · t=9.86s · tools=0.76
- `kb+openspec`: acc=0.966 · tokens=1397.7 · llm_calls=2.14 · steps=1.17 · t=10.56s · tools=0.66

## 诚实边界（必须看）
- **accuracy 由 GLM 生成 + GLM 判分**（同家族 self-preference）→ 相对参考值，非绝对回归值。
- **skills 臂注入的是 bundled 精简 SOP 文本**（`eval/arms/skills_bundled/`），**非完整 Claude Code skill 运行时**（无触发机制/hook）。是 headless 可复现近似，不等于真实 skill 效果。
- **`cost_$` 依赖 MODEL_PRICES 单价**，单价未知则 0（占位）；当前价格为占位，勿当真实成本。
- 样本量小（29 题），结论显著性有限——看趋势勿绝对化。
- bug_fix 题仍用 symbol/file broad match 判分（非修复质量 LLM-judge）。

## 怎么看 skills 值不值
对比 `kb+superpowers` / `kb+openspec` vs `kb` 的 accuracy（skills 帮没帮）+ mean_total_tokens（skills 多花多少）。**bug_fix 题上差异最可能显现**（纯 code_retrieval 上 skills 显不出价值）。

详见 `summary.json`（臂×指标矩阵，程序消费用）、各臂 `arms/<arm>/`（config + aggregate + episodes）。

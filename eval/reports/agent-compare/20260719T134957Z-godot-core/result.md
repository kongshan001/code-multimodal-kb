# agent-compare 结果 · target=godot-core · model=glm-4.7 · engine=sdk
> 37 题 × 1 runs × 4 臂。

## 怎么读懂这份报告（规则，先看）

**4 个臂是什么**：
- `no-kb` = 只给 grep + 读文件（朴素搜索，无知识库）
- `kb` = 给 cmm 代码知识库（语义检索符号）
- `kb+superpowers` / `kb+openspec` = kb + 往 agent 指令里注入 superpowers/openspec 的工程纪律 SOP
  （注入的是**精简 SOP 文本**，不是真 skill 运行时——见末尾诚实边界）

**答对（✓）怎么判**：终答里含 gold 符号或文件名就算对（broad 子串匹配，零 LLM judge）。
**gold 是什么**：每题的标准答案——来自 codegraph 挖出的真实代码符号/文件，构造即正确（不是人拍脑袋写的）。

**某题被标截断（逐题表 `截断` 列 ⚠ / `truncated_rate` > 0）**：agent 跑满 backstop（默认 **30 轮**，no-kb 臂 **12 轮**，防死循环的安全网）仍未自然给出答案 = **真卡住**。本跑采用 run-until-answer：**不 inject 猜测答案**，那题的 `answer` 是占位（判分即错）。backstop 远超正常收敛所需，所以截断率衡量的是 agent 真正卡死的比例，不是被步数上限人为截断。

**`thinking` / 思考过程**：GLM-5.1 经这个端点不返独立 thinking block，所以思考 = agent 的推理文本（assistant 回答），不是单独的隐藏思维链——别当成完整思考链。
**`cost_$`**：token × 单价；单价是**占位**（待确认 GLM 定价），勿当真实成本，看相对大小即可。
**`tool_diversity` 高**：可能 agent 在乱试不同工具（没方向），未必好事。

## 谁赢
- **准确率最高**：`kb+superpowers`（accuracy=0.973）
- **最省 token**：`kb`（mean_total_tokens=3864.1）
- **最省钱**：`kb`（mean_cost_$=0.0094）
- **KB vs 无 KB token 压缩**：3.22×（>1 = KB 省）

## 指标怎么看（小白版）
| 指标 | 大白话 |
|---|---|
| `accuracy` | 答对率 = 答对的题 ÷ 总题数。0~1，越高越好 |
| `mean_total_tokens` | 平均每题处理多少 token（= 新读 input + 缓存重读 cache_read + output，真实处理量）。越少越省 |
| `mean_cache_read_tokens` | 其中命中 prompt 缓存重读的 token（缓存多的臂 prompt 大，如 skills 臂带 SOP） |
| `mean_llm_calls` | 平均每题调几次大模型。越少越快越省 |
| `mean_tool_steps` | 平均每题用几次工具（cmm/grep/read） |
| `mean_wall_clock_s` | 平均每题跑多久（秒） |
| `mean_cost_$` | 平均每题花多少钱（≈ token × 单价） |
| `tool_diversity` | 平均用了几种不同工具（高了可能在乱试） |
| `truncated_rate` | 多少题没在步数内答完（卡住了）。0 最好 |
| `no_tool_rate` | 多少题 agent 根本没调工具就答了（凭记忆）。高了说明该臂准确率不是工具/KB 贡献的——测量纯度 |
| `context_compression` | 有 KB 比无 KB 省几倍 token（>1=KB 省；仅 no-kb+kb 都跑时给） |

## 对比矩阵
| 臂 | accuracy | mean_total_tokens | mean_cache_read_tokens | mean_llm_calls | mean_tool_steps | mean_wall_clock_s | mean_cost_$ | tool_diversity | truncated_rate | no_tool_rate | n_episodes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `no-kb` | 0.784 | 12460.8 | 10667.2 | 8.22 | 7.38 | 17.72 | 0.0223 | 1.92 | 0.216 | 0.0 | 37 |
| `kb` | 0.919 | 3864.1 | 3182.7 | 3.3 | 2.3 | 10.06 | 0.0094 | 1.24 | 0.0 | 0.0 | 37 |
| `kb+superpowers` | 0.973 | 5583.2 | 4851.9 | 3.68 | 2.65 | 10.82 | 0.011 | 1.38 | 0.0 | 0.0 | 37 |
| `kb+openspec` | 0.919 | 5069.5 | 4339.9 | 3.43 | 2.43 | 9.55 | 0.0107 | 1.27 | 0.0 | 0.0 | 37 |

## 逐题得分对照

> 每题各臂的答对 / 答案 / 指标（37 题 × 4 臂）。看哪题谁答对、谁省 token、谁卡住。

### q01 · code_retrieval
**题**：Godot 里字符串格式化的底层函数叫什么？  ·  **gold**：vformat

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✗ | (未在限定步数内自然作答) | 30335 | 13 | 13 | 35.48 | ⚠卡住 |
| `kb` | ✗ | `String.sprintf` | 3085 | 3 | 2 | 17.81 |  |
| `kb+superpowers` | ✓ | `vformat` | 12698 | 7 | 6 | 23.59 |  |
| `kb+openspec` | ✓ | `vformat` | 6399 | 6 | 5 | 19.34 |  |

### q02 · code_retrieval
**题**：整数转成字符串用哪个函数？  ·  **gold**：itos

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✗ | (未在限定步数内自然作答) | 29680 | 14 | 14 | 25.57 | ⚠卡住 |
| `kb` | ✗ | `String::num`、`String::num_int64`、`String::num_u | 4979 | 4 | 3 | 11.7 |  |
| `kb+superpowers` | ✓ | `itos`、`String::num`、`String::num_int64`、`String | 10618 | 6 | 5 | 13.55 |  |
| `kb+openspec` | ✓ | `itos` | 3953 | 3 | 2 | 7.4 |  |

### q04 · code_retrieval
**题**：A* 寻路算法用哪个类？  ·  **gold**：AStar

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | `AStar`、`AStarGrid2D` | 6318 | 5 | 4 | 11.62 |  |
| `kb` | ✓ | `AStar2D`、`AStar3D` | 3368 | 3 | 2 | 8.25 |  |
| `kb+superpowers` | ✓ | `AStar2D`、`AStar3D` | 9891 | 6 | 5 | 11.61 |  |
| `kb+openspec` | ✓ | `AStar2D`、`AStar3D` | 4152 | 3 | 2 | 8.12 |  |

### q03 · code_retrieval
**题**：删除对象、释放内存用哪个函数？  ·  **gold**：memdelete

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✗ | 我来查找一下 Godot 中删除对象和释放内存的相关函数。 | 31568 | 15 | 14 | 24.87 | ⚠卡住 |
| `kb` | ✓ | `memdelete` | 2024 | 2 | 1 | 8.41 |  |
| `kb+superpowers` | ✓ | `memdelete`、`memdelete_arr`、`memdelete_allocator | 9835 | 6 | 5 | 12.98 |  |
| `kb+openspec` | ✗ | `operator delete`, `free` | 2726 | 2 | 1 | 7.69 |  |

### q05 · code_retrieval
**题**：操作系统抽象层用哪个类？  ·  **gold**：OS

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | `OS` | 15661 | 10 | 9 | 20.37 |  |
| `kb` | ✓ | `OS` | 3167 | 3 | 2 | 8.27 |  |
| `kb+superpowers` | ✓ | `OS` | 7255 | 5 | 4 | 12.47 |  |
| `kb+openspec` | ✓ | `OS` | 3965 | 3 | 2 | 9.17 |  |

### q06 · code_retrieval
**题**：表示颜色的类叫什么？  ·  **gold**：Color

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✗ | (未在限定步数内自然作答) | 18804 | 12 | 12 | 23.55 | ⚠卡住 |
| `kb` | ✓ | `Color` | 1889 | 2 | 1 | 6.78 |  |
| `kb+superpowers` | ✓ | `Color` | 2548 | 2 | 1 | 9.89 |  |
| `kb+openspec` | ✓ | `Color` | 2450 | 2 | 1 | 6.49 |  |

### q07 · code_retrieval
**题**：二维向量用哪个类？  ·  **gold**：Vector2

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | `Vector2` | 6045 | 5 | 4 | 11.0 |  |
| `kb` | ✓ | `Vector2` | 1847 | 2 | 1 | 6.84 |  |
| `kb+superpowers` | ✓ | `Vector2` | 2561 | 2 | 1 | 7.24 |  |
| `kb+openspec` | ✓ | `Vector2` | 4041 | 3 | 2 | 11.04 |  |

### q08 · code_retrieval
**题**：三维向量用哪个类？  ·  **gold**：Vector3

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | `Vector3` | 10775 | 7 | 6 | 16.62 |  |
| `kb` | ✓ | `Vector3` | 1882 | 2 | 1 | 8.91 |  |
| `kb+superpowers` | ✓ | `Vector3` | 2557 | 2 | 1 | 8.18 |  |
| `kb+openspec` | ✓ | `Vector3` | 2447 | 2 | 1 | 6.81 |  |

### q09 · code_retrieval
**题**：四元数用哪个类？  ·  **gold**：Quaternion

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | `Quaternion` | 10131 | 8 | 7 | 18.28 |  |
| `kb` | ✓ | `Quaternion` | 1935 | 2 | 1 | 7.52 |  |
| `kb+superpowers` | ✓ | `Quaternion` | 2621 | 2 | 1 | 6.83 |  |
| `kb+openspec` | ✓ | `Quaternion` | 2484 | 2 | 1 | 7.14 |  |

### q10 · code_retrieval
**题**：二维矩形用哪个类？  ·  **gold**：Rect2

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | `Rect2`、`Rect2i` | 6987 | 5 | 4 | 13.26 |  |
| `kb` | ✓ | `Rect2` | 2977 | 3 | 2 | 8.11 |  |
| `kb+superpowers` | ✓ | `Rect2` | 2592 | 2 | 1 | 7.68 |  |
| `kb+openspec` | ✓ | `Rect2` | 2492 | 2 | 1 | 6.65 |  |

### q11 · code_retrieval
**题**：JSON 解析用哪个类？  ·  **gold**：JSON

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | `JSON` | 7874 | 6 | 5 | 14.04 |  |
| `kb` | ✓ | `JSON` | 1931 | 2 | 1 | 8.54 |  |
| `kb+superpowers` | ✓ | `JSON` | 2661 | 2 | 1 | 8.89 |  |
| `kb+openspec` | ✓ | `JSON` | 2531 | 2 | 1 | 7.66 |  |

### q12 · code_retrieval
**题**：图像数据用哪个类？  ·  **gold**：Image

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | `Image` | 4336 | 4 | 3 | 10.36 |  |
| `kb` | ✓ | `Image` | 1931 | 2 | 1 | 8.7 |  |
| `kb+superpowers` | ✓ | `Image` | 4252 | 3 | 2 | 10.65 |  |
| `kb+openspec` | ✓ | `Image` | 2448 | 2 | 1 | 7.39 |  |

### q13 · code_retrieval
**题**：加载资源用哪个类？  ·  **gold**：ResourceLoader

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | `ResourceLoader` | 5708 | 4 | 3 | 10.85 |  |
| `kb` | ✓ | `ResourceLoader` | 1901 | 2 | 1 | 7.69 |  |
| `kb+superpowers` | ✓ | `ResourceLoader` | 2623 | 2 | 1 | 8.77 |  |
| `kb+openspec` | ✓ | `ResourceLoader` | 2456 | 2 | 1 | 8.43 |  |

### q14 · code_retrieval
**题**：保存资源用哪个类？  ·  **gold**：ResourceSaver

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | `ResourceSaver` | 4998 | 4 | 3 | 10.42 |  |
| `kb` | ✓ | `ResourceSaver` | 3268 | 3 | 2 | 10.27 |  |
| `kb+superpowers` | ✓ | `ResourceSaver` | 2649 | 2 | 1 | 8.32 |  |
| `kb+openspec` | ✓ | ResourceSaver | 3957 | 3 | 2 | 9.46 |  |

### q15 · code_retrieval
**题**：文件读写操作用哪个类？  ·  **gold**：FileAccess

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | `FileAccess` | 4543 | 4 | 3 | 10.88 |  |
| `kb` | ✓ | `FileAccess` | 3263 | 3 | 2 | 10.9 |  |
| `kb+superpowers` | ✓ | `FileAccess` | 6127 | 4 | 3 | 12.66 |  |
| `kb+openspec` | ✓ | `FileAccess` | 5806 | 4 | 3 | 11.89 |  |

### q16 · code_retrieval
**题**：目录操作用哪个类？  ·  **gold**：DirAccess

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | `DirAccess` | 5811 | 5 | 4 | 11.6 |  |
| `kb` | ✓ | DirAccess | 3215 | 3 | 2 | 8.42 |  |
| `kb+superpowers` | ✓ | `DirAccess` | 4186 | 3 | 2 | 10.09 |  |
| `kb+openspec` | ✓ | `DirAccess` | 4014 | 3 | 2 | 9.26 |  |

### q17 · code_retrieval
**题**：消息队列用哪个类？  ·  **gold**：MessageQueue

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | `MessageQueue` | 5178 | 5 | 4 | 11.7 |  |
| `kb` | ✓ | `MessageQueue` | 3195 | 3 | 2 | 11.26 |  |
| `kb+superpowers` | ✓ | `MessageQueue` | 2587 | 2 | 1 | 8.97 |  |
| `kb+openspec` | ✓ | `MessageQueue` | 2550 | 2 | 1 | 8.66 |  |

### q18 · code_retrieval
**题**：引擎主类叫什么？  ·  **gold**：Engine

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | `Engine` | 4312 | 4 | 3 | 10.42 |  |
| `kb` | ✓ | `Engine` | 12654 | 9 | 8 | 17.81 |  |
| `kb+superpowers` | ✓ | `Engine` | 7448 | 5 | 4 | 11.81 |  |
| `kb+openspec` | ✓ | `Engine` | 9119 | 6 | 5 | 13.02 |  |

### q19 · code_retrieval
**题**：主循环基类叫什么？  ·  **gold**：MainLoop

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | `MainLoop` | 7343 | 6 | 5 | 12.24 |  |
| `kb` | ✓ | `MainLoop` | 1933 | 2 | 1 | 6.79 |  |
| `kb+superpowers` | ✓ | `MainLoop` | 2543 | 2 | 1 | 7.45 |  |
| `kb+openspec` | ✓ | `MainLoop` | 5564 | 4 | 3 | 9.25 |  |

### q20 · code_retrieval
**题**：撤销重做系统用哪个类？  ·  **gold**：UndoRedo

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | `UndoRedo` | 7839 | 6 | 5 | 14.69 |  |
| `kb` | ✓ | `UndoRedo` | 1968 | 2 | 1 | 8.24 |  |
| `kb+superpowers` | ✓ | `UndoRedo` | 2604 | 2 | 1 | 8.44 |  |
| `kb+openspec` | ✓ | `UndoRedo` | 2555 | 2 | 1 | 6.32 |  |

### q22 · code_retrieval
**题**：字符串名（优化版字符串）用哪个类？  ·  **gold**：StringName

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | `StringName` | 1857 | 2 | 1 | 7.63 |  |
| `kb` | ✓ | `StringName` | 1963 | 2 | 1 | 12.81 |  |
| `kb+superpowers` | ✓ | `StringName` | 2643 | 2 | 1 | 8.71 |  |
| `kb+openspec` | ✓ | StringName | 2658 | 2 | 1 | 9.46 |  |

### q21 · code_retrieval
**题**：节点路径用哪个类？  ·  **gold**：NodePath

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | NodePath | 16180 | 9 | 8 | 19.17 |  |
| `kb` | ✓ | `NodePath` | 1882 | 2 | 1 | 8.31 |  |
| `kb+superpowers` | ✓ | `NodePath` | 2610 | 2 | 1 | 8.45 |  |
| `kb+openspec` | ✓ | `NodePath` | 2450 | 2 | 1 | 8.43 |  |

### q23 · code_retrieval
**题**：随机数生成器用哪个类？  ·  **gold**：RandomNumberGenerator

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | `RandomNumberGenerator` | 1876 | 2 | 1 | 6.87 |  |
| `kb` | ✓ | `RandomNumberGenerator` | 1924 | 2 | 1 | 6.7 |  |
| `kb+superpowers` | ✓ | `RandomNumberGenerator` | 2644 | 2 | 1 | 7.05 |  |
| `kb+openspec` | ✓ | `RandomNumberGenerator` | 2527 | 2 | 1 | 9.16 |  |

### q24 · code_retrieval
**题**：加密解密用哪个类？  ·  **gold**：Crypto

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | `Crypto` | 5302 | 5 | 4 | 19.59 |  |
| `kb` | ✓ | `AESContext`, `Crypto`, `CryptoCore`, `CryptoKey | 11196 | 8 | 7 | 18.43 |  |
| `kb+superpowers` | ✓ | `Crypto` | 10091 | 6 | 5 | 11.57 |  |
| `kb+openspec` | ✓ | `Crypto`、`CryptoKey` | 21028 | 11 | 10 | 16.66 |  |

### q25 · code_retrieval
**题**：翻译/本地化服务器用哪个类？  ·  **gold**：TranslationServer

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | `TranslationServer` | 5200 | 5 | 4 | 21.0 |  |
| `kb` | ✓ | `TranslationServer` | 1948 | 2 | 1 | 8.77 |  |
| `kb+superpowers` | ✓ | `TranslationServer` | 2612 | 2 | 1 | 7.32 |  |
| `kb+openspec` | ✓ | `TranslationServer` | 2552 | 2 | 1 | 6.22 |  |

### q26 · code_retrieval
**题**：HTTP 客户端用哪个类？  ·  **gold**：HTTPClient

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | `HTTPClient` | 1855 | 2 | 1 | 13.35 |  |
| `kb` | ✓ | `HTTPClient` | 1974 | 2 | 1 | 10.41 |  |
| `kb+superpowers` | ✓ | `HTTPClient` | 6236 | 4 | 3 | 19.44 |  |
| `kb+openspec` | ✓ | HTTPClient | 2497 | 2 | 1 | 8.54 |  |

### q27 · bug_fix
**题**：对象内存泄漏：某对象被释放后仍被引用（use-after-free）。Godot 里删除/释放对象的底层函数叫什么？  ·  **gold**：core/memory/memory.h, memdelete

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✗ | (未在限定步数内自然作答) | 38921 | 24 | 24 | 30.05 | ⚠卡住 |
| `kb` | ✗ | `gdextension_object_destroy` | 8802 | 6 | 5 | 14.86 |  |
| `kb+superpowers` | ✓ | `memdelete` | 15588 | 8 | 7 | 26.19 |  |
| `kb+openspec` | ✗ | `RefCounted::unreference` | 10513 | 6 | 5 | 11.83 |  |

### q28 · bug_fix
**题**：字符串格式化在某些 locale 边界情况下输出乱码，疑是底层格式化例程的 bug。Godot 里字符串格式化的底层函数叫什么？  ·  **gold**：core/string/print_string.cpp, vformat

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✗ | 我来搜索 Godot 中的字符串格式化底层函数。 | 29311 | 19 | 18 | 26.75 | ⚠卡住 |
| `kb` | ✓ | `String.sprintf`、`String.format`、`vformat` | 2076 | 2 | 1 | 6.68 |  |
| `kb+superpowers` | ✗ | `String.sprintf` 和 `String.format` | 5989 | 4 | 3 | 10.19 |  |
| `kb+openspec` | ✗ | `String::sprintf`, `String::format` | 7566 | 5 | 4 | 13.22 |  |

### q29 · bug_fix
**题**：A* 寻路在两点间返回了错误路径，忽略了一个障碍物。Godot 里负责计算寻路路径的是哪个类？  ·  **gold**：AStar, core/math/a_star.h

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | `AStarGrid2D`（还有 `AStar2D` 和 `AStar3D`） | 9362 | 8 | 7 | 15.74 |  |
| `kb` | ✓ | `AStar2D`、`AStar3D` | 10666 | 7 | 6 | 13.98 |  |
| `kb+superpowers` | ✓ | `AStar2D` / `AStar3D` | 2885 | 3 | 2 | 7.96 |  |
| `kb+openspec` | ✓ | `AStar2D`, `AStar3D` | 11995 | 7 | 6 | 13.57 |  |

### q30 · code_retrieval
**题**：Godot core 里 Vector、PackedArray 等容器底层共享同一份数据、写时才复制（copy-on-write）的数据封装类叫什么？  ·  **gold**：CowData

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | `CowData` | 9531 | 8 | 7 | 15.37 |  |
| `kb` | ✓ | `CowData` | 6309 | 5 | 4 | 10.09 |  |
| `kb+superpowers` | ✓ | `CowData` | 6075 | 5 | 3 | 9.05 |  |
| `kb+openspec` | ✓ | `CowData` | 7965 | 5 | 4 | 9.07 |  |

### q31 · code_retrieval
**题**：Godot core 里用来替代 std::vector、默认不在堆上分配、专供内部用的小型动态数组类叫什么？  ·  **gold**：LocalVector

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | `LocalVector` | 19958 | 11 | 10 | 23.94 |  |
| `kb` | ✓ | `LocalVector` | 6403 | 5 | 4 | 14.06 |  |
| `kb+superpowers` | ✓ | `LocalVector` | 8200 | 5 | 4 | 11.48 |  |
| `kb+openspec` | ✓ | `LocalVector` | 8251 | 5 | 4 | 13.64 |  |

### q32 · code_retrieval
**题**：Godot core 里把链表指针内嵌进节点自身（侵入式，不额外分配节点）的链表类叫什么？  ·  **gold**：SelfList

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | `SelfList` | 10265 | 8 | 7 | 18.84 |  |
| `kb` | ✓ | `SelfList` | 5943 | 5 | 4 | 10.21 |  |
| `kb+superpowers` | ✓ | `SelfList` | 13829 | 8 | 7 | 13.79 |  |
| `kb+openspec` | ✓ | `SelfList` | 5789 | 4 | 3 | 9.12 |  |

### q33 · code_retrieval
**题**：Godot core 里按页批量分配固定大小对象、避免频繁 new/delete 的内存池类叫什么？  ·  **gold**：PagedAllocator

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | `PagedAllocator` | 18638 | 14 | 13 | 25.25 |  |
| `kb` | ✓ | `PagedAllocator` | 6340 | 5 | 4 | 10.55 |  |
| `kb+superpowers` | ✓ | `PagedAllocator` | 6459 | 5 | 4 | 10.77 |  |
| `kb+openspec` | ✓ | `PagedAllocator` | 2602 | 2 | 1 | 7.33 |  |

### q34 · code_retrieval
**题**：Godot core 里用原子操作实现线程安全引用计数的类叫什么？  ·  **gold**：SafeRefCount

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | `SafeRefcount` | 8546 | 8 | 7 | 17.2 |  |
| `kb` | ✓ | `SafeRefCount` | 7050 | 6 | 5 | 12.41 |  |
| `kb+superpowers` | ✓ | `SafeRefCount` | 11785 | 7 | 6 | 14.36 |  |
| `kb+openspec` | ✓ | `SafeRefCount` | 15312 | 8 | 7 | 13.73 |  |

### q35 · code_retrieval
**题**：Godot core 里实现并查集（union-find / disjoint-set）的类叫什么？  ·  **gold**：DisjointSet

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✗ | (未在限定步数内自然作答) | 21428 | 15 | 15 | 31.39 | ⚠卡住 |
| `kb` | ✓ | `DisjointSet` | 2007 | 2 | 1 | 6.84 |  |
| `kb+superpowers` | ✓ | `DisjointSet` | 2609 | 2 | 1 | 7.31 |  |
| `kb+openspec` | ✓ | `DisjointSet` | 2591 | 2 | 1 | 8.48 |  |

### q36 · code_retrieval
**题**：Godot core 里用于动态场景的层次包围盒（bounding volume hierarchy，broadphase 加速结构）的类叫什么？  ·  **gold**：DynamicBVH

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✗ | (未在限定步数内自然作答) | 20237 | 12 | 12 | 26.95 | ⚠卡住 |
| `kb` | ✓ | `DynamicBVH` | 2043 | 2 | 1 | 7.79 |  |
| `kb+superpowers` | ✓ | `DynamicBVH` | 2764 | 2 | 1 | 9.36 |  |
| `kb+openspec` | ✓ | `DynamicBVH` | 2593 | 2 | 1 | 8.32 |  |

### q37 · code_retrieval
**题**：Godot core 里定长环形缓冲区（先进先出、写满覆盖最旧）的容器类叫什么？  ·  **gold**：RingBuffer

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | `RingBuffer` | 18336 | 10 | 9 | 18.83 |  |
| `kb` | ✓ | `RingBuffer` | 2033 | 2 | 1 | 8.04 |  |
| `kb+superpowers` | ✓ | `RingBuffer` | 2703 | 2 | 1 | 7.36 |  |
| `kb+openspec` | ✓ | `RingBuffer` | 2574 | 2 | 1 | 5.34 |  |

## 各臂速览
- `no-kb`: acc=0.784 · tokens=12460.8 · llm_calls=8.22 · steps=7.38 · t=17.72s · tools=1.92
- `kb`: acc=0.919 · tokens=3864.1 · llm_calls=3.3 · steps=2.3 · t=10.06s · tools=1.24
- `kb+superpowers`: acc=0.973 · tokens=5583.2 · llm_calls=3.68 · steps=2.65 · t=10.82s · tools=1.38
- `kb+openspec`: acc=0.919 · tokens=5069.5 · llm_calls=3.43 · steps=2.43 · t=9.55s · tools=1.27

## 工具使用 / 测量纯度（KB 到底帮没帮）

> `no_tool_rate` = 该臂多少题**没调任何工具**就答了（凭模型记忆）。这些题答对**不算工具/KB 的贡献**。
> 拆开看 `acc_with_tool`（用了工具的题的准确率）vs `acc_no_tool`（没用的）——前者才反映工具价值。

| 臂 | no_tool_rate | acc_with_tool | acc_no_tool | 解读 |
|---|---|---|---|---|
| `no-kb` | 0.0 | 0.784 | - | 每题都用了工具 |
| `kb` | 0.0 | 0.919 | - | 每题都用了工具 |
| `kb+superpowers` | 0.0 | 0.973 | - | 每题都用了工具 |
| `kb+openspec` | 0.0 | 0.919 | - | 每题都用了工具 |

## 诚实边界（必须看）
- **accuracy 由 GLM 生成 + GLM 判分**（同家族 self-preference）→ 相对参考值，非绝对回归值。
- **skills 臂注入的是 bundled 精简 SOP 文本**（`eval/arms/skills_bundled/`），**非完整 Claude Code skill 运行时**（无触发机制/hook）。是 headless 可复现近似，不等于真实 skill 效果。
- **`cost_$` 依赖 MODEL_PRICES 单价**，单价未知则 0（占位）；当前价格为占位，勿当真实成本。
- 样本量小（37 题），结论显著性有限——看趋势勿绝对化。
- bug_fix 题仍用 symbol/file broad match 判分（非修复质量 LLM-judge）。

## 怎么看 skills 值不值
对比 `kb+superpowers` / `kb+openspec` vs `kb` 的 accuracy（skills 帮没帮）+ mean_total_tokens（skills 多花多少）。**bug_fix 题上差异最可能显现**（纯 code_retrieval 上 skills 显不出价值）。

详见 `summary.json`（臂×指标矩阵，程序消费用）、各臂 `arms/<arm>/`（config + aggregate + episodes）。

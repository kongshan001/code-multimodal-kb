# godot-core · Godot 引擎核心代码检索

> 拿 **Godot 4.7 引擎的 `core/`**（大型 C++ 库）当靶子，测代码 KB 在"真·大库"上能不能听懂大白话、找到对的符号。
> 大库是代码检索的**硬考**——符号多、同名多、概念查询多。小库跑满分 ≠ 大库也行。

## 这是什么

- **目标代码**：Godot 4.7-stable 的 `core/`（13504 个代码节点 / 38470 条边 / 1094 个类）——一个真实的大型 C++ 游戏引擎。
- **cmm 项目名**：`Users-ks-128-Documents-godot-src-core`（你机器不同 → 改 `target.local.json`）。

## 测什么

给一句大白话（`string format`、`a star pathfinding`、`delete object free memory`），看 cmm 能不能在前几个结果里找到对的符号（`vformat`、`AStar`、`memdelete`）。

26 道题，混了：
- **精确名查询**：`color` → `Color`（认名字）
- **概念查询**：`operating system abstraction` → `OS`（认概念，更难——grep 抓不到）

## 最新结果

### 代码检索（2026-07-13 · 26 题）

| 方法 | `broad_recall@5` | 大白话 |
|---|---|---|
| **BM25**（cmm 主路） | **0.846** | 前 5 命中 84.6% |
| grep（朴素文本搜索） | 0.692 | 前 5 命中 69.2% |

→ BM25 比 grep **高 22%**，尤其在概念查询上拉开差距（grep 只抓字面，抓不到"概念"）。

### Agent A/B（证明"有 KB 比没 KB 省 token + 更准"）

| 指标 | 值 | 大白话 |
|---|---|---|
| 压缩比（Stage 0，2026-07-13） | **12.71×** | 用 KB 注入比朴素 grep 读文件**省 92% context token** |
| codegraph 臂准确度（Stage 1，2026-07-11） | **0.962** | 真 agent 跑，四臂里最准 |

## 数字怎么看

- **`broad_recall@5`**（主指标）：前 5 个结果里有没有正确答案。Godot 大库**必须看 broad**——`strict recall@5` 在 Godot 上只有 0.5，不是检索烂，是 cmm 把类埋在方法节点下，严格匹配结构上吃亏。broad（名字/路径/全名任一命中）才是公平刻度。
- **压缩比 12.71×**：朴素 agent 要读 ~1750 token 的文件才能答，KB 只注 ~195 token 的符号清单 → 省约 9 成 context。

## 怎么自己跑

```bash
bench run code      --target godot-core --method bm25   # 代码检索（主路）
bench run ab        --target godot-core                 # A/B 省 token（零 LLM，秒级）
bench run ab-agent  --target godot-core                 # 真 agent 准确度（需 LLM 凭据）
```

## 诚实边界

- 大库 `strict recall@5 = 0.5` 是结构问题（类埋在方法下），**不是**检索差——故用 broad。
- ab-agent 的 0.962 由 GLM 判分（生成模型和判分模型同家族，有 self-preference 风险），是**相对参考值**，非绝对回归值。

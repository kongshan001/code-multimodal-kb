# 价值量化 Benchmark 报告 · 2026-07-11

> 本报告把 `eval/reports/*.json` 的实测数据聚合成一张「当前价值」量化视图。
> 所有数字均来自已落盘的评测 JSON（零手算、零 LLM judge），可由
> `eval/run_code_baseline.py` / `run_doc_baseline.py` / `run_crosstool_baseline.py` 复现。
> 指标定义见 `eval/metrics.py`。

## 0. 评测规模与靶子

| 项 | 值 |
|---|---|
| 参考靶子 | Godot 4.7-stable `core/`（真实百万行 C++，417 .cpp/.h）|
| 代码索引规模 | **13504 节点 / 38470 边 / 1094 类**（cmm `fast`/`moderate`）|
| 文档索引规模 | 17 篇 .rst → **72 节点 / 32 边 / 40 社区**（graphify + glm-4.6）|
| 检索评测总次数 | **117 次**（代码 26×3 路 + 参照 21 + 文档 10 + 跨工具 8）|
| 独立评测 JSON | 6 个（bm25/grep/semantic × Godot + graphify 参照 + doc + crosstool）|
| lockfile | `cmm 0.8.1 · graphify 0.8.46 · temp=0 · 零 LLM judge` |

## 1. 核心价值总表（一图看完）

```
                        broad@5    相对 grep    满命中率    盲区率
代码 KB  BM25(主路)     0.846      +22.3% ▲     84.6%       15.4%
代码 KB  grep(对照)     0.692       —            —          19.2%
代码 KB  semantic(兜底) 0.846      +22.3% ▲     —          15.4%
文档 KB  graphify.query 0.700       —           50.0%       —
跨工具   anchoring      1.000       —          100%          0%
```

**一句话价值结论**：在真实百万行 C++ 上，BM25 主路把代码检索 broad@5 从 grep 的 0.692 拉到 **0.846（+22.3%）**；跨工具 anchoring（文档概念→代码定位）**8/8 = 100%**——这是本项目最具差异化的硬证据；文档侧 recall@5=0.70，可用但非优秀。

## 2. 代码侧 · 三路检索对比（Godot core/，n=26）

| method | broad@1 | broad@3 | broad@5 | broad@10 | strict@5 |
|---|---|---|---|---|---|
| grep（`search_code`）| 0.346 | 0.577 | 0.692 | 0.731 | 0.000 |
| semantic（`semantic_query`）| 0.769 | 0.846 | 0.846 | 0.846 | 0.308 |
| **BM25（`search_graph query`）** | **0.846** | **0.846** | **0.846** | **0.885** | **0.500** |

### 2.1 BM25 主路相对 grep 的提升

- **broad@5**：0.692 → 0.846，**相对 +22.3%**（绝对 +0.154）
- **broad@1**：0.346 → 0.846，**相对 +144%**（首条命中能力翻倍式提升）
- **strict@5**：0.000 → 0.500（grep 在大 C++ 上把类埋在方法下，strict 结构性失效；BM25 真返回类/类型节点）

> 这是 design 决策 4「semantic_query 主路」被实证推翻为「BM25 主路」的量化依据。

### 2.2 命中分布

- BM25 broad@5 = 1.0（满命中）：**22/26 = 84.6%**
- BM25 broad@5 = 0（盲区）：**4/26 = 15.4%**

### 2.3 盲区（BM25 救不动的 4 条）

| query | gold | 根因 |
|---|---|---|
| `string format` | `vformat` | 纯概念词，代码不含 |
| `int to string` | `itos` | 纯概念词，代码不含 |
| `delete object free memory` | `memdelete` | 代码含 free/delete 但 gold 是聚合宏 |
| `directory access` | `DirAccess` | snake/CamelCase 错配 |

> 这 4 条是「代码里完全不出现 query 词」的硬限——任何检索都救不了，必须靠 agent NL→关键词翻译层（design 决策 4 不可省的兜底）。
> 注：grep 全盲的概念 query 有 5 条，BM25 救回 3 条（`a star pathfinding`→AStar3D、`operating system`→OS、`delete/free memory`→Memory.free_static），剩 2 条 + directory access 共 4 条仍盲。

### 2.4 小/中型仓库参照（graphify 自身 Python 仓库，n=21）

| recall@1 | recall@3 | recall@5 | recall@10 | broad@5 |
|---|---|---|---|---|
| 0.476 | 0.667 | 0.762 | 0.810 | 0.857 |

> 在中小型 Python 仓库上 cmm `search_code` recall@5=0.762——与 Godot 上的 broad@5=0.846 量级一致，说明工具跨语言/跨规模表现稳定（非 Godot 专属过拟合）。

## 3. 文档侧 · graphify.query（Godot 17-doc 子集，n=10）

| recall@1 | recall@3 | recall@5 | recall@all |
|---|---|---|---|
| 0.217 | 0.600 | **0.700** | 0.833 |

- 满命中（recall@5=1.0）：**5/10 = 50%**
- 漏点根因（3/10）：抽取建图时「方法/回调节点 ↔ 所属类/概念节点」连边偏弱，BFS 从概念节点到不了方法节点（如 `_ready Callback`、`add_child Method`）。
- 亮点：graphify 自动从 NL 选对起始节点（如 `vector normalization and dot product` 自选三起点全命中）——文档侧无需 agent 预翻译，与代码侧 pathfinding 死穴形成对比。

## 4. 跨工具 anchoring（差异化核心，n=8）

| graphify 命中率 | cmm 命中@5 | 跨工具成功率 |
|---|---|---|
| 1.000 | 1.000 | **1.000（8/8）** |

链路：`NL 概念 → graphify 文档节点 → 抽真实标识符 → cmm 代码定位`，8 个概念（Vector2/Vector3/Transform2D/Resource/RandomNumberGenerator/Expression/Quaternion/Signals）全部端到端命中正确代码文件。

> 这是「文档↔代码双向定位」——整条 KB 链路最有差异化价值的环节，100% 成功率是当前最强证据。

## 5. 成本 / 效率

| 项 | 值 |
|---|---|
| 文档建图 LLM 成本 | 17 篇 → **$0.22**（glm-4.6）|
| 全量 godot-docs 预估 | ~$27（~3000 页，未跑）|
| 代码索引 | cmm 单机静态二进制，零 LLM、零 GPU |
| 检索 | 查询阶段两路均**不调 LLM**（BM25/图遍历），毫秒级 |
| 凭据 | 一把 BigModel/GLM key 同时解锁「文档建图 + Mem0 抽取 + 文档评测」|

## 6. 价值边界（诚实）

本报告量化的价值有以下**边界**，引用时须注明：

1. **gold 偏软**：代码侧 gold 是 architecture-derived（cmm 实测符号派生），**非 PR 反挖**（task 2.4 未做）。分数可信但偏乐观，PR 反挖是更硬的 scale-up。
2. **小 N**：代码 26 / 文档 10 / 跨工具 8——非 RepoBench/SWE-Lancer 全量规模（HF 需 token + 范式不对口，留作 scale-up）。
3. **单仓库单语言**：仅 Godot C++ + graphify Python 参照；多仓库/跨语言（TS/Go/Java）未验证。
4. **文档/记忆侧答案质量评测未跑出分**：`run_doc_quality.py`（faithfulness/G-Eval/GraphRAG head-to-head）复刻脚本就绪，**被 BigModel key 持续 429 限流阻塞**——本报告只覆盖「检索召回」层，不含「答案质量」层。
5. **记忆层零量化**：Mem0 Stage 1 未接入 agent，记忆侧评测（recall@k/去重/边界路由）全空。
6. **strict@5 在大 C++ 上失效**：Godot strict@5=0.0（grep）/0.5（BM25）——粒度错配，只能用 broad（类/文件区级）作公平刻度。
7. **概念盲区 15.4% 是硬限**：BM25 救不动的 4 条是「代码不含 query 词」，结构性不可检索，依赖 agent 翻译层。

## 7. 当前价值定位

| 维度 | 量化结论 | 证据强度 |
|---|---|---|
| 代码检索可用性 | broad@5=0.846，+22.3% vs grep | ●●●○（真库×3 路对照）|
| 跨工具 anchoring | 100%（8/8）| ●●●○（端到端实测）|
| 文档检索可用性 | recall@5=0.70 | ●●○○（小 N、子集）|
| 工具选型正确性 | BM25 > semantic > grep（实证修正 design）| ●●●○（3 路量化）|
| 经济性 | $0.22/17 篇，查询零 LLM | ●●●○（实测成本）|
| 答案质量 | **未量化**（卡 429）| ○○○○ |
| 记忆层价值 | **未量化**（未接入）| ○○○○ |

**总判断**：当前已量化的价值集中在「**检索召回 + 跨工具定位 + 工具选型**」三层，证据较硬；「答案质量」与「记忆层」两层尚无数据。项目处于「**核心命题已证、量化地基已铺、上层（答案质量/记忆/规模化）待封顶**」的阶段。

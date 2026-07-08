# Godot 文档侧基线发现 · graphify.query × Godot docs subset

> task 3.1/3.2/3.4。17 篇 Godot .rst（tutorials/math 全量 + scripting 节点/信号/生命周期/资源/单例）
> 经 graphify + BigModel glm-4.6 建图：72 节点 / 32 边 / 40 社区 / 3 超边，~$0.22。
> `python -m eval.run_doc_baseline`。

## 数字（n=10 概念查询，gold = 建图实测节点 label）

| recall@1 | recall@3 | recall@5 | recall@all |
|---|---|---|---|
| 0.217 | 0.6 | **0.70** | 0.833 |

lockfile：`graphify 0.8.46 · BigModel glm-4.6 · 17 rst 子集 · query 本地 BFS 不调 LLM`。

## 亮点：graphify 自动从 NL 选对起始节点

- `vector normalization and dot product` → graphify 自选起始 = `['Dot Product','Vector Normalization','Vector2 Class']`，**三个 gold 全部命中起点**。
- `how do nodes communicate with signals` → 自选 `Signals Concept` 起点，命中。
- NL→图节点的映射 graphify 做得很好（无需 agent 预翻译，与 cmm 那侧的 pathfinding 死穴不同）。

## 漏的点（recall@all<1，共 3/10）

| query | 漏的 gold | 根因 |
|---|---|---|
| node lifecycle ready callback | `_ready Callback` | BFS 从 Node Class 出发 depth2 到不了 _ready（**方法节点没和概念节点连边**）|
| attach child node get node path | `add_child Method`、`get_node Method` | 同上——方法节点未被选作起点、也未从 Node 连边可达 |
| bezier curve path | `Cubic/Quadratic Bezier Curve` | 概念细分节点未被选作起点 |

**共同根因：抽取建图时「方法/回调节点 ↔ 其所属类/概念节点」的边偏弱**，导致 BFS 从概念节点出发到不了方法节点。→ 可行动的图质量改进项：抽取 prompt 强化"方法必须连到所属类"。

## KB Godot 双轨现状（凭据墙破后）

| 轨 | 工具 | recall@5 | 备注 |
|---|---|---|---|
| 代码 | cmm BM25 | **0.846** | broad（类区级）|
| 文档 | graphify query | **0.70** | BFS 图遍历 |

→ 项目核心命题「KB 在真实 Godot 上可用」**双侧都被真数据验证**。

## 方法学边界
- 子集 17 rst（非全量 godot-docs ~3000 页）；gold = concept 节点级（方法节点偏弱是已知）。
- 检索仅 graphify query（BFS）；`path`/`explain` + cmm↔graphify 跨工具 anchoring 留待后续。
- 凭据：复用环境 BigModel key（runbook B 已沉淀配置）。

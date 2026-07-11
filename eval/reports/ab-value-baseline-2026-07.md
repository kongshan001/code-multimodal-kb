# Agent A/B 价值 Benchmark 报告 · 2026-07-11（Stage 0 token 代理）

> 本报告量化"配备 vs 不配备代码 KB"对 agent 任务的**端到端价值差**——回答"这套系统到底有没有用"。
> 属 `add-evaluation-baseline` §6（agent 层），与既有检索层 benchmark（recall@k）互补。
> 数字来自归档 JSON `reports/archive/20260711T110417Z-ab-value-stage0-godot-stage0.json`
> （`bench run ab` 实跑，零手算），可由 `eval/run_ab_value.py` 复现。

## 0. 命题与口径

| 项 | 值 |
|---|---|
| 命题 | 同一代码库，agent 配 cmm 代码 KB vs 朴素 grep，干同一批活的 context 成本与命中差 |
| 题集 | `gold_godot` 26 条代码定位题（Godot core/，符号 gold，零 LLM 判分） |
| Arm A baseline | 朴素检索：`grep -rli <query>` 列文件 + 读 top-3 文件（每文件 4000 chars 截断）|
| Arm B KB | cmm `search_graph` bm25 top-5（我们的代码 KB 注入的 context） |
| lockfile | `cmm 0.8.1 · 零 LLM · char/4 token 估算` |

> **Stage 边界**：本报告是 **Stage 0 token 代理**——只证"KB 省 context token + 注入更准"，
> **不证 agent 答得更对**（后者是 Stage 1，需 LLM key 跑 agent loop，env 当前无 key，凭据门控）。

## 1. 核心结果

```
                         KB 臂        朴素 grep 臂      差距
mean 注入 token           195          1750 (读文件)     KB 省 ~12.7× context
mean 压缩比（naive/KB）    —            —                12.71×（中位 15.5×，max 18.4×）
kb_hit@5（注入含 gold）   0.846        —                 与检索层 broad@5=0.846 一致
grep 盲区（0 命中）        —            7/26 = 27%        KB 救回其中 5 条
```

**一句话价值**：回答同一道代码定位题，代码 KB 用 **~195 token** 就把答案符号注入 top-5
（命中 84.6%）；朴素 grep 要么**读 ~1750 token** 才覆盖同样信息（中位贵 15.5×），要么对
**27% 的概念题完全打空白**（grep 返 0 文件）——而 KB 还能救回其中 5/7。

## 2. Token 用量差（用户诉求 ①）

| query | KB 注入 | 朴素 grep+读 | 压缩比 |
|---|---|---|---|
| `rect2` | 163 t（hit ✓） | 3000 t | **18.4×** |
| `vector3` | 166 t（hit ✓） | 3000 t | 18.1× |
| `color` | 295 t（hit ✓） | 3122 t | 10.6× |
| **mean (26 题)** | **195 t** | **1750 t** | **12.71×** |

分布：min 4× / 中位 15.5× / max 18.4×。即**每题 KB 平均替 agent 省 ~1500 token 的 context**。
（朴素 grep 的"读文件"按 top-3 × 4000 chars 截断，是 naive-RAG 代理；真要全量读 core/ 是百万 token 级。）

## 3. 准确度代理（用户诉求 ②，Stage 0 口径）

Stage 0 不能测"agent 终答对不对"（需 Stage 1 的 LLM run），但能量化**注入精度**：

- **kb_hit@5 = 0.846**：KB 注入的 top-5 context 含 gold 答案符号的比例——与检索层
  `broad@5=0.846` 完全一致（同口径），互为印证。
- **朴素 grep 盲区 7/26 = 27%**：概念题（`int to string` / `delete object free memory` /
  `a star pathfinding` / `operating system` / `undo redo` / `translation server` / `http client`）
  grep 返 0 文件——agent 无从下手。其中 **KB 救回 5 条**（a star→AStar、OS、UndoRedo、
  TranslationServer、HTTPClient），剩 2 条（itos / memdelete）KB 也盲（概念词代码里不出现）。

> 这 2 条是代码侧"概念盲区"硬限（见 value-benchmark §2.3），任何检索都救不了，须靠 agent
> NL→关键词翻译层。KB 的价值在**把盲区从 7 条压到 2 条**（救回 5）。

## 4. 效率（用户诉求 ③，Stage 1 完整测）

Stage 0 能给的效率信号：**token-per-relevant-context**——KB 用 195t 拿到命中 context，
朴素 grep 用 1750t 拿到（且 27% 概率拿不到）。完整效率（agent 步数 / wall-clock / token-per-correct）
需 Stage 1 agent loop 实测，凭据门控。

## 5. 诚实边界（引用须注明）

1. **Stage 0 ≠ agent 答对率**：只证"context 省 token + 注入命中"，不证"agent 答得更对"。
   后者是 Stage 1（design §F 已就绪，待 LLM key）。
2. **token 用 char/4 粗估**：Stage 1 用 LLM API 的 usage 字段精确替代。
3. **朴素基线是 naive-RAG 代理**：grep+读 top-3 文件截断，非全量；真 baseline agent 行为更复杂。
4. **Godot 公开 → LLM 训练可能见过**（Stage 1 暴露）：Stage 1 用"朴素检索"非"裸答"基线缓解（design F2）。
5. **仅 cmm 代码 KB 一臂**：graphify 文档 KB / mempalace 记忆对代码定位题贡献小，未含（design F4）。
6. **小 N=26**：首基线，扩到 RepoBench/SWE-Lancer 全量是 scale-up（§2.1）。

## 6. 价值定位

| 维度 | 量化结论 | 证据强度 |
|---|---|---|
| context token 节省 | mean 压缩 12.71×（中位 15.5×）| ●●●○（26 题真跑）|
| 注入命中 | kb_hit@5=0.846（与 broad@5 一致）| ●●●○ |
| 概念盲区收窄 | grep 盲 7→KB 盲 2（救回 5）| ●●●○ |
| agent 答对率提升 | **未量化**（Stage 1 凭据门控）| ○○○○ |
| 端到端效率（步数/耗时）| **未量化**（Stage 1）| ○○○○ |

**总判断**：Stage 0 用零 LLM 实测坐实了"代码 KB 在 **context 经济性**上有量级优势"（省 ~12.7× token），
且把朴素检索的概念盲区从 27% 压到 8%。"配 KB 是否让 agent **答得更对**"这一最终命题，待 Stage 1
LLM 凭据到位后跑全 agent A/B 封顶。

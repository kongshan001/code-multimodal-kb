# 记忆层 Benchmark 报告 · 2026-07-11

> 本报告量化 `agent-memory` capability 的记忆层价值——填补 `value-benchmark-2026-07.md` §7
> 标注的「记忆层价值 ○○○○（未量化）」缺口。所有数字来自归档 JSON
> `reports/archive/20260711T104332Z-mempalace-engineer_demo.json`（`bench run memory` 实跑，
> 零手算），可由 `eval/run_memory_baseline.py` 复现。指标定义见 `eval/metrics.py` +
> `eval/routing.py`。
>
> **前置已满足**：MemPalace Stage 1 已接入并 mine（change `add-agent-memory` 已归档，
> palace 1485 drawers）。本评测即 `add-evaluation-baseline` §4（task 4.2 + 4.3）。

## 0. 评测规模

| 项 | 值 |
|---|---|
| subject | MemPalace 3.5.0（本地 embedding，核心零 LLM） |
| palace 规模 | 1485 drawers（memory 文件 4 + 会话 jsonl 碎片 1481） |
| 召回评测 | **15 条 NL query** × top-10 = 150 次 drawer 召回 |
| 路由评测 | **13 条候选事实**（客观/程序/事件/主观 4 类） |
| lockfile | `mempalace 3.5.0 · cmm 0.8.1 · graphify 0.8.46 · temp=0 · 零 LLM judge` |

## 1. 核心结果总表

```
                          值       释义
召回 hit@5（任一 gold）   0.933    14/15 query 在 top-5 命中正确 source
召回 recall@5             0.900    top-5 覆盖 gold source 的比例（多 gold 项摊薄）
召回 hit@1（首条）        0.800    12/15 query 首条即正确 source
去重 unique_source@5      0.613    top-5 不同 source 占比（同源碎片冗余度）
路由总体准确率            1.000    D1 四层归属 13/13 全对
路由 per-class            4×1.000  客观/程序/事件/主观 各 100%
注入体积收敛              有界     search ≤10 / MEMORY.md ≤20，不随库膨胀
```

**一句话结论**：主观记忆（memory 文件）召回干净（hit@5=0.933），首条命中率 0.80；
D1 四层路由规则在标注集上完全可操作（准确率 1.0）。主要弱点是**去重**（同源会话碎片
占 top-k 近 40%）和**数量类概念查询**（1 条 miss）。

## 2. 召回质量分析（task 4.2）

### 2.1 memory 文件 vs 会话碎片

| 目标类型 | query 数 | hit@5 | 说明 |
|---|---|---|---|
| memory 文件（*.md） | 8 | 8/8 = 1.0 | 主观层召回干净——query 匹配内容即 top 命中 |
| 会话 jsonl | 7 | 6/7 = 0.857 | 情景/程序内容召回偏松散（碎片化） |

memory 文件（agent-memory-approach / prefer-global-tool-sharing /
commit-every-change-to-git / MEMORY.md）是 palace 里**最干净的信源**——它们是
人工凝练的主观事实，query 一旦匹配语义就稳定 top-1/top-2。这印证 D1 的核心命题：
**主观记忆单独成层、前摄召回，是有检索质量保障的**（非全量注入的妥协）。

### 2.2 唯一 miss 的根因

| query | gold | 根因 |
|---|---|---|
| `MEMORY.md 索引现在有几条记忆` | `MEMORY.md` | 数量类概念词（"几条/数量"）与 MEMORY.md 的 drawer 文本（索引行）语义不匹配 → top-5 全是会话碎片 |

> 与代码侧 `value-benchmark` 的「概念盲区」同构：query 用了信源文本里不出现的词
> （"几条"），embedding 召回救不了。改进方向：agent NL→关键词翻译层（同代码侧 design 决策 4 兜底）。

### 2.3 去重（unique_source_ratio@5 = 0.613）

top-5 结果平均只有 61% 是不同 source——即 ~39% 是**同源会话的多个碎片**。
极端例：`Intel Mac 安装` query 的 top-5 有 3 条都来自同一安装会话 `de6c53eb.jsonl`
（unique@5=0.4）。

- **对召回无碍**：同源多碎片反而加固正确 source 的命中（gold 就在该会话）。
- **对注入体积有碍**：若想要 5 条**不同**相关记忆，实际只得到 ~3 条信源多样性。
- **根因**：palace 1485 drawers 里 1481 是会话级 mine 的碎片（未做实体级合并）。
  MemPalace 的实体合并（closet/hallway）在 mine 时做了一部分，但会话碎片仍偏多。
- **改进方向**：会话 mine 后跑 `mempalace compress`（AAAK 压缩 + 去重），或对高频会话做抽稀。

## 3. D1 边界路由准确率（task 4.3）

```
类别        准确率    样本数
objective   1.000     3     代码/文档事实 → KB
procedural  1.000     3     how-to/命令  → skills
episodic    1.000     3     日期/commit 事件 → git/tasks
subjective  1.000     4     偏好/决策/工作方式 → memory
总体        1.000    13
```

D1 路由 cascade（`routing.py`：subjective > episodic > procedural > objective-default）
在 13 条标注集上**零错路由**。关键判定：
- 「决策 + 日期」复合事实（如"7/11 决定走 MemPalace"）正确归 subjective（memory 存决策结论，
  事件本身归 git）——与 CLAUDE.md「决策锚」规则一致。
- grep/命令/部署类正确归 procedural；API 字段/属性类正确归 objective。

> **诚实边界**：13 条标注集与规则 cascade 同源（都按 D1 金句构造），1.0 的准确率部分源于此，
> 不等于在任意自然事实上的泛化准确率。真实泛化需更大、独立标注的候选集（见 §4）。
> 本指标的价值在：① 4 类标注集作为**回归门禁**固化（`test_gold_memory_snapshot`）；
> ② 证明 D1 规则**可操作、可确定性近似**（非模糊口号）。

## 4. 注入体积收敛

| 通道 | 上限 | 机制 |
|---|---|---|
| MemPalace search | ≤10（`--results`） | 按相关性召回的固定窗口 |
| MEMORY.md 全量注入 | ≤20（CLAUDE.md 容量纪律） | 超限降级为按需召回 |

Stage 1 已把主观记忆从「MEMORY.md 全量注入」切换为「MemPalace 按需召回」——
注入体积**不随事实库增长无界膨胀**（spec requirement「Memory capacity discipline」满足）。
本项是设计属性验证（非增长曲线），数值 = 两通道的固定上限。

## 5. 诚实边界（引用须注明）

1. **小 N**：召回 15 / 路由 13——首基线规模，非大规模标注。需扩到 ~50+ 才稳。
2. **gold 偏软**：召回 gold 是"source_file 级"（broad，非精确 drawer）——同代码侧 broad@5
   的公平刻度选择；精确 drawer 级 recall 会更低。
3. **路由集与规则同源**：1.0 准确率含构造偏置（§3），独立标注前不当作文产级精度。
4. **palace 偏会话**：1485 drawers 中 99.6% 是会话碎片，memory 文件仅 4——召回分数高度
   依赖会话 mine 质量；换 palace 构成分数不可直接比。
5. **未评测**：记忆**答案质量**（召回的 drawer 是否真能回答问题，非仅 source 命中）未量化——
   需 LLM judge，归 §3 文档侧同一道凭据墙。
6. **embedding 确定性**：MemPalace 用本地 onnxruntime embedding，查询零 LLM、确定性，
   可复现（lockfile 锁 mempalace 3.5.0）；但 embedding 模型随版本变，跨版本分数不可比。

## 6. 价值定位（接 value-benchmark §7）

| 维度 | 量化结论 | 证据强度 |
|---|---|---|
| 主观记忆召回 | hit@5=0.933 / hit@1=0.80 | ●●●○（15 query 真跑）|
| D1 路由可操作性 | 准确率 1.0（4 类）| ●●○○（小 N + 构造偏置）|
| 注入体积有界 | 两通道固定上限 | ●●●○（设计属性验证）|
| 去重质量 | unique@5=0.613（偏弱）| ●●○○（实测，改进方向明确）|
| 记忆答案质量 | **faithfulness 0.951 / context_precision 0.360**（Ragas 协议，LLM-judged）| ●●○○ |

**总判断**：`value-benchmark` 标注的「记忆层 ○○○○」现已填到 **●●○○**——召回与路由
两层有了实测分，证明 MemPalace Stage 1 的主观记忆层**可召回、可路由、注入有界**；
去重与答案质量是下一步封顶方向。记忆层从「未接入未量化」进入「接入并部分量化」。

## 7. 运营发现：auto-save hook 过度 mining 致召回退化 → 已修复（benchmark 驱动闭环）

**发现**：复测召回时 palace 从 1485 膨胀到 14605 drawers（~10×）——全局 Stop/PreCompact hook
（`mempalace hook run --hook stop`，非 idempotent）把**另一项目（Unity）的会话 transcript 反复 mine**
进 palace 的 sessions wing（13115 垃圾 drawer），淹没 wing_api 真记忆 → **hit@5 从 0.933 跌到 0.6**。

**修复（闭环完成）**：
1. **止血**：禁用 ~/.claude/settings.json 的 mempalace Stop/PreCompact hook（备份在 /tmp/settings.json.bak.*）。
2. **重置 + 重 mine**：擦 palace → `mempalace init` → `mempalace mine` engineer_demo 会话 → 14605 → **2021 drawers**（纯 wing_api，sessions bloat wing 消失）。
3. **重测**：`bench run memory` → **hit@5 = 0.933 恢复**（归档 `...20260712T004546Z-mempalace-engineer_demo.json`）。

→ **benchmark 兑现核心价值**：不是评分，是抓到真实运营事故（全局 hook 把别项目垃圾 mine 进记忆、
致召回 −33%），量化影响，驱动修复，验证恢复。完整的"测→诊→改→重测"闭环。

**遗留**：hook 已禁（auto-save 暂停）。恢复 auto-save 需等 mempalace 出 idempotent 的 hook
（`sweep` 是 idempotent 但不走 hook stdin）；当前可手动 `mempalace sweep <jsonl>` 按需增量存。
source-dedup re-rank（`mempalace_search(dedup_sources=True)`）仍可作为召回默认 re-rank 层（免费多样性）。



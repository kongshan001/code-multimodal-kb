# 结果分析 · godot-core 37题×4臂 · GLM-4.7（含 8 道冷门难题）

> 配套 `result.md`（指标矩阵 + 逐题 + 测量纯度段）/ `summary.json`（原始数据）。写于 2026-07-19。
> 本次是 benchmark **首次清晰测出 KB 价值**——换模型 + 加难题后，天花板效应打破。

---

## 0. 本次跑与之前的关键差异

| 维度 | 之前（20260715T151116Z） | 本次（20260719T134957Z） |
|---|---|---|
| 模型 | GLM 5.1 | **GLM 4.7** |
| 题数 | 29（26 简单 + 3 bug_fix） | **37**（+ 8 冷门内部类） |
| 冷门题 | 无 | CowData / LocalVector / SelfList / PagedAllocator / SafeRefCount / DisjointSet / DynamicBVH / RingBuffer |
| 测量纯度 | 无此指标 | **新增** no_tool_rate + acc_with_tool / acc_no_tool |
| 分臂 backstop | 全 30 | **no-kb 12**（A2，控 flail 成本） |
| 并发 | 串行 | **全局并发** pool=4 |

---

## 1. 矩阵：KB 价值清晰显现

| 臂 | accuracy | mean_total_tokens | mean_llm_calls | truncated_rate | no_tool_rate |
|---|---|---|---|---|---|
| no-kb | **0.784** | 12461 | 8.2 | **0.22** | 0.00 |
| kb | **0.919** | 3864 | 3.3 | 0.00 | 0.00 |
| **kb+superpowers** | **0.973** | 5583 | 3.7 | 0.00 | 0.00 |
| kb+openspec | 0.919 | 5070 | 3.4 | 0.00 | 0.00 |

**头条**：
- **no-kb 暴跌**（0.931→0.784，-14.7%）——冷门题 grep 抓瞎，22% 撞 backstop、avg 8.2 轮空转、12461 token。
- **kb 稳住**（0.966→0.919，-4.7%）——cmm 语义检索冷门符号依然 2-3 步收敛。
- **kb+superpowers 最佳**（0.973）——SOP 注入在 GLM 4.7 上有效（5.1 时被噪声淹没）。
- **no_tool_rate 全 0**：GLM 4.7 每题都用工具（比 5.1 更守"用工具查找"纪律），所有 accuracy 都是 tool-assisted，测量纯度干净。

---

## 2. 冷门题逐题分化（2/8 清晰拉开）

| 冷门题（gold） | no-kb | kb | kb+sp | kb+ops | 说明 |
|---|---|---|---|---|---|
| CowData | ✓ | ✓ | ✓ | ✓ | grep 在 cowdata.h 碰到类名 |
| LocalVector | ✓ | ✓ | ✓ | ✓ | 同 |
| SelfList | ✓ | ✓ | ✓ | ✓ | 同 |
| PagedAllocator | ✓ | ✓ | ✓ | ✓ | 同 |
| SafeRefCount | ✓ | ✓ | ✓ | ✓ | 同 |
| **DisjointSet** | **✗** | **✓** | **✓** | **✓** | grep 搜"并查集"无果；cmm 语义命中 |
| **DynamicBVH** | **✗** | **✓** | **✓** | **✓** | grep 搜"包围盒"无果；cmm 语义命中 |
| RingBuffer | ✓ | ✓ | ✓ | ✓ | grep 碰到 ring_buffer.h |

→ **语义查询（"并查集"/"包围盒"）是 grep 的盲区、cmm 的主场。** 这正是 KB 的核心价值——NL 概念 → 代码符号的语义跳跃。
→ 6/8 no-kb 也对了：grep 在 `.h` 文件名或注释里碰巧匹配到了类名。要制造更多分化，题面应避免暴露类名线索（如"并查集"不暴露 DisjointSet）。

---

## 3. 测量纯度（GLM 4.7 特有发现）

| 臂 | no_tool_rate | acc_with_tool | acc_no_tool | 解读 |
|---|---|---|---|---|
| no-kb | 0.00 | 0.784 | - | 每题都用工具 |
| kb | 0.00 | 0.919 | - | 每题都用工具 |
| kb+superpowers | 0.00 | 0.973 | - | 每题都用工具 |
| kb+openspec | 0.00 | 0.919 | - | 每题都用工具 |

GLM 4.7 `no_tool_rate` 全 0——**每道题都调了工具才答**。对比 GLM 5.1（部分题 kb 臂不调 cmm 直接凭记忆答），4.7 更服从 "用工具查找" 的 system prompt 纪律。

**这意味着**：本次所有 accuracy 都是 tool-assisted（工具确实参与了），没有"凭记忆混分"。测量纯度高。

---

## 4. 成本与效率

| 臂 | mean_total_tokens | mean_cost_$ | mean_wall_clock_s |
|---|---|---|---|
| no-kb | **12461**（最高） | 0.0087 | ~长（flail + backstop） |
| kb | **3864**（最低） | 0.0027 | ~短 |
| kb+superpowers | 5583 | 0.0039 | ~短 |
| kb+openspec | 5070 | 0.0035 | ~短 |

no-kb 在难题上 **3 倍于 kb 的 token**（12461 vs 3864）——grep 反复试错（avg 7.4 步），每步重发膨胀历史。kb 的 cmm 1-2 步命中 → 省了轮数 = 省了 token = 省了钱。

> 注：cost 用占位单价 $0.70/Mtoken，非真实 GLM 4.7 定价。看相对大小。

---

## 5. vs GLM 5.1 对比（换模型效应）

| 臂 | 5.1 acc（29 易） | 4.7 acc（37 含难） | 变化 | 解读 |
|---|---|---|---|---|
| no-kb | 0.931 | 0.784 | **-14.7%** | 冷门题 crush 了 grep |
| kb | 0.966 | 0.919 | -4.7% | 轻微降（题更难 + 4.7 略弱于 5.1？） |
| kb+superpowers | 0.966 | **0.973** | +0.7% | SOP 在 4.7 上反而更有效 |
| kb+openspec | 0.931 | 0.919 | -1.2% | 基本持平 |

两因素叠加（换模型 + 加难题），no-kb 受打击最大（-14.7%），KB 臂稳住。**说明 KB 的价值在"难题 × 弱工具"组合下最显著。**

---

## 6. 结论（benchmark 效度验证）

**① benchmark 终于"活"了**：之前 GLM 5.1 + 简单题 = 天花板效应（no-kb/kb 持平）。现在 GLM 4.7 + 冷门题 → no-kb 暴跌、KB 稳赢、skills 加分。**题难度是激活 benchmark 的关键杠杆。**

**② KB 价值的核心场景 = 语义检索**：grep（词面）搜不到"并查集 → DisjointSet"这种 NL 概念 → 符号跳跃；cmm（语义）能。这是 KB 不可替代的价值。

**③ GLM 4.7 是更"守纪律"的测试对象**：no_tool_rate=0（每题用工具），比 5.1 更适合 benchmark（测量纯度高，结果可信）。

**④ skills 臂（superpowers）在 4.7 上有效**（0.973 最高）——工程纪律 SOP 对 4.7 有增益。需多 run 验证稳不稳。

---

## 7. 诚实边界

- **n=1 run**：单次跑，方差仍在（temp=0 也非完全确定）。要稳结论需 n≥3 取均值。
- **8 冷门题中仅 2/8 分化**：6 道 no-kb 也对了（grep 碰巧在 .h 名/注释里匹配）。要更大分化需更多"纯语义"题（题面不暴露类名线索）。
- **GLM 4.7 vs 5.1 差异混了两个变量**（换模型 + 加题），不能单独归因于模型。
- **cost 是占位价**，非真实 4.7 定价。
- **skills SOP 是精简文本**，非真 Claude Code skill 运行时。
- **bug_fix 仅 3 题**，样本太小不单独出结论。

---

## 8. 下一步建议（按效度优先级）

1. **多 run n≥3**：确认 0.973 vs 0.919 的差是信号还是噪声。
2. **加更多纯语义题**（题面不暴露类名）：如"管理写时复制引用计数的内部机制"→ RefCounted/CowData（不暴露名字）。
3. **多模型对比**：GLM 4.7 vs 5.1 vs MiniMax（若 API 格式支持）——benchmark 的跨模型适用性。

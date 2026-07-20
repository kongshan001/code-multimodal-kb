# ab_agent 优化路线图

> 基于 `docs/ab-agent-internals.md` 的源码分析整理。按 **影响×可行性** 排，标注状态。
> 维护：推进一项就改状态；新增优化项追加到对应分组。

状态图例：✅ 已完成 · 🚧 进行中 · ⬜ 待办 · ❌ 否决（附理由）

---

## A. 成本 / 效率

| 项 | 状态 | 说明 |
|---|---|---|
| **A2 分臂 backstop** | ✅ | no-kb（grep 易空转）降到 12，卡死早停省 token。`config.agent.max_steps_by_arm` |
| **A1 截断喂模型的 tool_result** | ❌ | 会切 gold（关键信息可能在被截段）——且 stuck 成本主因是轮数不是单结果大，杠杆错 |
| A3 重复 tool 调用早停 | ⬜ | 同 grep pattern 连调 N 次→大概率卡了，提前停（次优先，backstop 已兜底） |

## B. 效度（数字可不可信）

| 项 | 状态 | 说明 |
|---|---|---|
| **测量纯度：no_tool_rate + acc split** | ✅ | 报告标"没调工具就答"的题——KB 贡献只在 acc_with_tool 里。`_aggregate` 加 3 指标 + result.md 专段 |
| **B1 多 run n≥3 取均值** | ⬜ | 治"方差>臂间差"根本病（同题两次跑 acc 洗牌）。并行+降本后可负担。**最高优先** |
| **B2 加难题集** | ✅ | 加 8 道冷门内部类（CowData/LocalVector/SelfList/…），GLM 4.7 跑出 KB 分化（no-kb 0.784 vs kb 0.919） |
| B3 报告标 n / 方差 / token 分项 | ⬜ | 矩阵列 input/output/cache 分项 + 标 n（多 run 后才有方差） |
| 判分严格度 | ⬜ | broad 子串可能误中；可加 strict 或 LLM-judge 交叉校（但有 self-preference） |

## C. 覆盖（测得准不准）

| 项 | 状态 | 说明 |
|---|---|---|
| `read_file` 分页/offset | ⬜ | gold 可能在文件深位（现 read_cap=2000 截断漏）；加 offset 让 agent 翻后面。token 会涨，需权衡 |
| cmm 空结果兜底 | ⬜ | q18 类：cmm 返空→模型硬猜错；空时引导重查或退 grep |

## D. 公平性（sdk vs raw A/B 严谨）

| 项 | 状态 | 说明 |
|---|---|---|
| C1 对齐 temperature | ⬜ | raw 显式 temp=0；sdk 走默认（未知）→ A/B 不公平。sdk 设 temp=0 |
| C3 对齐 cost 口径 | ⬜ | sdk cost=total_cost_usd(cache 折价)；raw=_cost 全价 → 两 engine cost 不可直接比 |
| C2 对齐 thinking | ⬜ | sdk 默认带、raw 不请求（证过不改收敛，次要） |

## E. 速度 / 工程

| 项 | 状态 | 说明 |
|---|---|---|
| **全局并发（跨题跨臂）** | ✅ | 所有 (题×臂×run) 进同池，as_completed，无每题 barrier。pool=4，~2.2× 加速 |
| pool 调大（6-8） | ⬜ | 端点不限流可再提速；429 风险，先试 6 看稳不稳 |
| D1 缩小 `except Exception: pass` | ⬜ | `_consume` 吞所有异常（max_turns/网络/解析）→ 真 bug 被藏；只接 max_turns，其余记日志 |
| `run()` 老路径并行 | ⬜ | 跟 run_compare 一致（次要，少用） |

## F. 不建议做（避免过度工程）

- 强行对齐 `llm_calls` 两 engine 口径（差 ≤1，无意义）。
- 给卡死题上 force-answer（已选 run-until-answer，别回退）。
- 给 raw 复刻 thinking/caching（抹平了反而失去对照基底）。
- 给 sdk 复刻 raw 的手搓 messages（失去 SDK 价值）。

---

## 推荐下一步

**B1 多 run n≥3** 是剩下最高价值的——它是"数字可不可信"的根本，且并行+降本后跑得起了。
但 B1 的前提是**题集值得多跑**：若不先做 **B2 加难题**，多 run 只是更精确地测"模型本就会的题"。

所以两条路：
1. **求稳**：先 B1（多 run）确认现有结论稳不稳 → 再 B2（加题）。
2. **求效**：先 B2（加几道难题）→ 再 B1（多 run 测它）。

倾向 **路径 2**（加题优先）—— 否则多 run 投入的信号还是天花板噪声。

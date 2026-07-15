# 结果分析 · godot-core 29题×4臂（claude_agent_sdk 首跑）

> 配套 `result.md`（指标矩阵+逐题）/ `summary.json`（原始数据）。本文记录**围绕这次跑的调研与结论**，
> 多数结论有对照实验/逐题实锤支撑，标注了证据等级。写于 2026-07-15。

## 0. 背景

`ab_agent` 的 agent loop 从手写 ReAct（直连 anthropic SDK）迁到 `claude_agent_sdk`（claude CLI 封装），
见 openspec change `migrate-ab-agent-to-claude-sdk`。本次是该迁移后的**第一个全量 benchmark**。
本文回答三个问题：① 迁移有没有把指标弄脏？② 跟迁移前的旧跑为何差这么多？③ 谁赢、为什么？

---

## 1. 迁移验证：数字可信（核心结论）

迁移最大风险是 **CLI 默认工具定义带来的 token 税**（spike 实测默认 22-40k input token/episode）会淹没
token/cost 指标。本次 116 episode 实跑：

- 全臂 `mean_total_tokens` = **1015–1542**，无一窜回 22-40k → D7 最小配置（`tools=[]` + `setting_sources=[]`）
  在规模上守住。**token 税风险未发生。**
- trace 字段逐一对齐迁移前契约；`episode.json` 完整（顺手修了既有 null bug，见下）。
- 79/79 pytest 绿。

> 顺手修的既有 bug：`agent_compare_report._clean_episode` 函数体为空（body 误漂进下一个函数 return 后成死代码），
> 导致所有历史 `episode.json` 落 `null`。本次修复 + 加 regression 断言。**非迁移引入**，但堵在 trace 落盘路径上。

**结论：本次数字是可信的测量，测量引擎没被换 SDK 弄脏。**

---

## 2. 跟迁移前旧跑的"巨大差距"——是伪差距

旧跑（commit `63ab3ef`，2026-07-14）vs 本次：token 掉 3-7×、步数掉 2-4×、准确率升、截断几乎消失。
乍看像"SDK 把 agent 升级了"。**两个因果假设都被对照实验否掉**（教训：看相关 ≠ 因果）：

| 假设 | 对照实验 | 结果 |
|---|---|---|
| ① thinking 默认开了，agent 变聪明 | 同题拨 thinking on/off | ❌ 都是 1 tool_call / 2 轮收敛，行为没变 |
| ② 旧 loop 天生 thrash | 重建旧 loop 跑同题 | ❌ 也是 1 tool_call / 2 轮收敛，没 thrash |

**真因**：旧跑本身就是个 **n=4 的开发期 pilot**（commit 自述"验证 trace 捕获"），不是基准：
- 每题方差极大（1–13 步；一题炸到 21816 token），n=4 让 1-2 题 thrash 就把均值拉飞。
- thrash 不是 agent 能力差（已证旧 loop 重跑同题也 1 步收敛），是**特定题目 + API 非确定性 + 小样本**。
- token 差是机械结果：旧 pilot 一些题跑 4-13 步、每步重发膨胀历史且无缓存 → 4k-21k token；本次 1-2 步 + 缓存 → ~1k。

**结论：没有"agent 能力跨越式提升"这回事。旧 n=4 pilot 不可作 baseline，本次是首份可信测量。**

---

## 3. 谁赢、为什么——no-kb 在这套题上真赢（实锤）

| 臂 | accuracy | tokens | cost |
|---|---|---|---|
| **no-kb** | **0.931** | 1164 | $0.0072 |
| kb | 0.862（最低） | 1091 | $0.0084 |
| kb+superpowers | 0.897 | **1015** | $0.0089 |
| **kb+openspec** | **0.931** | 1542 | $0.012 |

反直觉：**纯 kb 准确率最低，no-kb 并列最高且最省。** 逐题查 kb 输、no-kb 赢的两题，机制清楚：

- **q1「字符串格式化底层函数」（gold=`vformat`）**：cmm 返回 `String.format`+`format_number`（语义上"最像 format"
  的高层方法），**没返真正的底层 `vformat`** → kb 止步于浅答案 `String::format` ✗。no-kb grep "format" 捞到含
  vformat 的文件，read 后挖到 `vformat` ✓。
- **q18「引擎主类」（gold=`Engine`）**：cmm **返回空** → kb 硬猜 `Main` ✗。no-kb **一次工具没调**，凭训练知识答
  `Engine` ✓。

**机制**：题太简单（26/29 是"X 用哪个类"，glm 训练里就懂 Godot）。这种题上 cmm 反而帮倒忙——返**显眼但非最深**
的答案（模型止步），或返**空**（模型"查过了"就硬猜，比纯凭记忆还差）。grep/no-tool 让模型自己的知识占上风。

**这不等于 KB 没用**：KB 的价值要在"模型不会"的难题上才显现（cmm 找回模型回忆不起的符号）。本套题 90% 是模型会的，
KB 既没空间帮忙、又有空间误导。3 道 bug_fix 才是真分化点（q27 全跪、q28 仅 openspec 救回）。
**要测出 KB/skills 价值，得换更难/更冷门的题集——这是出题层面的下一步。**

---

## 4. 截断机制（本次跑之后已改为 run-until-answer）

**截断率怎么算**（`agent_compare_report.py:39`）：`truncated_rate = 该臂 truncated=True 的题数 ÷ 总题数`；
单题 `truncated` = 主 query 跑满 backstop 仍未自然给出答案。

**本次跑之后的行为变更**（应你要求"不考虑截断、跑到出答案为止"）：
- backstop 从 8/12 轮抬到 **30 轮**（仅作防死循环安全网，正常题远在此之前自然收敛）。
- **去掉 force-answer**：不再 inject 猜测答案。跑满 30 轮还没答 = 真卡住，`answer` 留占位、判分即错。
- 于是 `truncated_rate` 衡量的是 **agent 真正卡死的比例**，不是被人为步数上限截断。
- 代价：极少数原本靠 force-answer 猜对的题会变错（更诚实）；30 轮 backstop 极少触发，成本可控。

> 本次报告（`result.md`/`summary.json`）仍是旧机制（force-answer）下跑的；下次重跑将采用 run-until-answer。

---

## 5. 诚实边界

- **n=1 run**：每题每臂只跑 1 次。temp 即便 0，API 也非完全确定（见 §2）。要稳结论需多 run 取均值。
- **判分 broad 子串**：gold 符号 alnum 子串命中即对，可能放过"答非所问但含符号"的误中。
- **题集偏简单**：90% code_retrieval 是模型会的 → KB/skills 的准确率加分 marginal（见 §3）。
- **bundled SOP 非 skill 运行时**：skills 臂注入的是精简 SOP 文本，不是真 superpowers/openspec 运行时。
- **cost 是占位价**：token × 占位单价，看相对不看绝对。
- **glm-5.1 经此端点不返独立 thinking block**：`thinking` = agent 推理文本，非隐藏思维链。

## 6. 下一步建议（按性价比）

1. **加难题集**（最高性价比）：增加 bug_fix / 冷门符号题，让 KB 有空间发挥——否则永远测不出 KB 价值。
2. **多 run 取均值**（n≥3）：压住 API 非确定性，§2 的"方差"才不会污染结论。
3. 用本次新行为（中文题 + run-until-answer）重跑一份，作为新基线。
4. 归档 openspec change `migrate-ab-agent-to-claude-sdk`。

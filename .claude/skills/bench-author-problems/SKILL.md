---
name: bench-author-problems
description: 出题 → AI 审核 → 人工确认 → 入库 → 跑多臂对比 benchmark → 出目录报告，一条龙。给目标工程造测试题（code_retrieval 自动 + bug_fix 手动），过两层 AI 审（实证 ambiguity + 独立 subagent 语义匹配），人工 approve 入库，跑 4 臂（no-kb/kb/kb+superpowers/kb+openspec）对比，产出含结论+执行过程+会话+思考的目录报告，量化"KB 值不值"和"软件开发 skills（superpowers/openspec）值不值"。用户说"给 X 工程出题并对比 skills"、"测 superpowers/openspec 的价值"、"出题→审→跑 benchmark→报告 一条龙"、"我想看有 skills 和没 skills 的 agent 差多少"时触发。纯对接目标工程（建 target/索引）用 bench-dock-target；只读已有报告用 bench list-reports。
---

# 出题 → 审 → 对比 → 报告 一条龙

把"我想 benchmark 我的工程 + 看skills 价值"变成：题库建好 + 多臂对比跑完 + 一份人能读的目录报告。前置：目标工程已 dock（有 `eval/targets/<id>/`，见 `bench-dock-target` skill）；本流程在那个 target 上出题 + 跑对比。

## 全流程（7 步）

### 1. 确认 target 已就绪
```bash
python -c "from eval.targets import load; print(load('<id>')['target']['subjects'])"
```
未 dock → 先走 `bench-dock-target`。本流程产出 `code_retrieval` + `bug_fix` 两类题。

### 2. 自动出 code_retrieval 题
```bash
bench goldgen <seed词> --target <id>          # codegraph 挖真符号 + LLM 拟 NL 题（gold=符号，构造即正确）
bench goldgen-verify --target <id>            # 实证审：ambiguity（同名多模块）+ 检索可达，零 LLM
```
候选以 `status: pending` 进 `problems.json`。

### 3. 手动 curate bug_fix 题（关键——给 skills 价值）
**纯 code_retrieval（找符号）上 superpowers/openspec 显不出价值**——它们是"怎么 build/debug/spec"的 SOP，不是检索技巧。要测 skills 价值，必须有 bug_fix 题（需推理定位，非词面查找）。

用 Gold lab 编辑器加 bug_fix（`bench web` → #/goldlab → 选 target → "+ 新增题目" → type=bug_fix）：
- `query` = 真实 bug 描述/复现（需理解控制流才能定位）
- `gold` = `{symbols: [该改的符号], files: [预期文件]}`
- 覆盖 3-8 个不同模块/场景

> 题目质量决定 skills 对比有没有意义。bug_fix 越需推理，skills 越有发挥空间。

### 4. AI 审（两层互补）

**4a 实证审**（已在 2 步跑了，零 LLM）：抓 gold 歧义。

**4b 语义审**（本 skill 的核心新增——独立 subagent 判 query↔gold 语义匹配）**：对每个 `status: pending` 题，spawn 一个独立 subagent 判语义匹配。这步抓实证抓不到的：query 说"数学向量"但 gold=Vector（动态数组，非数学向量）；前提事实错；query 太模糊。固化提示词：

```
你是代码 benchmark 的题库审核员，独立判断一道题的 query 与 gold 是否语义匹配。
题目：type=<type>, query/fact=<text>, gold=<gold>
判断：一个开发者问这个 query，期望的答案是不是就是 gold？
- query 用概念描述时，gold 是不是那个概念对应的真符号/文件/层？
- 有没有前提事实错（query 描述的代码行为不存在）？
- query 是否太模糊（多个 gold 都合理）？
只输出 JSON：{"verdict": "match" | "mismatch" | "ambiguous", "reason": "<一句>"}
默认严格：拿不准 → ambiguous。不要迁就，宁可标 ambiguous 让人审。
```

主 agent（你）用 Agent 工具按上述提示词 spawn subagent，每 pending 题一个（或批量），收集 verdict。把 `mismatch`/`ambiguous` 的题标记给人审重点看（可在 problems.json 加 `semantic_verdict`/`semantic_reason` 字段，或口头汇总）。

### 5. 人工 approve 入库
`bench web` → Gold lab → 逐条审 pending 候选：好的 ✓ approve（status→accepted），差的 🗑 删。重点看 4b 标 mismatch/ambiguous 的。改完记得 `git commit`（前端不自动提交）。

### 6. 跑 4 臂对比
```bash
bench run agent-compare --target <id> --runs 1
```
4 臂：`no-kb` / `kb` / `kb+superpowers` / `kb+openspec`，跑全部题（code_retrieval + bug_fix）。可选 `--subset N`（pilot）、`--arms no-kb,kb`（只测 KB 价值，省 skill 臂）。**会花 GLM 钱 + 时间**——先 `--subset 6` 试水。

> 无凭据/无 anthropic？`--smoke` 用 mock LLM 跑通流水线（产出结构完整但假数据的报告，验管道用）。

### 7. 读目录报告
报告在 `eval/reports/agent-compare/<ts>-<id>/`：
- `conclusion.md`——**先看这个**：谁赢、by 哪指标、诚实边界
- `summary.json`——臂×指标矩阵（accuracy/tokens/llm_calls/tool_steps/wall_clock/cost/tool_diversity + KB压缩比）
- `matrix.md`——可视化网格
- `arms/<arm>/config.md`——这臂工具+注入了哪个 skill（透明）
- `arms/<arm>/episodes/qNN/episode.json`——单题执行过程（逐步 tool）+ 指标
- `arms/<arm>/episodes/qNN/session.jsonl`——完整会话流（本地，gitignore）
- `arms/<arm>/episodes/qNN/thinking.md`——思考过程（本地，gitignore）

**看 skills 价值**：对比 `kb+superpowers`/`kb+openspec` vs `kb` 的 accuracy（skills 帮没帮）+ mean_total_tokens（skills 多花了多少 token）。bug_fix 题上差异最可能显现。

## 诚实边界（报告里也有，重申）

- **skills 臂注入的是 bundled 精简 SOP 文本**（`eval/arms/skills_bundled/`），**非完整 Claude Code skill 运行时**（无触发机制/hook）。headless 可复现近似，**不等于真实 skill 效果**——skills 真实价值可能更高（完整运行时有触发/上下文）。
- **accuracy 由 GLM 生成 + GLM 判分**（同家族 self-preference）→ 相对参考值。
- **bug_fix 仍用 symbol/file broad match 判分**（非修复质量 LLM-judge）——保守刻度。
- 样本量小（几道题）→ 看趋势勿绝对化。

## 命令速查
```bash
alias bench='python -m eval.cli'
bench goldgen <seeds> --target <id>           # 自动出 code_retrieval 题
bench goldgen-verify --target <id>            # 实证审
bench web                                     # Gold lab：手动加 bug_fix + approve pending
bench run agent-compare --target <id> --runs 1   # 4 臂对比 → 目录报告
bench run agent-compare --target <id> --smoke    # mock（无凭据验管道）
```

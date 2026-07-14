## Context

现有 agent 对比（`eval/ab_agent.py` run_episode + `ab_tools.py` 臂注册表 + `run_ab_agent.py` 判分/聚合）只测"有/无 KB"在**代码检索**上，输出单 JSON。用户要：① 加 skills 维（superpowers/openspec）② 多维指标（token/调用次数/耗时/成本/准确率）③ 目录化报告含执行过程+会话+思考。

run_episode 现状（ab_agent.py:83-128）：固定 `SYS_PROMPT`（**硬编码 Godot**——latent bug）；loop 每轮 1 次 `messages.create`（steps=LLM 调用数）+ 累 token + exec tool_use；返回 {answer, input/output_tokens, steps, tool_calls[], tool_texts[], truncated}。判分在 run_ab_agent `_judge`（gold ∈ 终答 broad match）。

约束：零新增依赖；本机无 anthropic → 必须 mock 降级；GLM 走 anthropic 兼容端点（同家族 self-preference）；铁则走 OpenSpec。

## Goals / Non-Goals

**Goals:**
- 4 臂（KB × skills）agent 对比，多维指标，目录化报告（结论+执行+会话+思考）。
- skills 臂通过 system prompt 注入精简 SOP，给 skills 价值可测空间。
- bug_fix 题型让 skills 在比检索难的任务上有发挥。
- 无凭据可 mock 跑通写器+流水线。

**Non-Goals:**
- **不**接 Claude Code 真实 skill 运行时（触发机制/hook）——只注入 SOP 文本（R2 诚实边界）。
- **不**换判分模型（仍 GLM，self-preference 风险保留标注）。
- **不**做 session/thinking 的入库（本地 gitignore，防膨胀）。
- **不**自动 git commit 报告（用户自行提交 conclusion/summary）。
- **不**在本变更做前端 agent-compare 视图（留后续；CLI + 目录报告先行）。

## Decisions

### D1. 4 臂 = 工具集 × skills 注入

```python
ARMS = {
  "no-kb":          {"tools": ["grep_code", "read_file"], "skills": []},
  "kb":             {"tools": ["cmm_search", "read_file"], "skills": []},
  "kb+superpowers": {"tools": ["cmm_search", "read_file"], "skills": ["superpowers"]},
  "kb+openspec":    {"tools": ["cmm_search", "read_file"], "skills": ["openspec"]},
}
```
- `ARMS` 从 `dict[str, list[str]]` → `dict[str, {tools, skills}]`（**BREAKING**，旧臂名 baseline/doc/codegraph 走兼容映射或迁移）。
- skills 内容从 `eval/arms/skills_bundled/<name>.md` 读（仓库 bundle，可复现）。
- 考虑过的替代：跑真实 Claude Code skill 运行时——否决（不可复现、依赖宿主、非 headless）。注入 SOP 文本是 headless 可复现的近似。

### D2. run_episode 6 项改造（grounded 映射）

| # | 改造 | 现状（ab_agent.py） | 改法 |
|---|---|---|---|
| 1 | skills 臂注入 | SYS_PROMPT 模块常量 + 硬编码 Godot | BASE_SYS_PROMPT 去上帝化、目标感知（从 target 读 language/notes）；system = BASE + concat(skill 内容) |
| 2 | llm_calls 显式 | `steps`（每轮1次create）隐含 | 输出 `llm_calls=steps`；`tool_steps=len(tool_calls)` |
| 3 | wall_clock_s | 无 | `time.time()` 包 episode |
| 4 | cost_$ | 无 | `MODEL_PRICES`（glm-5.x $/Mtoken）× token；未知 null+note |
| 5 | session 消息流 | `messages` 建了没返 | 序列化每轮 {role, content(text/tool_use/tool_result)}；tool_result 截断 top-N |
| 6 | thinking（模型无关） | 只抽 text block | 抽 thinking block；有则进 thinking，无则 fallback 本轮 text |

输出扩展：`{answer, input_tokens, output_tokens, llm_calls, tool_calls[], tool_steps, tool_texts[], truncated, wall_clock_s, cost_$, session[], thinking[]}`。

- **R1**：SYS_PROMPT "Godot 引擎 core/" → 目标感知。
- **R7**：skills 臂 `max_steps` 6→10（SOP 更费步）；其它臂保持 6。

### D3. 报告写器 + 目录 schema

```
eval/reports/agent-compare/<UTC-ts>-<target>/
  conclusion.md       人读：哪臂赢、by 哪指标、显著性、诚实标注
  summary.json        臂×指标矩阵（每臂一套全指标）
  matrix.md           可视化网格（{KB×skills} × 指标）
  arms/<arm>/
    config.md         这臂工具集 + 注入的 skill（透明可审计）
    aggregate.json    这臂指标聚合（mean across episodes）
    episodes/qNN/
      episode.json    query+gold+answer+correct+逐步tool+单题指标  [入库]
      session.jsonl   完整消息流逐轮                             [gitignore]
      thinking.md     思考过程（thinking block 或 reasoning）      [gitignore]
```
入库策略（D-锁定）：conclusion/summary/matrix/arms/<arm>/{config,aggregate,episodes/episode.json} 入库；`session.jsonl`+`thinking.md` 本地 gitignore。`.gitignore` 加 `eval/reports/agent-compare/*/arms/*/episodes/*/session.jsonl` + `thinking.md`。

### D4. 指标集（每臂；summary.json = 矩阵）

| 指标 | 含义 | 来源 |
|---|---|---|
| `accuracy` | 终答正确率（gold broad match） | run_ab_agent `_judge` |
| `input_tokens` / `output_tokens` / `total_tokens` | token 消耗 | resp.usage 累加 |
| `llm_calls` | LLM 调用轮数 | = steps |
| `tool_steps` | 工具调用次数 | len(tool_calls) |
| `wall_clock_s` | 端到端耗时 | time.time() |
| `cost_$` | 钱（token×单价） | MODEL_PRICES |
| `context_compression` | 有KB vs 无KB 注入token比 | kb/no-kb arm token 比 |
| `tool_diversity` | 用了几种不同工具 | len(set(tool_calls)) |

### D5. bug_fix 题型（Option B——给 skills 发挥空间）

纯检索（find symbol）上 skills 无价值。新增 `bug_fix`：
- `query` = bug 复现/描述（需理解控制流，非词面查找）
- `gold` = `{symbols: [要改的符号], files: [预期文件]}`
- 判分复用 code_retrieval 的 broad match（answer 含 gold 符号/文件）
- 每目标 curate 5-8 道（比检索难，给 systematic-debugging 等 SOP 发挥空间）
- 4 臂跑 code_retrieval + bug_fix 两类 → 跨难度对比

### D6. bench-author-problems skill 编排范围

skill 在引擎之上，编排（不实现）：给目标工程 → goldgen 设计 code_retrieval 题 → 手动 curate bug_fix 题 → AI 审（`goldgen-verify` 实证 + **独立 subagent 语义审**，skill 里固化 subagent 提示词——这步现在缺）→ 人工 approve 入库 → `bench run agent-compare` → 目录报告。引擎做：ab_agent 改造 / 报告写器 / bug_fix schema / CLI。

## Risks / Trade-offs

| # | Risk | Mitigation |
|---|---|---|
| R1 | SYS_PROMPT 硬编码 Godot | D2 改目标感知（从 target 读） |
| R2 | bundled skill 是精简 SOP，非完整 skill 运行时 | conclusion + config.md 标注"注入 SOP 文本，非触发机制" |
| R3 | GLM 判分同家族 self-preference | conclusion 标注；accuracy 当相对值 |
| R4 | GLM 单价未知 → cost_$ null | MODEL_PRICES 留表，未知则 null + note |
| R5 | session.jsonl 大 | 本地 gitignore + tool_result 截断 top-N chars |
| R6 | 本机无 anthropic → 跑不了真 episode | 复用 test_ab_agent mock 模式做 smoke；真跑待凭据 |
| R7 | skills 臂 SOP 更费步 → max_steps=6 截断 | skills 臂 max_steps 放宽 10 |
| R8 | bug_fix 题仍判 symbol-match，可能仍偏检索 | 题目设计强调"需推理定位"（非词面）；后续可加 LLM-judge 修复质量 |

## Migration Plan

连续提交（每步带验证）：
1. ab_agent.run_episode 6 项改造 + 去 Godot（mock 测试）。
2. ab_tools ARMS 升级 {tools,skills} + 4 臂 + 旧臂名兼容。
3. skills_bundled/{superpowers,openspec}.md 精简 SOP。
4. bug_fix type（targets.py schema + 校验 + 一批示例题）。
5. agent_compare_report.py 目录写器（mock 跑通）。
6. bench CLI run agent-compare 子命令。
7. run_ab_agent 适配新臂/指标/写器。
8. 测试：mock LLM smoke（无凭据跑通写器+流水线）+ bug_fix schema。
9. bench-author-problems skill。
10. 文档（runbook + frontend-guide 若前端）。

**回滚**：连续提交，`git revert` 该批即可。bug_fix type 是 schema 加法（向后兼容，旧 target 无 bug_fix 题不受影响）。

## Open Questions

- **OQ1**：bug_fix 的 gold 判分是否要加"修复质量" LLM-judge（不只 symbol-match）？本变更先用 broad match（复用），R8 留后续。
- **OQ2**：`cost_$` 的 GLM 单价——需查 BigModel 当前定价填 MODEL_PRICES；查不到则 null。
- **OQ3**：旧臂名（baseline/kb/doc/codegraph）兼容映射保留多久？倾向本变更保留映射（ab-agent 旧入口不破），下个变更再删。

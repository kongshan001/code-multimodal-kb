# Tasks · add-bench-agent-compare

按 design.md 迁移计划（10 步）拆。每步独立提交 main + push（带 Co-Authored-By）。每 task 带验证证据。本机无 anthropic → 各步用 mock 验证；真 episode 待凭据。

## 1. ab_agent.run_episode 改造（6 项 + 去 Godot）

- [x] 1.1 去 SYS_PROMPT 上帝化：BASE_SYS_PROMPT 改目标感知（从 target 读 language/notes，不硬编码 Godot）；system = BASE + concat(skill 内容)
- [x] 1.2 输出扩 `llm_calls`(=steps) / `tool_steps`(=len tool_calls) / `wall_clock_s`(time.time 包 episode) / `cost_$`(MODEL_PRICES×token，未知 null)
- [x] 1.3 捕 `session`（序列化每轮 role+content，tool_result 截断 top-N）+ `thinking`（抽 thinking block，无则 fallback 该轮 text）
- [x] 1.4 skills 臂 max_steps 放宽 10（非 skills 臂保持 6）
- [x] 1.5 改 `test_ab_agent.py` mock 适配新输出字段 → 全绿（无凭据可跑）

## 2. ab_tools 臂注册表升级

- [x] 2.1 `ARMS: dict[str,{tools,skills}]` + 4 臂定义（no-kb/kb/kb+superpowers/kb+openspec）
- [x] 2.2 旧臂名（baseline/kb/doc/codegraph）兼容映射（baseline→no-kb, kb→kb, doc→no-kb, codegraph→no-kb 工具近似）——保 ab-agent 旧入口不破（OQ3）
- [x] 2.3 skill 内容加载器：从 `eval/arms/skills_bundled/<name>.md` 读
- [x] 2.4 `arm_schemas(arm)` 适配新结构（取 arm["tools"]）

## 3. skills_bundled 精简 SOP

- [x] 3.1 `eval/arms/skills_bundled/superpowers.md`：精简 brainstorming + systematic-debugging + TDD SOP（可注入 prompt 的文本）
- [x] 3.2 `eval/arms/skills_bundled/openspec.md`：精简 spec-before-code 纪律
- [x] 3.3 标注：这是 SOP 文本近似，非完整 skill 运行时（R2 诚实边界）

## 4. bug_fix problem type

- [x] 4.1 `eval/targets.py` schema 加 bug_fix：gold={symbols, files} 均非空 list[str]；_GOLD_FIELDS + _LIST_GOLD 更新
- [x] 4.2 loader 校验 + slugify/assign_ids 兼容（bug_fix 用 query）
- [x] 4.3 给 1-2 个现有 target curate 示例 bug_fix 题（5-8 道，需推理定位非词面）
- [x] 4.4 test_targets_loader.py 加 bug_fix 合法/非法 case → 全绿

## 5. agent_compare_report.py 目录写器

- [x] 5.1 新模块：输入多臂 episode 结果 + 臂配置 → 写目录（conclusion.md/summary.json/matrix.md/arms/<arm>/{config,aggregate,episodes/qNN/{episode.json,session.jsonl,thinking.md}}）
- [x] 5.2 conclusion.md 人读结论（哪臂赢+by指标+显著性+诚实标注）+ summary.json 臂×指标矩阵 + matrix.md 可视化
- [x] 5.3 `.gitignore` 加 session.jsonl + thinking.md 规则（结论类入库）
- [x] 5.4 mock 跑通写器（无凭据产出结构完整报告）→ 测试覆盖

## 6. bench CLI run agent-compare 子命令

- [x] 6.1 `cli.py` 加 `run agent-compare --target <id> [--arms ...] [--runs N] [--subset N] [--smoke]`
- [x] 6.2 调 run_ab_agent（多臂）+ agent_compare_report 写器
- [x] 6.3 `--smoke` 模式：无凭据用 mock LLM 跑通

## 7. run_ab_agent 适配新臂/指标/写器

- [x] 7.1 适配新 ARMS 结构 + skills 注入 + bug_fix 题型（两类题都跑）
- [x] 7.2 聚合新指标（accuracy/llm_calls/tool_steps/wall_clock/cost/context_compression/tool_diversity）
- [x] 7.3 调 agent_compare_report 写目录报告
- [x] 7.4 旧 `_judge` broad match 复用至 bug_fix

## 8. 测试

- [x] 8.1 mock LLM smoke：无凭据跑通 agent-compare 全流水线（4 臂 + 目录报告结构完整）
- [x] 8.2 bug_fix schema 校验（合法 + 缺 symbols/files 拒）
- [x] 8.3 报告写器单测（mock 输入 → 目录结构 + summary 矩阵 + conclusion 含诚实标注）
- [x] 8.4 全量 `pytest eval/tests/` 绿（除既有 anthropic-blocked）

## 9. bench-author-problems skill

- [ ] 9.1 `.claude/skills/bench-author-problems/SKILL.md`：编排"给目标工程 → goldgen 设计 code_retrieval → 手动 curate bug_fix → AI 审（goldgen-verify 实证 + 独立 subagent 语义审，固化 subagent 提示词）→ 人工 approve 入库 → bench run agent-compare → 目录报告"
- [ ] 9.2 界定 skill 编排 vs 引擎做（skill 不实现，只编排 + 固化 subagent 语义审提示词）
- [ ] 9.3 触发描述覆盖"给 X 工程 benchmark + 对比 skills"、"测 superpowers/openspec 价值"

## 10. 文档

- [ ] 10.1 `docs/benchmark-runbook.md`：agent-compare 段（4 臂 + 指标 + 目录报告 + 诚实边界）
- [ ] 10.2 `docs/frontend-guide.md`：若前端触发 agent-compare，补说明（否则标后续）
- [ ] 10.3 README/target README 提及 bug_fix 题型 + agent-compare（按需）

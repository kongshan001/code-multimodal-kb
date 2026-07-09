## 1. Stage 0：边界落地与文件记忆加固（零凭据·零新工具）

- [x] 1.1 把 D1 四层归属规则 + 判定测试（"忘了这条 agent 会不会被纠正"）写入 `CLAUDE.md` 作为强制纪律 — 新建项目级 `CLAUDE.md`（repo 根，git 跟踪），含四层归属表 + 判定测试金句 + 范围边界
- [x] 1.2 给文件记忆设分类纪律：每条 fact 的 frontmatter `type` 限定为 user/feedback/project/reference 之一；为 MEMORY.md 索引设容量上限规则 — 写入项目 `CLAUDE.md`「分类纪律」(type 四选一, 无匹配则拒) +「容量上限」(~20 条, 超限降级为按需召回, Stage 1 后失效)；实测 MEMORY.md 现 3 条远低于上限
- [x] 1.3 建决策→情景锚机制：决策型 memory 条目 MUST 附带 git commit 或 tasks 条目引用 — 规则入 `CLAUDE.md`「决策锚」；演示: 新写 `memory/agent-memory-approach.md` (type: project) 锚 commit `daf359b` + tasks §2，并在 MEMORY.md 加索引行
- [x] 1.4 端到端验证 Stage 0 → 验证：新会话启动时相关偏好被正确铺垫；构造 4 条候选事实（客观/程序/事件/主观各一）按判定测试全部正确路由 — 铺垫: MEMORY.md 本会话已注入上下文（2 条原条目可见），新条目下会话生效；路由 4 案全对：①"cmm search_code ~112ms"→否→KB/cmm ②"部署 cmm 步骤"→否→程序/runbook ③"7/7 完成 task 4.1"→否→情景/commit 6ae72e5 ④"用户偏好全局工具"→**是**→memory/✓；实测 memory/ 仅含 project/feedback（主观），无客观/程序/情景泄漏

## 2. Stage 1：Mem0 / OpenMemory MCP 接入（凭据门控·与 doc-side KB 共享解锁）

- [ ] 2.1 前置：LLM 凭据就位（与 `add-code-multimodal-kb` doc-side graphify 共享同一 key）→ 验证：key 可被 Mem0 抽取调用
- [ ] 2.2 自托管 Mem0（Docker：API + Postgres/pgvector + Neo4j；或全本地 Qdrant + Neo4j + Ollama）→ 验证：健康检查通过 + add/search 往返成功
- [ ] 2.3 OpenMemory MCP 注册到 Claude Code（及已注册 cmm 的其他 agent）→ 验证：agent 内 `mcp__openmemory__*` 工具可调
- [ ] 2.4 迁移现有 MEMORY.md 事实进 Mem0；召回从全量注入切到相关性召回 → 验证：旧事实可被按主题召回，且不再全量进上下文
- [ ] 2.5 端到端联调 → 验证：同一会话内记忆召回（主观，走 Mem0）与 KB 查询（客观，走 cmm/graphify）各走各路、不互相污染

## 3. Stage 2：Zep / Graphiti 时序召回（可选·情景痛点触发）

- [ ] 3.1 触发评估：确认"决策/事件时序召回"是真实痛点（仅当 Stage 1 后情景召回仍不足）才启动，否则跳过本节
- [ ] 3.2 自托管 Graphiti（Neo4j 或 FalkorDB 后端）+ MCP 注册到 agent → 验证：时序图建图 + MCP 工具可调
- [ ] 3.3 验证时序召回 → 验证：按时间线/实体回溯某决策的脉络，结果带时间戳与来源

## 4. 评测（记忆召回质量基线）

> **归属**：记忆评测归横切变更 `add-evaluation-baseline` §4；本节为历史 task，实际进度以该变更为准。

- [ ] 4.1 评测 harness：封装"调 Mem0 收集 (query, 召回结果, gold)"，锁定抽取模型 + 版本保证可复现
- [ ] 4.2 召回质量指标：recall@k / 命中率 + 实体去重正确率 + 注入体积收敛曲线
- [ ] 4.3 边界正确率：候选事实（主观/客观/程序/事件）路由准确率，验证 D1 归属规则可操作

## 5. 部署与文档

- [ ] 5.1 runbook：Mem0 自托管 + MCP 注册完整步骤（沿用 `add-code-multimodal-kb` 的 runbook 模板：锁版本 + checksum + 注册副作用 + 回滚）
- [ ] 5.2 把 D1 边界纪律 + Stage 0/1/2 路线沉淀进 `docs/deployment-runbook.md` 与 `CLAUDE.md`

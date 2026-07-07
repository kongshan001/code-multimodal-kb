## 1. 环境与接入（复用工具）

- [x] 1.1 确认 graphify 已升级到 0.8.46 且 `graphify --version` 无 warning（已验证：`graphify 0.8.46`，无 warning）
- [x] 1.2 安装 / 配置 codebase-memory-mcp 为 MCP server，验证可对示例仓库建图与查询 — 二进制 v0.8.1 装于 ~/.local/bin（checksums.txt 校验通过 + ad-hoc 签名，未抓 main），cli 通道 + index_repository 验证通过；MCP server 注册到 agent 归 task 4.1（待确认 install 副作用后执行）
- [ ] 1.3 验证 `graphify --mcp` 可作为 MCP server 启动并被 agent 调用
- [ ] 1.4 决策 graphify 图存储：`graph.json`（文件）或 Neo4j（`--neo4j`）

## 2. 代码知识库（code-knowledge-base，复用 codebase-memory-mcp）

- [x] 2.1 把目标代码仓库接入 codebase-memory-mcp，完成首次全量索引（tree-sitter AST + 类型解析 → KG） — engineer_demo 流程跑通（零代码）；graphify 源码实质索引：2192 节点 / 802 函数 / 4979 边 / 2.6s，含 CALLS(1518)+USAGE(860)+IMPORTS(51)+SEMANTIC_RELATED(25) 边
- [x] 2.2 验证跨仓库自然语言问答、符号定位、调用链查询 — search_code（符号定位 112ms，file:line+度数+3.4x 去重）、trace_path（callees+callers 多跳 hop1-3）、get_code_snippet（完整源码+file:line+元数据）均验证通过且不调 LLM；query_graph 吃结构 DSL（裸 NL 报 parse 错），用法待确认——非阻塞，NL 检索由 agent 用 search_code+trace_path 组合（符合决策4）
- [x] 2.3 配置增量索引（文件变更后只重索引受影响部分） — detect_changes 验证通过（基于持久化文件哈希检测 changed_files + impacted_symbols，depth=2），建图时 persist_hashes pass 已对 168 文件落哈希；config auto_index 默认 false（按需开启归 task 6.2/6.3）
- [ ] 2.4 代码检索评测基线（跨仓库问答集 → 召回 / 命中率）

## 3. 多模态知识库（multimodal-knowledge-base，复用 graphify，docs-only）

- [ ] 3.1 对设计文档 / 论文 / 技术资料 / 图片建图：**指向纯文档目录**（代码不进 graphify，Part A 自动空跑）
- [ ] 3.2 验证跨文档理解：`query`（BFS/DFS）、`path`（概念间最短路径）、`explain`（节点解释）+ `source_location` 引用
- [ ] 3.3 配置增量更新（`--update` / `--watch` / post-commit hook 三选一）+ LLM token 成本控制（评估 Gemini 后端）
- [ ] 3.4 跨文档理解评测基线

## 4. Agent 注册与联调

- [x] 4.1 把 codebase-memory-mcp 与 graphify（`--mcp`）注册到 Claude Code / Cursor 的 MCP 配置 — cmm 已注册到 Claude Code（~/.claude.json + ~/.claude/.mcp.json）+ Codex/OpenCode/VS Code，含 PreToolUse(Grep/Glob 增强)+SessionStart hooks + codebase-memory skill；graphify-mcp 注册走 graphify install 归 task 6.3（依赖文档图 → LLM 凭据）；本机未装 Cursor 故跳过；改前配置已备份 /tmp/cmm-config-backup 可回滚
- [ ] 4.2 端到端联调：同一 agent 会话内分别用两路回答代码问题与文档问题
- [ ] 4.3 处理两个 MCP server 的工具命名 / 优先级冲突

## 5. 评测（benchmark 深度调研后重做）

- [ ] 5.1 评测 harness：建 pytest 套件 + 封装「调两个 MCP 收集 (query, 检索/图结果, answer, gold)」；先锁 graphify `temp=0 + 模型 + 版本` 保证可复现（B2 前置）
- [ ] 5.2 代码检索主轨道：RepoBench-R（recall@k / nDCG@10）+ SWE-Lancer-Loc（216 条 NL→文件/函数定位命中率）
- [ ] 5.3 代码图检索专用指标（自建）：Symbol-Level Hit@k、Call-Chain Edge Recall、Path Precision@k（gold 来自静态调用图）
- [ ] 5.4 CoIR 降级对照：cosqa + codesearchnet + stackoverflow 子集跑 nomic-embed-code 向量基线（防退化，分数不与榜单比）
- [ ] 5.5 代码 ground truth：从真实 merged PR 反挖（NL issue → git diff 解析 gold symbols → 静态调用图 gold 链）+ 执行式验证（LSP goto-def 反查）
- [ ] 5.6 文档答案质量：DeepEval faithfulness / answer relevancy / G-Eval（评 graphify 文本节点→答案）
- [ ] 5.7 GraphRAG 答案：复刻 MS GraphRAG LLM grader（comprehensiveness / diversity / empowerment head-to-head vs 朴素 RAG）
- [ ] 5.8 抽取质量抽样：独立模型（非 graphify 抽取模型）打 entity / relation / claim 准确率
- [ ] 5.9 外部跨文档基线：GraphRAG-Bench / WildGraphBench 子集作 held-out；RAGChecker 降级为 claim-level 归因诊断
- [ ] 5.10 触发行动的阈值门禁：recall@5<0.6→补文档向量 / anchoring<70%→重设计 bridging / 抽取<0.7→调 prompt / P95>2s→缓存
- [ ] 5.11 文档化自托管 / 配置 / 跑评测步骤（含模型版本锁定说明）
- [ ] 5.12 解决 design Open Questions：图存储形态、增量更新方式、工具命名冲突

## 6. 其他设备接入 / 环境部署

- [ ] 6.1 前置确认：macOS/Linux/Windows + 支持 MCP 的 agent（Claude Code / Cursor / Codex 等）+ Python & uv（graphify）+ Python（DeepEval）
- [ ] 6.2 代码 KB 安装：**锁定具体 release 版本（非 main）+ 校验 checksum** 后再 install（避免 `curl|bash` 抓 main 导致版本漂移 / 供应链风险）；CN 网络用代理（本机 `127.0.0.1:7897`）或 ghproxy 镜像拉 install.sh；安装器自动识别 agent 写 MCP 配置；按需 `codebase-memory-mcp config set auto_index true`
- [ ] 6.3 多模态文档 KB 安装：`uv tool install graphifyy` → `graphify install`（同步 skill + 注册 CLAUDE.md）→ `graphify <docs-path>` 建图 → `graphify <docs-path> --mcp` 起 server 并在 agent 注册
- [ ] 6.4 评测环境（可选）：`pip install deepeval`，拉仓库跑 pytest 评测套件
- [ ] 6.5 验证：agent 内分别测一条代码问题（走 codebase-memory-mcp）与一条文档问题（走 graphify）
- [x] 6.6 文档化部署 runbook — docs/deployment-runbook.md 已纳入仓库：A 代码侧（cmm v0.8.1 完整步骤：锁版本+checksum+签名+落位+注册副作用+查询验证）实测通过；B 文档侧（graphify 建图）依赖 LLM 凭据，框架就绪待补全；FAQ 沉淀 SSL 抖动/quarantine/install 删索引/query_graph DSL 等实测踩坑

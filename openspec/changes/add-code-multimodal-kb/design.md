## Context

本仓库要为 **agent / IDE（Claude Code、Cursor、Codex 等）** 提供知识库能力，覆盖跨仓库代码问答 + 多模态文档（设计文档 / 论文 / 技术资料）跨文档理解。消费方就是 agent 本身，因此**不自建网关、不引入平台外壳**——直接复用两个 MCP server 注册给 agent：

- **codebase-memory-mcp** → 代码知识图谱
- **graphify（`--mcp`）** → 多模态文档知识图谱（docs-only，不碰代码）

按 Simplicity First + 复用优先，本 change 几乎不写代码，核心是「安装 + 配置 + 注册 + 验证 + 评测」。当前 `openspec/specs/` 为空，greenfield。

约束：优先 ≥10K star 成熟开源项目（star 为 2026-07 GitHub API 快照）；必须可自托管。

## Goals / Non-Goals

**Goals:**
- 复用 codebase-memory-mcp 覆盖代码知识库（AST + 类型解析 + 调用链）
- 复用 graphify 覆盖多模态文档知识库（docs-only，跨文档理解 / 关系梳理）
- 把两个 MCP server 注册到 agent，验证跨工具检索可用
- 建立检索 / 回答质量评测基线

**Non-Goals:**
- 不自建网关 / HTTP API（消费方是 agent，MCP 即接口）
- 不引入 RAGFlow / Dify 平台外壳（不需要 UI）
- 不做 ColPali 视觉页级检索（多模态 = 跨文档理解，抽取式够用）
- graphify 不处理代码（代码归 codebase-memory-mcp，避免重复建图）
- 不自研索引 / 知识图谱 / embedding / 视觉模型
- 不服务非 agent 消费方（webapp / 产品 HTTP 客户端 / 内部 wiki）——MCP 只能被 MCP client 调用；若未来需产品功能集成，另起 change（届时自建薄 HTTP 网关或上 RAGFlow / Dify 外壳）

## Decisions

### 决策 1：架构 = 两个 MCP server 直连 agent（零自建）

```
codebase-memory-mcp  ─┐
                      ├─→  注册到 Claude Code / Cursor / Codex（MCP config）
graphify --mcp        ─┘
```

无网关、无外壳、无自建检索代码。两路结果的整合交给 agent 自身（在它的能力范围内）。

### 决策 2：代码 KB = codebase-memory-mcp（27.2K★），graphify 不碰代码

| 方案 | Stars | 机制 | 结论 |
|---|---|---|---|
| **codebase-memory-mcp** (DeusData) | **27.2K** | tree-sitter AST + 轻量 LSP 类型解析 → 持久 KG，毫秒级，含调用链 / 引用 | ✅ **采用** |
| graphify Part A | 本地 skill | 仅 AST 抽取，无类型解析 / 调用链 | ❌ 对代码弱，不用于代码 |
| 自建 tree-sitter + 向量 | — | — | ❌ 重复造轮子 |

**结论**：代码 KB 由 codebase-memory-mcp 独占。graphify 不索引代码——既避免重复建图 + 双倍存储，也因为 codebase-memory-mcp 对代码严格更强（有类型解析与调用链）。

### 决策 3：多模态 KB = graphify（docs-only），砍 ColPali

用户多模态场景为**跨文档理解 / 关系梳理**（设计文档、论文、技术资料），非表格 / 扫描件的精确页级召回。

- 指向**纯文档目录** → graphify 的 Part A（代码 AST）自动空跑，只跑 Part B 语义抽取，**天然不碰代码**
- 检索用 graphify 的 `query`（BFS/DFS）、`path`（概念间最短路径）、`explain`（节点解释），引用用 `source_location`
- 砍掉 ColPali / ColQwen2 及 GPU 依赖（范式对比详见 v2，本场景不需要视觉页级召回）

### 决策 4：NL 检索流程（agent 翻译 + 工具检索）

**查询阶段**两个 MCP server 均不调 LLM——NL→查询由 agent 翻译、工具只跑图 / 结构查询；但 **graphify 建图阶段依赖 LLM**（Part B 语义抽取，默认 host agent，可选 Gemini backend），故无 LLM 凭据环境建不了文档图。

**路由三分**：

| 问题类型 | 主路 |
|---|---|
| 纯代码（「X 在哪 / 谁调它」） | codebase-memory-mcp |
| 纯文档（「文档怎么描述 X」） | graphify |
| 设计↔代码（「文档写的 X 代码在哪」） | graphify 锚定概念 → codebase-memory-mcp 落代码 |

**代码侧主路 = codebase-memory-mcp 的 `semantic_query`**（自带 nomic-embed-code 向量 + 11 信号混合打分，**直接处理词汇不匹配**，无需 agent brainstorm 同义词）。仅当 `semantic_query` 空召回时走结构兜底（retrieve-then-narrow）：

1. **抽取**：从 NL 抽候选标识符 / 概念 / 动词
2. **符号检索**：符号搜索 / 模糊名匹配 → 候选符号
3. **收窄**：用调用链 / 引用 / 类型 确认

（文档侧 graphify 无向量，靠其自身 `query` 词汇扩展 + BFS/DFS；词汇不匹配风险集中在文档侧，见已知短板。）

**graphify 间接桥**：`graphify query` 把模糊概念变成文档图里的**具名实体** → 拿该标识符喂 codebase-memory-mcp 定位实现 + 调用链。

**已知短板（修正）**：codebase-memory-mcp 自带 `semantic_query`（内置 nomic-embed-code + 11 信号混合打分，零 API key），**代码侧词汇不匹配风险低**；真正的风险在 graphify 文档侧（纯图遍历、无向量），靠 graphify 自身词汇扩展 + agent 兜底。若文档侧评测召回不足，再考虑补文档向量——**代码侧无需另建向量索引**。

### 决策 5：图存储 = 默认 graph.json（前置决策，非 Open Question）

部署形态依赖此选择（Neo4j 需 JVM + 独立服务，会推翻「单机零依赖」承诺），故前置拍板（审核 B1）：**默认用 graphify 的 `graph.json`（文件）**，零额外依赖、契合单机自托管；**仅当单机压测超阈值**（节点数过多或查询并发打满文件加载）才切 Neo4j（`--neo4j`）。task 1.4 先做 graph.json 压测定阈值。

## Risks / Trade-offs

- **依赖两个相对新的图范式工具** → codebase-memory-mcp 27.2K★ 较成熟；graphify 社区较小，需关注维护活跃度，必要时可回退自建代码索引。
- **graphify 语义抽取消耗 LLM token** → 用 `--update` 增量 + 缓存；评估切 Gemini 后端降本。
- **graphify 语义抽取非确定**（LLM 生成）→ 多设备/跨时间图不一致、评测不可复现、cross-tool anchoring 脆弱（同概念不同机器命名不同）。缓解（审核 B2）：**锁 `temp=0 + 固定 LLM 模型 + graphify 版本`** 并记入评测报告；anchoring **经 `source_location` 抽真实代码标识符**，不靠节点显示名裸传递。无 LLM 凭据环境建不了文档图（已知约束）。
- **文档内嵌代码块污染图**（审核 M6）→ 设计文档/论文里的代码片段会被 Part B 抽成「符号」节点，与 codebase-memory-mcp 真实符号混淆、`source_location` 跳到 markdown 代码块。缓解：graphify 抽取 prompt 约定「只抽领域概念不抽代码符号」+ 节点标 `provenance`（doc_inline_code vs source_code）。
- **两路结果靠 agent 自己整合（无网关融合）** → 在 agent 能力范围内可接受；若日后发现整合不稳，再补薄层（届时按需引入，非现在）。
- **图检索对「精确片段召回」弱于向量** → 当前场景为关系梳理，可接受；未来若有精确召回需求再补向量路径。

## 评测体系（benchmark 深度调研后重做）

两轮 subagent 深度调研（代码侧 + GraphRAG/多模态侧）的核心结论：**原选型（DeepEval + CoIR + RAGChecker）评了「答案质量 + chunk-RAG 归因」，却完全没评我们的核心差异化价值——图结构质量、跨文档关系、符号/调用链定位**。CoIR 是纯 dense-embedding 评测（范式错配），DeepEval/RAGChecker 把 context 当 flat chunks（丢图结构）。重做如下。

### 代码侧（图/结构/agent 检索）

| 角色 | 选型 | Stars | 用途 |
|---|---|---|---|
| 主轨道 | **RepoBench-R**（ICLR24）+ **SWE-Lancer-Loc**（216 NL→文件/函数） | 208 / 1.4K | repo 级检索 ranking + agent 符号定位（干净、已释出） |
| 图检索专用指标（自建） | Symbol-Level Hit@k / Call-Chain Edge Recall / Path Precision@k | — | 测 codebase-memory-mcp 真正关心的「定位符号 + 调用链」 |
| 向量基线对照 | CoIR 子集（cosqa + codesearchnet + stackoverflow） | 155 | 降级为 ~10-15%，仅防 nomic-embed-code 退化 |
| 方法论锚 | RepoHyper（tree-sitter + 调用图 + RSG + GNN，架构最像我们） | 73 | 读它省试错 |
| 备选 | CORE-Bench（2026-06，专为补 CoIR 的洞，**暂无公开 repo**） | — | 盯释出再上 |

### 文档侧（GraphRAG / 跨文档理解）

| 角色 | 选型 | Stars | 用途 |
|---|---|---|---|
| 答案质量 | **DeepEval**（保留，缩小范围） | 16.7K | faithfulness / answer relevancy / G-Eval 评 graphify 抽取后的**文本节点 → 答案** |
| 归因诊断 | RAGChecker（降级） | 1.1K | claim-level 区分检索/生成错；**节点拍扁为 chunks，认知丢图结构**；repo 2024-12 起停滞 |
| GraphRAG 答案（新增） | **MS GraphRAG LLM grader**（`graphrag/evaluate/llm_grader/`） | 34.2K | comprehensiveness / diversity / empowerment head-to-head，GraphRAG 圈事实标准，几十行复刻 |
| 抽取质量（新增） | 独立模型 LLM grader 抽样打 entity / relation / claim | — | 补「图构建质量」整块盲区（graphify 核心价值所在） |
| 外部跨文档基线（新增） | GraphRAG-Bench（ICLR26）/ WildGraphBench（ACL26）子集 | 456 / 16 | held-out，避免作者自标偏见 |

**砍掉**：DeepEval 多模态指标（graphify 抽取阶段已把图转文本，触发不了）、ViDoRe / ColPali（不做页级图像检索）、AutoRAG / RagaAI（无 GraphRAG 支持 + 停滞）。

### Ground truth（避「LLM 评 LLM」循环 + 作者自标偏见）

- **代码侧**：从真实 merged PR 反挖——NL issue 当 query，git diff 解析出的被改函数当 gold symbols，静态调用图当 gold 调用链；叠加执行式验证（LSP goto-def 反查 agent 输出命中）。零 LLM judge。
- **文档侧**：借用 MuSiQue / GraphRAG-Bench 的 gold path；hold-out 10-20% 文档测过召回 / 幻觉抵抗力；**gold 生成模型 ≠ graphify 抽取模型**（防 Preference Leakage）；多裁判集成（Claude + GPT + Gemini 取均值）。

### 触发行动的阈值（否则评测劳而无功）

| 指标 | 阈值 | 触发动作 |
|---|---|---|
| 文档侧 recall@5 | < 0.6 | 评估补文档向量索引 |
| cross-tool anchoring 成功率 | < 70% | 重设计 bridging（改走 `source_location` 而非裸字符串） |
| 抽取质量 entity/relation 准确率 | < 0.7 | 调 graphify 抽取 prompt / 换模型 |
| 查询 P95 延迟 | > 2s | 加查询缓存 |

### 评测可复现性前提

graphify 语义抽取非确定（见 Risks），评测基线可复现**必须先锁**：`temp=0 + 固定 LLM 模型 + graphify 版本`，并在评测报告记录这三项——否则跨设备/跨时间分数无意义（见审核 must-fix B2）。

## 部署：其他设备接入

两个核心工具都是**单机自包含**（codebase-memory-mcp 单静态二进制、零依赖；graphify 为 uv tool），**安装器自动配置 agent**，所以新设备接入 =「下载 → install → 建图」。**无需共享状态同步**——图索引从源码/文档在本机重建（`~/.cache/codebase-memory-mcp/`、`graphify-out/`），仅评测测试集与 agent 配置随 git / 仓库走。**版本锁定 + CN 可达性**（审核 M7）：codebase-memory-mcp 锁定具体 release（非 main）并校验 checksum；`raw.githubusercontent.com` 在 CN 默认不可达，走代理（本机 `127.0.0.1:7897`）或 ghproxy 镜像。具体步骤见 tasks.md §6。

## Open Questions

1. graphify 增量更新走 `--update`（手动 / post-commit hook 触发）——`--watch` 是 AST-only（不跑 Part B 语义），不适用 docs-only。
2. 两个 MCP server 在 agent 配置里的工具命名 / 优先级如何避免冲突？（Claude Code 用 `mcp__<server>__<tool>` 前缀无冲突，其他 client 待验证）

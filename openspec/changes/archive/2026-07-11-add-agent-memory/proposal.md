## Why

agent 跨会话需要"记忆"（用户偏好 / 关键决策 / 工作情景），但当前是 **5 个互不连通的记忆孤岛**：context window（工作）/ git+tasks.md（情景）/ skills（程序）/ cmm+graphify（语义-客观，KB 项目进行中）/ MEMORY.md（语义-主观，仅 2 条 · 全量注入 · 无智能召回）。两个真实缺口拖低 agent 质量：**(1) 语义-主观层太薄**——MEMORY.md 全量注入会膨胀、无相关性召回；**(2) 情景记忆不可被 agent 主动召回**——决策散落在 git/tasks，agent 不会"想起上次定的事"。需要把记忆确立为与 KB / skills / git 并列、职责清晰的一层。

## What Changes

- **确立记忆边界**：把"记忆 vs KB vs skills vs git"四层归属规则与判定测试固化成 spec（记忆 = 前摄式铺垫/主观；KB = 反应式查询/客观）
- **Stage 0（零凭据·零新工具）**：加固现有文件记忆——分类纪律（user/feedback/project/reference）+ MEMORY.md 容量上限 + 把 git/tasks 显式接成"可指回"的情景源；本阶段即产出可用价值
- **Stage 1（MemPalace·核心零 LLM·不卡凭据）**：接入 **MemPalace**（[github.com/MemPalace/mempalace](https://github.com/MemPalace/mempalace)，19.5K★，MCP server + ChromaDB embedded + 内置 temporal KG）作为语义-主观 + 情景存储，把薄文件记忆升级为向量 + 图召回；**替换原选 Mem0**（部署成本：pip+embedded vs 3 容器；核心零 LLM 解绑凭据墙；内置 temporal KG 吸收 Stage 2）；明确**排除 Cognee**（与 graphify 同物撞车）和 **Letta/MemGPT**（agent 须跑在其内，Claude Code 架构错配）
- **Stage 2（可选）**：先用 **MemPalace 内置 temporal KG** 做决策 / 事件时序召回；评估不足才接入 **Zep / Graphiti**（Neo4j/FalkorDB）
- 沿用 `add-code-multimodal-kb` 确立的"复用成熟 MCP + 注册到 agent"原则，**不建网关、不引平台外壳、几乎零自建代码**

## Capabilities

### New Capabilities
- `agent-memory`: agent 跨会话的主观记忆层——用户偏好 / 关键决策 / 工作情景的捕获、存储、召回与生命周期管理；与代码（归 cmm）/ 文档内容（归 graphify）/ 程序（归 skills）/ 事件审计（归 git）明确分工

### Modified Capabilities
（无——本项目 greenfield，`openspec/specs/` 当前为空；`agent-memory` 与进行中的 `code-knowledge-base` / `multimodal-knowledge-base` 互补不重叠）

## Impact

- **新增依赖（复用）**：MemPalace（Stage 1，`uv tool install` + ChromaDB embedded，零外部服务、零 Docker）；可选 Zep/Graphiti（Stage 2，仅 MemPalace temporal KG 不足时，Neo4j/FalkorDB）。原 Mem0 路线（`deploy/mem0*`）标记弃用
- **模型资源**：MemPalace **核心路径零 LLM**（raw 模式不调 LLM）；仅 extract/rerank extras 可选 LLM，仍与 doc-side graphify 共享同一凭据，无需额外来源、无需 GPU
- **配置变更**：agent 的 MCP server 注册（同 cmm/graphify 的注册套路）；文件记忆的纪律写入 CLAUDE.md / skill
- **范围边界**：只管"主观层"（用户 / 决策 / 情景），**不碰代码**（归 cmm）、**不碰文档内容**（归 graphify）
- **无新增自建服务、无网关、无对外 HTTP API**

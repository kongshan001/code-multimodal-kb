## Why

agent / IDE（Claude Code、Cursor 等）需要知识库能力：跨仓库**代码问答** + 多模态文档（设计文档 / 论文 / 技术资料）的**跨文档理解**。代码知识图谱已有 27K★ 级成熟实现（codebase-memory-mcp），本地已装的 graphify 能把文档建成可查询图。由于消费方就是 agent 本身，**直接复用两个 MCP server 注册给 agent** 即可——不建网关、不引平台外壳，几乎零自建代码。

## What Changes

- **代码知识库**：接入 codebase-memory-mcp（tree-sitter + 类型解析 + 持久 KG），支持跨仓库代码问答 / 符号定位 / 调用链
- **多模态知识库**：接入 graphify（文档 / 论文 / 图片 → 知识图谱，**docs-only 不碰代码**），支持跨文档理解 / 关系梳理
- 把两个 MCP server 注册到 agent（Claude Code / Cursor 配置），端到端验证可用
- 建立代码检索与跨文档理解的评测基线
- **变更（相对 v2）**：消费方确定为 agent → **砍掉 `knowledge-base-gateway` capability、砍掉 RAGFlow/Dify 外壳**；并明确 graphify 不再处理代码（归 codebase-memory-mcp）

## Capabilities

### New Capabilities

- `code-knowledge-base`: 基于 codebase-memory-mcp 的代码知识图谱与代码问答
- `multimodal-knowledge-base`: 基于 graphify 的多模态文档图检索（docs-only，跨文档理解 / 关系梳理）

### Modified Capabilities

（无——本项目为 greenfield，`openspec/specs/` 当前为空）

## Impact

- **新增依赖（复用）**：codebase-memory-mcp（MCP server）、graphify（0.8.46，uv tool `graphifyy`）；可选 Neo4j（graphify `--neo4j`）
- **模型资源**：graphify 语义抽取的 LLM（默认 host / 可选 Gemini）；**无需 GPU**
- **配置变更**：agent 的 MCP server 注册（Claude Code / Cursor 配置文件）
- **无新增自建服务、无网关、无对外 HTTP API**

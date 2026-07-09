# 架构 / 框架总览

> KB（代码 + 文档）+ 记忆 + 评测，全部复用成熟 MCP、注册到 agent、不建网关。
> 跨平台 `setup-kb.py` 一键接入任意项目。Godot 是参考靶子（已验证）。

## 系统组成

```
                         ┌──────────────────────────────────────────────┐
   Claude Code / agent ←─┤  MCP 注册                                     │
                         │   ├─ codebase-memory-mcp (cmm)   代码知识图   │
                         │   ├─ graphify-mcp                文档知识图   │
                         │   └─ mem0(-mcp)                  主观记忆     │
                         └──────────────────────────────────────────────┘
              ▲                                    ▲
   setup-kb.py│ 部署/接入                          │ 评测
   (Win/Mac/  │   ┌─ eval/ harness (pytest) ──────────────┐
   Linux)     └───┤  指标 + gold + 可复现 lockfile         │
                    └─ 产出 recall@k / broad / 跨工具成功率 ┘
```

## 数据流

| 轨 | 输入 | 工具 | 产出 | 查询接口 |
|---|---|---|---|---|
| 代码 KB | 代码仓库 | `cmm index`（tree-sitter + 类型解析）| 代码 KG（符号/调用链/引用）| BM25 主路（`search_graph query`）/ `search_code` / `semantic_query` |
| 文档 KB | 纯文档目录（.md/.rst/…）| `graphify`（LLM Part B 抽取，不碰代码）| 文档 KG（概念/关系/社区）| `query`（BFS）/ `path` / `explain` |
| 跨工具 | 文档概念 | graphify 节点 → 标识符 → cmm | 文档概念↔代码实现定位 | anchoring（design 决策级）|
| 记忆 | 对话/偏好/决策 | Mem0（抽取→向量+图）| 主观记忆库 | recall（前摄式铺垫）|

## 实现原理（三层机制）

核心机制在被复用的 **cmm / graphify** 里；`setup-kb.py` 只是编排器，不自己做检索/建图。

### 第 1 层 · 建索引（源材料 → 可查询图）
- **代码（cmm）**：tree-sitter 切 AST 拿符号（函数/类/方法）→ 静态分析建边（`CALLS`/`USAGE`/`IMPORTS`/`INHERITS`/`WRITES`）→ 轻量 **LSP** 跨文件类型解析（谁调谁、跨文件引用）；moderate 模式再加 **nomic-embed-code** 向量嵌入 + **LSH** 近似近邻。存持久 KG。
- **文档（graphify）**：扩展名分流（代码→Part A AST、文档→Part B）→ **LLM 读文档**抽实体/关系/社区 → `graph.json`。
- **关键**：是"**图**"不是"向量库"——节点=符号/概念，边=关系，所以能查调用链/概念关系，不只是相似度。

### 第 2 层 · 查询（问题 → 图里找）
- **cmm 三路**（实测 BM25 最优）：BM25（NL 分词 + 图中心性排序，主路）/ grep+图（精确标识符）/ 语义（query 向量 vs 函数向量余弦，token 相似）。返回 **符号 + file:line + 边**。
- **graphify**：BFS/DFS 从 NL 匹配的起始节点遍历文档图 → NODE/EDGE。
- **跨工具**：graphify 文档概念节点 → 抽标识符 → 喂 cmm 定位代码（anchoring，100%）。

### 第 3 层 · agent 接入（MCP）
cmm / graphify-mcp 各起一个 **stdio MCP server**，注册到 Claude Code（`~/.claude.json`）。agent 调 `mcp__codebase-memory-mcp__*` / `mcp__graphify__*` 工具 → 工具查本地图 → **结构化结果**回 agent。agent 不直接 grep 代码，拿"符号+file:line+边"推理。

### `setup-kb.py` 的角色：编排器
纯 subprocess 串 `precheck → 设 LLM env → cmm index → graphify build → claude mcp add`。真正建图/检索的是 cmm / graphify；脚本只负责把它们按"建图-查询-注册"串起来（复用，不重造，design 决策1）。

## 记忆四层模型（`add-agent-memory` D1）

| 层 | 载体 | 召回 | 归属判定 |
|---|---|---|---|
| 工作 | context window | 隐式 | 当前任务 |
| 情景 | git + tasks.md | 检索 | 何时做了何事 |
| 程序 | skills/ | 显式 | 怎么做 |
| 语义-客观 | cmm / graphify | 反应式查询 | 代码/文档客观事实 |
| 语义-主观 | Mem0（Stage 1）| 前摄式铺垫 | 用户/决策/偏好 |

**判定测试**：忘了这条 agent 会不会被纠正？会→Memory；不会但要查→KB；怎么做→Skill；何时→git/tasks。

## 关键设计决策（实证）

1. **复用成熟 MCP，不建网关** —— 消费方是 agent，MCP 即接口（`add-code-multimodal-kb` 决策1）
2. **代码 KB = cmm 独占，graphify 不碰代码** —— 靠扩展名分流（`classify_file`），避免重复建图（决策2/3）
3. **NL 检索主路 = BM25**（`search_graph query`）—— 实测推翻原决策4：BM25 broad@5=0.846 > semantic 0.692 > grep 0；semantic 仅作 token-相似兜底；概念词零词重合靠 agent 翻译（决策4 修正）
4. **跨工具 anchoring** —— graphify 概念节点 → 真实标识符 → cmm 定位代码（8/8=100%）
5. **凭据一把解锁** —— 环境 BigModel/GLM key 同时解锁 graphify 建图 + Mem0 抽取 + 文档评测

## Godot 验证基线（真实百万行 C++）

| 指标 | 值 |
|---|---|
| cmm index Godot core/ | 13504 节点 / 38470 边 |
| 代码 BM25 broad@5 | **0.846** |
| graphify 17-doc 子集 | 72 节点 |
| 文档 query recall@5 | **0.70** |
| 跨工具 anchoring 成功率 | **100%** |

## kit 模型（可移植）

- **engineer_demo 仓库 = 便携 kit**（脚本 + runbook + 评测 harness + 规格）
- **`setup-kb.py`** —— 参数化一键接入：`--code/--docs/--name` + LLM 凭据；Win/Mac/Linux 原生
- **目标无关** —— Godot 是参考靶子；任意项目换 `--code/--docs` 即可
- 详见 `docs/deployment-runbook.md`（部署/排错）+ `TODO.md`（路线图）

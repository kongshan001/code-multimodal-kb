## ADDED Requirements

### Requirement: Multimodal ingestion into a knowledge graph

系统 SHALL 通过 graphify 将设计文档、论文、技术资料、图片摄入为持久化知识图谱（实体 / 关系 / 社区），并保留每条事实的来源位置（`source_location`）。

#### Scenario: 多类型文档统一建图

- **WHEN** 摄入一组含 Markdown 设计文档、PDF 论文与图片的语料
- **THEN** graphify 产出统一知识图谱，跨文档的实体与关系被连接，且每个节点 / 边可追溯到来源文件位置

### Requirement: Cross-document graph retrieval

系统 SHALL 支持跨文档的图检索：自然语言查询（BFS 广度 / DFS 路径追踪）、概念间最短路径（path）、节点解释（explain），用于关系梳理而非单纯片段召回。

#### Scenario: 跨文档关系梳理

- **WHEN** 提问涉及分布在多篇文档中的两个概念之间的关系
- **THEN** 返回连接两者的图路径（节点 / 边），并标注每个跳点的来源文档位置

#### Scenario: 概念间最短路径

- **WHEN** 调用 path 查询两个概念
- **THEN** 返回它们在图中的最短路径及沿途节点说明

### Requirement: Incremental graph update

系统 SHALL 在文档变更时只重新抽取新增 / 变更文件（graphify `--update`），而非全量重建。

#### Scenario: 文档增量更新

- **WHEN** 某文档被修改
- **THEN** 仅该文件被重新抽取并入图，未变更文档不重复处理，已有缓存被复用

### Requirement: Source citation

系统 SHALL 在检索结果与回答中提供来源引用，可定位回原文档的具体位置（`source_location`）。

#### Scenario: 引用回溯到原文档

- **WHEN** 基于多模态图生成回答
- **THEN** 每条引用包含来源文档与位置，可跳转到原文档对应处

### Requirement: Provenance separation for inline code

文档内嵌代码块（markdown code fence / 伪代码 / SQL）SHALL 不被抽成与真实源码混淆的代码符号节点；被抽取的实体 SHALL 标注来源类型，使「文档示例」与「真实代码」可区分（审核 M6）。

#### Scenario: 文档代码块不污染图

- **WHEN** 一篇设计文档含 ```python 代码示例
- **THEN** graphify 不把这些代码符号当作领域实体入图，或给它们标 `provenance=doc_inline_code`，引用回溯跳到文档位置而非真实源码

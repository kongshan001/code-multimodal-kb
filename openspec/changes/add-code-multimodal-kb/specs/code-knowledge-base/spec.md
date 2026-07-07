## ADDED Requirements

### Requirement: AST-aware code chunking

系统 SHALL 使用 tree-sitter 按语法边界（函数 / 类 / 方法）将源码解析为符号节点（而非固定字符窗口切片），并保留符号元数据（符号名、类型、文件路径、起止行）。

#### Scenario: 切片落在语法边界上

- **WHEN** 索引一个含若干函数的源文件
- **THEN** 每个 chunk 对应一个完整函数/类/方法，不跨越函数体中部截断

#### Scenario: 保留符号元数据

- **WHEN** 完成一个文件的切片
- **THEN** 每个 chunk 携带符号名、符号类型、文件路径与起止行号，可被检索结果引用

### Requirement: Symbol-level structural retrieval

系统 SHALL 对代码库提供结构化符号检索（经知识图谱：符号名、类型、调用链、引用关系），并支持按符号类型、路径过滤。

#### Scenario: 自然语言定位符号

- **WHEN** 用户提问「重试 / 退避逻辑在哪里」
- **THEN** 返回相关函数及其文件:行号，命中包含实际处理 retry/backoff 的符号

#### Scenario: 精确标识符命中

- **WHEN** 查询包含精确标识符（如类名 `OrderService`）
- **THEN** 经类型解析准确定位该符号，并能给出其调用方与被调用方

### Requirement: Cross-repository code Q&A

系统 SHALL 支持跨多个仓库的自然语言代码问答，回答 MUST 附带可点击的源码引用（文件:行号 + 符号）。

#### Scenario: 跨仓库回答带引用

- **WHEN** 对分布在两个仓库的调用链提问
- **THEN** 回答包含来自两个仓库的源码引用，且引用准确指向被检索到的符号

### Requirement: Incremental re-indexing

系统 SHALL 在代码变更时只重新索引受影响的文件，而非全量重建。

#### Scenario: 文件变更触发增量

- **WHEN** 某文件被修改并提交
- **THEN** 仅该文件及其依赖符号被重新解析并入图，未变更文件不重复处理

### Requirement: Cross-tool code location via concept anchoring

当 NL 问题指向文档中的概念时，系统 SHALL 支持跨工具定位：经 graphify 在文档图锚定到具名实体后，由 codebase-memory-mcp 定位其代码实现。

#### Scenario: 设计概念定位到代码

- **WHEN** 提问「架构文档写的订单状态机，代码在哪实现」
- **THEN** 先经 graphify 在文档图命中 `OrderStateMachine` 概念节点，再由 codebase-memory-mcp 定位该符号的代码实现与调用链

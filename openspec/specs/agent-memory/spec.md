# agent-memory Specification

## Purpose

定义 agent 的"记忆"为独立于 KB（cmm / graphify）、skills、git 的一层，承载关于用户 / 工作方式 / 决策的主观事实。本层负责按归属规则路由每一条候选事实、为记忆附分类标记、前摄式召回以防已知错误、对注入设容量上限、并让关键决策可回溯其情景源。客观层（代码符号 / 调用链 / 文档正文）不进入记忆层，跨层协作走"锚定"模式。

## Requirements

### Requirement: Distinct memory layer with ownership rules

系统 SHALL 把"记忆"作为独立于 KB / skills / git 的一层，并按归属规则路由每一条候选事实：关于代码/文档的客观事实 → KB（cmm/graphify）；如何做某类事 → skills；何时发生何事 → git/tasks；关于用户/工作方式/决策的主观事实 → Memory。

#### Scenario: 判定测试决定归属

- **WHEN** 出现一条候选事实"忘了它 agent 会不会做出用户必须纠正的事"
- **THEN** 若答"会"则进入 Memory（主观层），否则按客观/程序/事件分别路由到 KB/skills/git，避免主观事实污染 KB 检索

#### Scenario: 记忆不吞并客观层

- **WHEN** 一条事实属于"代码/文档本身说了什么"
- **THEN** 该事实 MUST 路由到 KB（cmm/graphify），Memory 层 MUST NOT 重复存储其内容

### Requirement: Subjective memory classification

系统 SHALL 为每条记忆附类型标记，类型限定为 `user`（用户是谁）、`feedback`（用户给的工作方式指导）、`project`（进行中的工作/目标/约束）、`reference`（外部资源指针）之一，便于召回过滤与生命周期管理。

#### Scenario: 落盘带类型

- **WHEN** 捕获一条新记忆（如"用户偏好全局工具共享"）
- **THEN** 该记忆 MUST 携带上述四类之一的标记，且无匹配类型时被拒绝入库

### Requirement: Proactive recall to prevent mistakes

系统 SHALL 以"前摄式铺垫"方式召回记忆——在新会话/新任务开始时主动注入相关记忆以防 agent 犯已知会被纠正的错，而非仅在用户提问时被动查询。

#### Scenario: 新会话铺垫相关记忆

- **WHEN** 一个新会话启动且存在与当前项目相关的偏好/决策记忆
- **THEN** 相关记忆 MUST 被注入上下文（Stage 0 全量受控注入；Stage 1 按相关性召回），使 agent 在未被告知的情况下遵守既有偏好

### Requirement: Memory capacity discipline

系统 SHALL 对受控注入的记忆索引（如 MEMORY.md）设容量上限，超出时按相关性/时效降级为按需召回，避免随事实增长无限膨胀上下文。

#### Scenario: 索引超限降级

- **WHEN** 注入索引的事实条数/体积超过上限
- **THEN** 系统 MUST 将低相关/过时条目移出全量注入、改为按需召回，保持注入体积有界

### Requirement: Episodic traceability

系统 SHALL 让主观记忆中的关键决策可指回其情景源（git commit / tasks 条目），使 agent 能回答"我们何时、为何定了这件事"。

#### Scenario: 决策记忆带情景锚

- **WHEN** 捕获一条决策型记忆（如"决定复用 Mem0 而非自建"）
- **THEN** 该记忆 MUST 附带指向对应 git commit 或 tasks 条目的引用，便于回溯事件脉络

### Requirement: Relevance-based recall

系统 SHALL 提供基于语义相关性的记忆召回（向量相似 + 实体/关系图），替代无条件全量注入，使召回结果与当前任务相关且有界。

#### Scenario: 按相关性召回而非全量

- **WHEN** 当前任务涉及某主题而记忆库已积累大量事实
- **THEN** 系统 MUST 返回与该主题语义相关的少量记忆子集，而非全量记忆

#### Scenario: 实体去重与合并

- **WHEN** 新记忆与已存记忆描述同一实体/事实
- **THEN** 系统 MUST 合并而非重复入库，保持记忆库无冗余

### Requirement: Scope boundary (subjective only)

系统 MUST NOT 在记忆层存储代码符号/调用链或文档正文内容（这些归 cmm/graphify）；跨层协作 SHALL 走"锚定"模式——在文档图锚定概念、抽取真实标识符后交 KB 定位。

#### Scenario: 拒绝存入客观内容

- **WHEN** 试图把一段代码调用链或文档原文写入记忆层
- **THEN** 系统 MUST 拒绝，并路由到对应 KB 工具

#### Scenario: 跨层锚定定位

- **WHEN** 记忆引用了文档中的某概念且需定位其代码实现
- **THEN** 经 graphify `source_location` 抽出真实代码标识符后交 cmm 定位，记忆层自身不持有代码内容

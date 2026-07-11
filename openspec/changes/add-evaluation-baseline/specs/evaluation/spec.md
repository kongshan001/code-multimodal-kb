## ADDED Requirements

### Requirement: Reproducible evaluation harness

系统 SHALL 提供一个可复现的评测 harness（pytest 套件），封装"调 subject 工具（cmm / graphify / Mem0）→ 收集 (query, 检索/图结果, gold) → 算指标"，并在评测报告中记录锁定项（`temp=0` + 固定 LLM 模型 + 工具版本），使跨设备 / 跨时间分数可比。

#### Scenario: 锁版本可复现

- **WHEN** 在两台不同设备上对同一 subject 跑同一评测
- **THEN** 在锁定项一致时，分数差异落在可解释范围内，且报告附锁定项清单

#### Scenario: 一个 harness 测三 subject

- **WHEN** 对 code / doc / memory 三个 subject 分别评测
- **THEN** 三者共用同一 harness 与 ground-truth 哲学，仅指标与 gold 来源按 subject 切换

### Requirement: Code retrieval quality baseline

系统 SHALL 用 RepoBench-R（recall@k / nDCG@10）+ SWE-Lancer-Loc（NL→文件/函数命中率）建立代码检索质量基线，且**代码侧评测 SHALL 不调 LLM**（结构指标 + PR 反挖 gold），凭据缺席时仍可运行。

#### Scenario: 代码侧零凭据可跑

- **WHEN** 本机无 LLM 凭据时对 cmm 跑代码侧评测
- **THEN** 评测正常产出 recall@k / 命中率，不因缺凭据而失败

#### Scenario: 命中率达标

- **WHEN** 在 SWE-Lancer-Loc 216 条 NL→定位上评测
- **THEN** 文件/函数命中率不低于首跑设定的基线阈值

### Requirement: Symbol and call-chain graph metrics

系统 SHALL 提供图检索专用自建指标——Symbol-Level Hit@k、Call-Chain Edge Recall、Path Precision@k（gold 来自静态调用图），测 codebase-memory-mcp 真正关心的"定位符号 + 调用链"，而非仅 chunk 召回。

#### Scenario: 调用链 gold 对照

- **WHEN** 对某函数的调用链查询结果用静态调用图 gold 评分
- **THEN** 返回 Call-Chain Edge Recall 分数，反映真实调用边命中比例

### Requirement: Cross-document retrieval threshold

系统 SHALL 对文档侧跨文档检索建立 recall 基线；**recall@5 < 0.6 时 SHALL 触发**补文档向量索引的评估（凭据门控——依赖 graphify 文档图）。

#### Scenario: recall 不达标触发行动

- **WHEN** 文档侧 recall@5 < 0.6
- **THEN** 评测报告标记该指标未达标，并输出"评估补文档向量索引"的触发动作

### Requirement: Extraction quality sampling

系统 SHALL 用独立模型（非 graphify 抽取模型）抽样打 entity / relation / claim 准确率；准确率 < 0.7 时 SHALL 触发调抽取 prompt / 换模型（凭据门控）。

#### Scenario: 抽取质量独立评判

- **WHEN** 对 graphify 抽取出的实体/关系抽样评判
- **THEN** 评判模型 ≠ 抽取模型（防 Preference Leakage），并产出准确率分数

### Requirement: Memory recall quality

系统 SHALL 对记忆层主观记忆召回建立 recall@k 基线，并度量实体去重正确率与注入体积收敛（凭据门控——依赖 Memory Stage 1 Mem0）。

#### Scenario: 召回相关且有界

- **WHEN** 对一个主题召回记忆
- **THEN** 返回相关子集（recall@k 达标）、无重复实体（去重正确率达标）、注入体积不随库增长无界膨胀

### Requirement: Boundary routing accuracy

系统 SHALL 度量 D1 边界归属规则的 routing 准确率——构造覆盖客观 / 程序 / 事件 / 主观四类的标注集，验证候选事实被正确路由；准确率低于基线时 SHALL 触发补 D1 规则。

#### Scenario: 四类路由命中

- **WHEN** 对标注集里的候选事实逐条判定归属
- **THEN** 四类路由准确率均不低于设定基线，未达标的类别在报告中标出

### Requirement: Threshold-gated corrective action

评测 SHALL 为每个指标绑定阈值与触发动作；不达标项 SHALL 在评测报告里明确标记并输出对应改进动作，使评测驱动改进而非仅评分。

#### Scenario: 报告输出触发动作

- **WHEN** 某项指标低于其阈值
- **THEN** 评测报告对该指标标记"未达标"并附触发动作（如补向量 / 调 prompt / 加缓存），而非仅给分数

### Requirement: Ground truth without LLM-judge circularity

代码侧 gold SHALL 经真实 merged PR 反挖（NL issue→git diff→gold symbols→静态调用图 gold 链）+ LSP goto-def 执行式反查生成，**避免 LLM 评 LLM 循环**；文档 / 记忆侧 gold 生成模型 SHALL ≠ 被测抽取模型。

#### Scenario: 代码侧零 LLM judge

- **WHEN** 生成代码侧 ground truth
- **THEN** gold 完全来自 PR diff + 静态调用图 + LSP 反查，不调用任何 LLM 作裁判

### Requirement: Agent-level value differential (system vs no-system)

系统 SHALL 度量"配备 vs 不配备知识库 / 记忆系统"对 agent 任务的**端到端**价值差——含 token 用量、答案准确度、效率（步数 / 耗时），证明系统的边际价值，而非仅评检索层 recall。准确度与端到端 token 评测 SHALL 受 LLM 凭据门控；凭据缺席时 SHALL 仍能产出"context token 压缩比 + 注入命中"代理指标（Stage 0），并明确标注其不等于 agent 答对率。

#### Scenario: token 用量与准确度对照

- **WHEN** 对同一批代码定位题，分别在"有 cmm 代码 KB"与"朴素 grep 基线"下跑 agent
- **THEN** 报告两臂的 token 用量差（压缩比）、答案准确度差、效率差，量化系统价值

#### Scenario: 零凭据代理指标

- **WHEN** LLM 凭据缺席
- **THEN** 仍能量化 context token 压缩比 + 注入命中 gold（Stage 0），并在报告标注"非 agent 答对率"边界（Stage 1 凭据门控）

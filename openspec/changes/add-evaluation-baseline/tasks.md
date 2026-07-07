## 1. 评测 harness 骨架（零凭据）

- [x] 1.1 搭 pytest harness 骨架 + 封装"调 subject 工具（cmm / graphify / Mem0）→ 收集 (query, 检索/图结果, gold)"的统一接口 → 验证：`test_cmm_roundtrip` 通过（真实调 cmm list_projects 返回含 graphify 的项目列表）；harness `run_dataset` 收集记录通过
- [x] 1.2 锁可复现项（`temp=0` + 固定 LLM 模型 + 工具版本 graphify/cmm/Mem0）写入 harness 配置，评测报告自动附锁定项清单 → 验证：`test_stamp_adds_lockfile_to_report` + `test_detect_lockfile_runs` 通过（报告含 lockfile 字段 + 本机 cmm 版本已探测）

## 2. 代码侧评测（零凭据 · 主轨道 · 接管 add-code-multimodal-kb §5 代码部分）

- [ ] 2.1 拉 RepoBench-R + SWE-Lancer-Loc 数据集（CN 走代理/ghproxy）→ 验证：数据集落盘可加载。注：首基线已用 architecture-derived gold 跑通（见 2.2）；RepoBench HF 需 token(401) + completion/issue→file 范式与 cmm 符号检索不直接对口，留作 scale-up
- [x] 2.2 实现 recall@k / nDCG@10（RepoBench-R）+ NL→文件/函数命中率（SWE-Lancer-Loc）→ 指标实现 + 合成验证（6 测试）**且已在真实目标仓库跑出基线**：graphify strict@5=0.762；**Godot core/（13504 节点真实 C++）strict@5=0.0 / broad@5=0.692**（双指标：strict 在大 C++ 因粒度错配失效，broad+归一化为公平刻度）。报告 `eval/reports/code-baseline-{graphify,godot}-findings.md`。注：gold 用 architecture-derived（非 RepoBench 全量 / PR 反挖），见 2.1/2.4
- [x] 2.3 自建图指标 Symbol-Level Hit@k / Call-Chain Edge Recall / Path Precision@k（gold 来自 cmm 静态调用图）→ 指标实现完成 + 合成验证（`test_graph_metrics` 6 项，已知调用链算分正确）；注：接 cmm 真实静态调用图 gold 待 2.1 数据集 + 集成
- [ ] 2.4 PR 反挖 ground truth（NL issue→git diff→gold symbols→gold 调用链）+ LSP goto-def 执行式反查，零 LLM judge → 验证：gold 生成全程不调 LLM。注：首基线暂用 cmm `get_architecture` 实测符号的 architecture-derived gold 替代（零 LLM，已跑出 recall@5=0.762）；PR 反挖需目标仓库 git 历史，留作 gold 硬化 scale-up
- [ ] 2.5 CoIR 子集向量基线对照（cosqa+codesearchnet+stackoverflow，~10–15%，仅防退化）→ 验证：跑出对照分数不与榜单比

## 3. 文档侧评测（🔴 卡凭据 · 与 doc-side KB 共享解锁 · 接管 §5 文档部分）

- [ ] 3.1 前置：LLM 凭据就位 + graphify 文档图已建（依赖 add-code-multimodal-kb §3）
- [ ] 3.2 DeepEval faithfulness / answer relevancy / G-Eval（评 graphify 文本节点→答案）→ 验证：跑出文档答案质量分
- [ ] 3.3 复刻 MS GraphRAG LLM grader（comprehensiveness/diversity/empowerment head-to-head vs 朴素 RAG）→ 验证：head-to-head 评分可跑
- [ ] 3.4 抽取质量：独立模型（≠ graphify 抽取模型）抽样打 entity/relation/claim → 验证：评判模型与抽取模型不同
- [ ] 3.5 外部 held-out：GraphRAG-Bench / WildGraphBench 子集 → 验证：在 held-out 上跑出分数

## 4. 记忆侧评测（🔴 卡凭据 · 依赖 Memory Stage 1 Mem0 · 接管 add-agent-memory §4）

- [ ] 4.1 前置：Mem0 已接入并迁移现有记忆（依赖 add-agent-memory §2）
- [ ] 4.2 recall@k + 实体去重正确率 + 注入体积收敛 → 验证：对主题召回跑出相关性/去重/体积指标
- [ ] 4.3 边界路由准确率：构造 4 类标注集（客观/程序/事件/主观各若干）+ 路由 gold，验 D1 → 验证：四类路由准确率达标

## 5. 阈值门禁 + 报告 + 文档化

- [ ] 5.1 实现阈值门禁表（每指标绑阈值 + 触发动作），不达标项报告标记并输出改进动作 → 验证：注入一个低分样本，报告正确标记 + 输出动作
- [ ] 5.2 代码侧首跑出基线后，回填"设定基线"阈值（design Open Question 1）→ 验证：阈值字段有数
- [ ] 5.3 评测报告模板 + 跑评测步骤文档化（含数据集来源、锁定项、阈值）→ 验证：新人照文档能复现一次代码侧评测
- [ ] 5.4 在 add-code-multimodal-kb §5 + add-agent-memory §4 tasks.md 加归属行指向本变更 → 验证：两变更评测 task 标注"→ add-evaluation-baseline"

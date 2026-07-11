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
- [ ] 3.2 DeepEval faithfulness / answer relevancy / G-Eval（评 graphify 文本节点→答案）→ 验证：跑出文档答案质量分。注：复刻版脚本就绪（`eval/run_doc_quality.py` faithfulness/relevancy + `eval/llm.py` BigModel judge，免装 deepeval）；**实跑被 BigModel key 持续 429 限流阻塞**，待配额恢复后跑分数
- [ ] 3.3 复刻 MS GraphRAG LLM grader（comprehensiveness/diversity/empowerment head-to-head vs 朴素 RAG）→ 验证：head-to-head 评分可跑。注：head-to-head 判官已写进 `run_doc_quality.py`（graphify 答 vs naive grep，BigModel 判谁更全面）；同被 429 阻塞
- [ ] 3.4 抽取质量：独立模型（≠ graphify 抽取模型）抽样打 entity/relation/claim → 验证：评判模型与抽取模型不同
- [ ] 3.5 外部 held-out：GraphRAG-Bench / WildGraphBench 子集 → 验证：在 held-out 上跑出分数

## 4. 记忆侧评测（召回+路由零凭据已完成 · 答案质量仍卡 LLM judge · 接管 add-agent-memory §4）

> 2026-07 修订：Mem0 → MemPalace（add-agent-memory 已归档）。召回 + 路由两层用本地 embedding / 规则，**零 LLM**，已跑出基线；「记忆答案质量」（召回的 drawer 是否真答对问题）需 LLM judge，仍卡凭据，与 §3 文档侧同一道墙。

- [x] 4.1 前置：MemPalace 已接入并 mine 现有记忆（依赖 add-agent-memory §2，已归档）→ 验证：MemPalace 3.5.0 接入 + agent 内 `mempalace_search` 可调（commit aaf81e6）；palace 1485 drawers（memory 文件 4 + 会话碎片 1481）✓
- [x] 4.2 recall@k + 实体去重正确率 + 注入体积收敛 → 验证：`bench run memory` 跑 15 query → **hit@5=0.933 / hit@1=0.80 / recall@5=0.900**；memory 文件召回干净（8/8）、会话碎片偏松散（6/7）；去重 unique_source@5=**0.613**（同源碎片 ~39%，召回无碍、多样性弱）；注入体积有界（search ≤10 / MEMORY.md ≤20）。归档 `reports/archive/20260711T104332Z-mempalace-engineer_demo.json` + 报告 `reports/memory-baseline-2026-07.md` ✓
- [x] 4.3 边界路由准确率：构造 4 类标注集（客观/程序/事件/主观各 3–4 条）+ 路由 gold，验 D1 → 验证：`routing.py` cascade 对 13 条候选事实 **总体准确率 1.0**（四类各 1.0，零错路由）；「决策+日期」正确归 subjective 与 CLAUDE.md 决策锚一致。标注集固化为 `test_gold_memory_snapshot` 回归门禁。诚实边界（集与规则同源，泛化需扩标）见报告 §3 ✓

## 5. 阈值门禁 + 报告 + 文档化

- [ ] 5.1 实现阈值门禁表（每指标绑阈值 + 触发动作），不达标项报告标记并输出改进动作 → 验证：注入一个低分样本，报告正确标记 + 输出动作
- [ ] 5.2 代码侧首跑出基线后，回填"设定基线"阈值（design Open Question 1）→ 验证：阈值字段有数
- [ ] 5.3 评测报告模板 + 跑评测步骤文档化（含数据集来源、锁定项、阈值）→ 验证：新人照文档能复现一次代码侧评测
- [x] 5.4 在 add-code-multimodal-kb §5 + add-agent-memory §4 tasks.md 加归属行指向本变更 → 已在两变更 §5/§4 header 加"归属 add-evaluation-baseline"注，消除 ~15 个重复评测 task 的歧义

## 6. Agent 级 A/B 价值 benchmark（端到端：有系统 vs 无系统）

> 新增维度：§2–4 测**检索层** recall；本节测**agent 层**——配不配我们的系统，agent 把活干成/干省的差距。
> 三指标：① token 用量 ② 准确度 ③ 效率（步数/耗时）。分两 stage：
> **Stage 0 token 代理**（零 LLM，现在跑）/ **Stage 1 全 agent A/B**（需 LLM key，凭据门控）。
> 复用 `gold_godot`（代码定位题，符号 gold，零 LLM 可判分）。

- [x] 6.0 spike：cmm Godot 索引首次冷启动 search 报 "project not found" → 实测为瞬时状态（mem.init 首次重装项目注册表），暖后 search_code/search_graph 均正常；非阻塞 ✓
- [x] 6.1 Stage 0 token 代理 runner：对 gold_godot 26 题量 KB（cmm bm25 top-5）vs 朴素 grep（文件名 / grep+读文件）的 context token 压缩比 + KB 注入命中 gold 符号（kb_hit@5）→ 验证：`bench run ab` 真跑 → **mean 压缩 12.71×（中位 15.5×）/ kb_hit@5=0.846（与 broad@5 一致）/ 朴素 grep 盲区 7/26（KB 救回 5）**；归档 `reports/archive/20260711T110417Z-ab-value-stage0-godot-stage0.json` ✓
- [x] 6.2 Stage 0 测试 + cli `run ab` 子命令 + 报告 → 验证：`test_ab_value.py` 2 测试绿（全 29 passed）；cli `run ab` 归档通；报告 `reports/ab-value-baseline-2026-07.md`（含 6 条诚实边界，标注 Stage 0≠agent 答对率）✓
- [x] 6.3 Stage 1 agent A/B harness（**实施+跑通**，凭据走本地 cc-connect zhipu/BigModel anthropic 端点，不入库）→ `ab_agent.py`（可控 ReAct loop：temp=0 + 臂工具集 + max-steps + 429 退避 + token 累计 + 收敛纪律 prompt）+ `run_ab_agent.py`（判分：终答命中 + 检索命中双口径）+ `test_ab_agent.py`（3 测试）。**真跑 26×2×1**：准确度 0.923 并列天花板（baseline grep 已触顶，KB 救回概念题 int to string）；**KB 省 58% token / 2.4× token-per-correct / 步数 −38%**。归档 `...120018Z-ab-agent-stage1...json` + 报告 `ab-agent-stage1-2026-07.md`（v1 弱 prompt 54% truncated 污染→v2 收敛纪律修复，对称改进）✓
- [x] 6.4 三臂扩展（graphify 文档臂）+ 工具注册表复用化 → 加 graphify 第 3 臂跑全 26：doc final 0.346 / retrieval 0.923（**doc→code 锚定 agent 侧缺口**：检索到但 agent 不会转成符号答案，trunc 17/26）；三系统不同层不可互换，印证 D1。归档 `...132516Z-...-doc.json` + 报告 §6。**抽 `ab_tools.py` 注册表**：工具集中管理、臂变数据（ARMS dict），接新 KB 工具=写 executor+register+挂臂，loop/判分/归档不动；`test_ab_tools.py`（4 测试）验注册/解析/扩展 ✓

# 待办事务 / 路线图

> 2026-07-13 快照。已归档（本会话）：`add-bench-targets` / `add-bench-frontend` / `add-benchmark-runner`（主 spec 已同步，5 capability）。
> 活跃：`add-code-multimodal-kb`（9/33）。`add-evaluation-baseline` + `add-agent-memory` 更早归档。

## ✅ 已完成 / 已证明

### 知识库
- **代码 KB**：cmm 吃下 Godot core/（13504 节点）；BM25 broad@5=**0.846**（+22% vs grep）
- **文档 KB**：graphify 建 17-doc 子集图；query recall@5=**0.717**
- **跨工具 anchoring**：文档概念→代码定位 **8/8 = 100%**
- **codegraph**：第二代码 KB 接入（A/B 四臂 + goldgen 枚举）；准确度 **0.962**（四臂最高）

### 记忆层（MemPalace，已替换 Mem0）
- **Stage 0**：D1 四层归属纪律（CLAUDE.md）+ 文件记忆分类/容量/决策锚 ✓
- **Stage 1**：MemPalace 3.5.0 接入 + MCP + mine 2021 drawers + auto-save hooks（⚠️ 后禁用，见下）
- **召回**：hit@5=**0.933** · D1 路由准确率 **1.0** · 去重 unique@5=0.64
- **答案质量**：faithfulness=**0.951** / context_precision=0.360（Ragas 协议）

### 评测 benchmark（`benchmark-runner` + `benchmark-targets` + `bench-frontend` capability）
- **harness**：eval/（指标 + lockfile + 归档留底，64 测试绿）
- **题库配置化**：`targets/<id>/{target.json, problems.json}` 声明式（5 type + 稳定 id + 元数据），替旧 gold_*.py 字面量；`target.local.json` overlay 让引擎可移植（fork 模板）
- **bench CLI**：run code/doc/cross/memory/ab/ab-agent/doc-ragas/memory-quality + list-reports/show/compare（--target = target id）
- **A/B Stage 0**：context 压缩 **12.71×**（KB 省 58% token）
- **A/B Stage 1**：四臂横评 baseline/cmm/doc/codegraph（准确度并列天花板 0.923，codegraph 最准 0.962）
- **答案质量**：文档 faithfulness **0.971** + 记忆 **0.951**（Ragas 协议，LLM-judged）
- **goldgen 扩题**：symbol-driven agent 挖题 + 实证验收 + 人审（候选直写 problems.json status:pending，前端 approve，**废 fold/pending.md**）
- **前端 Gold lab 编辑器**：浏览器内 CRUD 题库（Playwright 验证 round-trip），不自动 git commit
- **bench-dock-target skill**：对接目标工程的 SOP（`.claude/skills/`）
- **Windows 兼容**：subprocess UTF-8（全仓）+ npm CLI `.cmd` 包装器解析
- **工具注册表**：ab_tools.py（接新 KB 零改 loop）

### 前端 + 工具链
- **前端 SPA**（Measurement Lab）：8/8 视图 live（Dashboard/Run/Reports/Detail/Compare/Setup/Onboarding/Gold lab）
- **setup.sh**：一键装环境 + 依赖坑固化
- **流程图**：fireworks-tech-graph（系统架构 / A/B 流程 / goldgen 流程）
- **palace 事故闭环**：Stop hook 非 idempotent → bloat 1485→14605 → 召回 0.933→0.6 → 禁 hook + 重置 → 恢复 0.933

## 🔶 进行中

- **`add-code-multimodal-kb`**（9/33）：代码/文档 KB 规模化 + path/explain 补全

## 📋 已登记延期（独立后续 change）

- **F1 `add-bench-doc-quality-targets`**：`run_doc_quality`/`run_doc_quality_ragas` 的文档语料路径配置化（需扩 `doc.rst_dir` schema + 可能第 6 个 target）
- **F2 `add-scaffold-portable-project-default`**：`web/app.js` `_targetProject` 默认路径（scaffold 能力目录扫描，非 bench）

## 📋 待办（按价值）

### 评测硬化（`add-evaluation-baseline` 已归档，遗留 scale-up）
- [ ] RepoBench-R / SWE-Lancer 全量（§2.1，HF 需 token + 范式适配）
- [ ] PR 反挖 gold（§2.4，比 architecture-derived 更硬）
- [ ] CoIR 向量基线对照（§2.5）
- [ ] 阈值门禁自动化 + 报告模板（§5）

### 答案质量绝对化
- [ ] 第二家族 judge（Claude/OpenAI key）做集成，解锁绝对质量分（当前 GLM 同家族 = 相对值）

### 记忆层运营
- [ ] 等 mempalace 出 idempotent auto-save hook（当前禁用，手动 `mempalace sweep`）
- [ ] palace drawer 抽稀/compress（会话碎片 ~99%，改善去重 + context_precision）

### KB 规模化
- [ ] Godot index scale up：core/ → +scene/+servers/
- [ ] 文档全量：17 → 全 godot-docs（~$27 LLM）
- [ ] 多仓库 / 跨语言验证

## 🚧 阻塞

- **第二家族 judge**：需 Claude/OpenAI key（当前仅 GLM cc-connect）
- **CN 网络**：GitHub/PyPI 走代理（`127.0.0.1:7897`）

## 💡 可选 / 低优

- Zep/Graphiti 时序召回（`add-agent-memory` Stage 2，痛点触发）
- 团队共享部署（中心 MCP server + wing_team 记忆隔离）
- 吞吐压测 harness（当前 benchmark 测质量不测 QPS）

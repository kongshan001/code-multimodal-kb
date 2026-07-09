# 待办事务 / 路线图

> 2026-07-09 快照。三变更：`add-code-multimodal-kb` 9/33 · `add-evaluation-baseline` 4/19 · `add-agent-memory` 4/17。
> 进度详情见各 `openspec/changes/<change>/tasks.md`。

## ✅ 已完成 / 已证明（项目核心命题）

- **代码 KB**：cmm 吃下真实百万行 C++（Godot core/ 13504 节点）；BM25 broad@5=**0.846**
- **文档 KB**：graphify + BigModel 建 Godot 17-doc 子集图（72 节点）；query recall@5=**0.70**
- **跨工具 anchoring**：文档概念→代码定位 **8/8=100%**
- **评测 harness**：`eval/`（指标 + gold + 可复现 lockfile，17 测试绿）
- **design 实证修正**：BM25 主路（非 semantic_query），决策4 已回写
- **凭据墙破**：环境 BigModel/GLM key 一把解锁 graphify + Mem0 + 文档评测
- **跨平台 kit**：`setup-kb.py`（Win/Mac/Linux），1-4+6 步实测零 bug
- **agent 纪律**：CLAUDE.md 铁则（新需求走 OpenSpec）+ 记忆四层归属

## 🔶 进行中 / 待验证

- **Mem0 记忆层（`add-agent-memory` Stage 1）**
  - Docker compose（`deploy/mem0/`）已写，按官方指南 —— ⚠ 未实测（本机无 Docker；用户 Win 暂不支持 Docker）
  - 无 Docker 路线（Ollama + qdrant-local，`deploy/mem0-local/`）—— ✅ **已实测通过**（add→search 闭环，`_test.py`）
- **graphify-mcp 注册**：venv 缺 `mcp` extra（`uv tool install --force graphifyy --with mcp`，网络）；agent 暂用 `graphify query` CLI
- **文档检索 path/explain**（kb task 3.2）：`query` 已验，path/explain 待测

## 📋 待办（按价值）

### 评测硬化（`add-evaluation-baseline`）
- [ ] 4.x 记忆侧评测（依赖 Mem0 落地）
- [ ] PR 反挖 gold（task 2.4）—— 比 architecture-derived gold 更硬
- [ ] CoIR 向量基线对照（task 2.5）
- [ ] 阈值门禁自动化（task 5.1）+ 评测报告模板（5.3）

### KB 规模化
- [ ] Godot index scale up：core/ → +scene/+servers/（压 cmm 内存/耗时）
- [ ] 文档全量：子集 17 → 全 godot-docs（~$27 LLM 成本）
- [ ] 多仓库 / 跨语言验证

### 记忆层（`add-agent-memory`）
- [ ] 2.x Mem0 落地（Docker 或无 Docker 路线，需 Win/Docker 环境验证）
- [ ] Stage 0 纪律实战检验（文件记忆分类/容量/决策锚）

## 🚧 阻塞

- **Mem0 实测**：用户 Win 无 Docker → 需 Docker 环境（Win Docker Desktop / Mac / Linux）验证 compose，或落定无 Docker 路线
- **CN 网络**：GitHub/PyPI 走代理（`127.0.0.1:7897`）；Mem0 `mcp` extra、数据集下载等受其影响

## 💡 可选 / 低优

- Zep/Graphiti 时序召回（`add-agent-memory` Stage 2，痛点触发）
- 其他 agent 适配（Codex/Cursor 已注册 cmm；Mem0/graphify 多 agent 注册）
- UI 可视化（cmm architecture / graphify callflow-html 已有）

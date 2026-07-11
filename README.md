# engineer_demo — agent 知识库 + 记忆（便携 kit）

给 agent（Claude Code 等）接入 **知识库**（代码 cmm + 文档 graphify）与 **记忆**（Mem0），复用成熟 MCP、不建网关。**跨平台 `setup-kb.py` 一键接入任意项目**（Win/Mac/Linux）。Godot 是参考靶子（已验证）。

## 现状（2026-07-09）

KB 在真实 Godot 上**双侧 + 跨工具端到端**验证：

| 指标 | 值 |
|---|---|
| 代码检索（cmm BM25）broad@5 | **0.846** |
| 文档检索（graphify query）recall@5 | **0.70** |
| 跨工具 anchoring（文档概念→代码定位）| **100%** |

凭据墙已破（环境 BigModel/GLM key）；eval harness 17 测试绿；跨平台 kit 已实测。

## 快速接入（一键 · 跨平台）

```bash
git clone <repo> && cd engineer_demo
python3 setup-kb.py --code <代码目录> --docs <文档目录> --name <项目名> [--no-memory]
```

详见 [deployment-runbook.md](docs/deployment-runbook.md)。Mem0 需 Docker（Win 无 Docker 走 §D 无 Docker 路线）。

## 文档索引

| 文档 | 内容 |
|---|---|
| [docs/architecture.md](docs/architecture.md) | **框架总览**：组件 / 数据流 / 记忆四层 / 设计决策 / Godot 验证 |
| [docs/deployment-runbook.md](docs/deployment-runbook.md) | **部署/排错**：A 代码 / B 文档 / C 评测 / D 记忆 + 快速接入 |
| [docs/benchmark-runbook.md](docs/benchmark-runbook.md) | **benchmark CLI**：`bench` 子命令 / 归档留底 / 读报告 / 复现 / 测试 |
| [TODO.md](TODO.md) | **路线图**：已证明 / 进行中 / 待办 / 阻塞 |
| [CLAUDE.md](CLAUDE.md) | agent 纪律：OpenSpec 铁则 + 记忆四层归属判定 |
| [eval/README.md](eval/README.md) | 评测 harness（指标 / gold / 可复现 lockfile）|
| `openspec/changes/<change>/` | 规格：proposal / design / specs / tasks |

## 变更（OpenSpec）

| 变更 | 进度 | 主题 |
|---|---|---|
| `add-code-multimodal-kb` | 9/33 | 代码 KB + 文档 KB（双侧已验证 Godot）|
| `add-evaluation-baseline` | 4/19 | 评测横切 capability（harness 三路 + 跨工具）|
| `add-agent-memory` | 4/17 | agent 记忆（Stage 0 ✅ / Stage 1 Mem0 待验）|

## 关键边界 / 约束

- **记忆 vs KB 金句**：*忘了这条 agent 会不会被纠正？会→Memory；不会但要查→KB；怎么做→Skill；何时→git*（详见 CLAUDE.md）
- **NL 代码检索主路 = BM25**（实证修正 design 决策4，非 semantic_query）
- 改动提交 main + push（带 Co-Authored-By）；新需求走 OpenSpec（铁则）

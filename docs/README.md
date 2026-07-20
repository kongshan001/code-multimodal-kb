# 文档索引

> 本仓库所有文档的**单一入口**。按用途分组，每篇标明给谁看、什么时候看。

---

## 🚀 快速上手

| 文档 | 内容 | 给谁 |
|---|---|---|
| [README.md](../README.md)（根目录） | 项目简介 + clone 后 3 步上手 | 所有人 |
| [bench.yaml.example](../bench.yaml.example) | 配置模板（cp 为 bench.yaml，改模型/key/路径） | 跑 benchmark 的人 |

## 🏗️ 架构

| 文档 | 内容 | 给谁 |
|---|---|---|
| [architecture.md](architecture.md) | 系统总览：KB（代码+文档）+ 记忆 + 评测，四层归属 | 理解全局 |
| [diagrams/](diagrams/README.md) | 流程图 4 张（总览 + agent loop + target 布局 + arms×tools） | 可视化理解 |

## 📊 Benchmark 评测

| 文档 | 内容 | 给谁 |
|---|---|---|
| [benchmark-runbook.md](benchmark-runbook.md) | bench CLI 手册：怎么跑、怎么读报告、报告结构 | **跑 benchmark 必读** |
| [ab-agent-internals.md](ab-agent-internals.md) | agent loop 源码级拆解（提示词/轮次/token，含两 engine） | **外部评审 / 深度理解** |
| [ab-agent-optimization-roadmap.md](ab-agent-optimization-roadmap.md) | 优化路线图（done/todo/否决，按优先级排） | 决定下一步做什么 |
| `eval/reports/agent-compare/*/analysis.md` | 每次跑的分析报告（结论 + 诚实边界 + 逐题分化） | 看具体跑分结论 |

## 🔧 运维

| 文档 | 内容 | 给谁 |
|---|---|---|
| [deployment-runbook.md](deployment-runbook.md) | 代码 + 文档 KB 部署（cmm/graphify/mempalace 安装） | 部署/运维 |
| [frontend-guide.md](frontend-guide.md) | bench web 前端使用说明 | 用界面跑/看结果 |
| [windows-compatibility.md](windows-compatibility.md) | Windows 中文系统编码/路径踩坑 | Windows 用户 |

## 📐 规格（OpenSpec）

| 位置 | 内容 |
|---|---|
| [openspec/specs/](../openspec/specs/) | 6 个 capability spec：benchmark-runner / targets / agent-compare / evaluation / bench-frontend / agent-memory |
| [openspec/changes/archive/](../openspec/changes/archive/) | 历史变更归档（含 migrate-ab-agent-to-claude-sdk 等） |

## 🤖 Skills（bench 操作流程）

| Skill | 触发场景 |
|---|---|
| `bench` | benchmark 单一入口——"benchmark 我的工程"先走它，判断+路由 |
| `bench-dock-target` | 对接新工程到 benchmark（建 target/索引/题） |
| `bench-author-problems` | 出题→AI 审核→人审→跑分→报告一条龙 |

---

## 文档间关系

```
README.md（上手）
  └→ docs/README.md（本索引）
       ├→ benchmark-runbook.md（怎么跑）
       │    └→ ab-agent-internals.md（引擎怎么工作）
       │         └→ ab-agent-optimization-roadmap.md（还能怎么优化）
       ├→ architecture.md（全局架构）
       │    └→ diagrams/（可视化）
       └→ deployment-runbook.md（怎么部署）
```

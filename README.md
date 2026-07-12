# engineer_demo — agent 知识库 + 记忆 + 评测 + 前端

给 agent（Claude Code 等）接入 **知识库**（代码 cmm + 文档 graphify）、**记忆**（MemPalace）、**评测 benchmark**（检索/agent A/B/答案质量）+ **前端可视化**（Measurement Lab）。复用成熟 MCP、不建网关。Godot 是参考靶子（端到端实测）。

## 现状（2026-07-12 · 端到端全验证）

| 层 | 指标 | 值 |
|---|---|---|
| 代码检索（cmm BM25）| broad@5 | **0.846** |
| 文档检索（graphify）| recall@5 | **0.717** |
| 跨工具 anchoring | 成功率 | **100%**（8/8）|
| 记忆召回（MemPalace）| hit@5 | **0.933** · 路由准确率 **1.0** |
| agent A/B Stage 0 | context 压缩 | **12.71×**（KB 省 58% token）|
| agent A/B Stage 1 | 四臂准确度 | baseline 0.923 · cmm 0.923 · codegraph **0.962** |
| 文档答案质量 | faithfulness | **0.971**（Ragas 协议）|
| 记忆答案质量 | faithfulness | **0.951** |

**pytest 48 passed · 归档 16 份 · E2E 12 CLI + 8 前端视图全通 · 零失败。**

## 快速接入

```bash
git clone https://github.com/kongshan001/code-multimodal-kb.git && cd engineer_demo
./setup.sh all                    # 装环境（Python + 4 工具 + 渲染 + 凭据检查）
python -m eval.cli web            # 起前端 → http://127.0.0.1:8765
# → 浏览器开 Dashboard / Run console / Setup 体检 / Gold lab
```

命令行同样可用：`python -m pytest eval/tests/`（零依赖测试）→ `python -m eval.cli run code/memory/ab/...`（跑评测）。

## 文档索引

| 文档 | 内容 |
|---|---|
| [docs/architecture.md](docs/architecture.md) | **框架总览**：组件 / 数据流 / 记忆四层 / 设计决策 |
| [docs/deployment-runbook.md](docs/deployment-runbook.md) | **部署/排错**：A 代码 / B 文档 / C 评测 / D 记忆 / E 离线 + hook 事故复盘 |
| [docs/windows-compatibility.md](docs/windows-compatibility.md) | **Win 兼容**：cp936 编码坑（read_text/print/subprocess）+ 修复铁律 + 平台差异 |
| [docs/benchmark-runbook.md](docs/benchmark-runbook.md) | **benchmark CLI**：`bench` 子命令 / goldgen 扩题 / 归档 / 读报告 / 复现 |
| [docs/diagrams/](docs/diagrams/README.md) | **流程图**（fireworks-tech-graph）：系统架构 / A/B 流程 / goldgen 流程 |
| [docs/frontend-guide.md](docs/frontend-guide.md) | **前端使用说明**：起服务 / 8 视图详解 / 典型工作流 / 排错 / CLI 对应 |
| [web/](web/index.html) | **前端可视化**（Measurement Lab）：Dashboard / Run / Setup / Onboarding / Gold lab |
| [eval/](eval/README.md) | **评测 harness**：指标 / gold / 可复现 lockfile / 工具注册表 |
| [TODO.md](TODO.md) | **路线图**：已证明 / 进行中 / 待办 |
| [CLAUDE.md](CLAUDE.md) | agent 纪律：OpenSpec 铁则 + 记忆四层归属判定 |

## OpenSpec 变更

| 变更 | 状态 | 主题 |
|---|---|---|
| `add-bench-frontend` | **进行中**（15/16）| 前端可视化层（8/8 视图 live，Measurement Lab）|
| `add-benchmark-runner` | 进行中 | bench CLI 骨架（已完成核心）|
| `add-code-multimodal-kb` | 进行中 | 代码 KB + 文档 KB |
| ~~`add-evaluation-baseline`~~ | **已归档** | 评测 capability（§1-2,4,6 已交付 + 同步主 spec）|
| ~~`add-agent-memory`~~ | **已归档** | agent 记忆 Stage 0+1（MemPalace 接入 + 同步主 spec）|

## 关键边界 / 约束

- **记忆 vs KB 金句**：*忘了这条 agent 会不会被纠正？会→Memory；不会但要查→KB；怎么做→Skill；何时→git*
- **NL 代码检索主路 = BM25**（实证修正 design 决策4，非 semantic_query）
- **LLM-judged 分是相对值**（GLM 生成+判 = 同家族 self-preference）；grounded 分（recall/symbol match）是绝对值
- **auto-save hook 非 idempotent**——全局 Stop hook 会把别项目会话反复 mine 进 palace 致召回退化（0.933→0.6 实测事故，已修复+记录 runbook §D.4-D.6）
- **benchmark 驱动改进**：测→诊→改→重测闭环（palace 事故是范例：发现 bloat→诊断 hook→禁用+重置→召回恢复 0.933）
- 改动提交 main + push（带 Co-Authored-By）；新需求走 OpenSpec（铁则）

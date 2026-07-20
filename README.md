# engineer_demo — agent 知识库 + 记忆 + 评测 + 前端

给 agent（Claude Code 等）接入 **知识库**（代码 cmm + 文档 graphify）、**记忆**（MemPalace）、**评测 benchmark**（检索/agent A/B/答案质量）+ **前端可视化**（Measurement Lab）。复用成熟 MCP、不建网关。Godot 是参考靶子（端到端实测）。

## 现状（2026-07-13 · 端到端全验证）

| 层 | 指标 | 值 |
|---|---|---|
| 代码检索（cmm BM25）| broad@5 | **0.846**（godot-core）· **0.952**（graphify-pkg 小库）|
| 文档检索（graphify）| recall@5 | **0.717** |
| 跨工具 anchoring | 成功率 | **100%**（8/8）|
| 记忆召回（MemPalace）| hit@5 | **0.933** · 路由准确率 **1.0** |
| agent A/B Stage 0 | context 压缩 | **12.71×**（KB 省 58% token）|
| agent A/B Stage 1 | 四臂准确度 | baseline 0.923 · cmm 0.923 · codegraph **0.962** |
| 文档答案质量 | faithfulness | **0.971**（Ragas 协议）|
| 记忆答案质量 | faithfulness | **0.951** |

**pytest 64 passed · 归档 37 份 · 5 target · Gold lab 题库编辑器 live · 零失败。**

## 快速接入

```bash
git clone https://github.com/kongshan001/code-multimodal-kb.git && cd engineer_demo
./setup.sh all                    # 装环境（Python + 4 工具 + 渲染 + 凭据检查）
python -m eval.cli web            # 起前端 → http://127.0.0.1:8765
# → 浏览器开 Dashboard / Run console / Setup 体检 / Gold lab
```

Windows：双击 `setup-bench.bat`（装 Python 依赖）→ `deploy.bat <代码目录>`（装 KB 工具 + 接入项目）。

命令行同样可用：`python -m pytest eval/tests/`（测试）→ `python -m eval.cli run code/memory/ab/...`（跑评测）。
改配置（模型/价格/步数上限/端口）：编辑 **`bench.yaml`**（无需改代码）。

## 对接你自己的工程（fork 模板）

本仓库是 fork 模板——clone 后把 benchmark 指向你自己的代码/文档/记忆：

1. 建 `eval/targets/<myproj>/target.json`：`cp eval/targets/<similar>/target.json.example target.json` 再填你机器路径（target.json 已 gitignored——本地配置不入库，各机不冲突；模板 target.json.example 入库）
2. 建索引（`codegraph init` / `cmm index` / `graphify build` / `mempalace mine`，按 subject）
3. 造题：`bench goldgen <seeds> --target <myproj>` → `bench web` Gold lab 逐条 approve；或前端编辑器手增
4. 跑：`bench run code --target <myproj> --method bm25`

完整 6 步 + 常见坑（cmm_project 名、机器路径、graphify 成本）见 [bench-dock-target skill](.claude/skills/bench-dock-target/SKILL.md)——对 Claude 说"把 X 工程对接到 benchmark"它会带你走完。每个 target 目录也有面向小白的 README。

## 文档索引

> **完整索引**：[docs/README.md](docs/README.md)（按用途分组 + 文档间关系图，单一入口）

| 文档 | 内容 |
|---|---|
| [docs/benchmark-runbook.md](docs/benchmark-runbook.md) | **bench CLI 手册**：怎么跑 / goldgen 扩题 / 归档 / 读报告 |
| [docs/ab-agent-internals.md](docs/ab-agent-internals.md) | **agent loop 源码拆解**：提示词 / 轮次 / token（含两 engine）← 外部评审 |
| [docs/ab-agent-optimization-roadmap.md](docs/ab-agent-optimization-roadmap.md) | **优化路线图**：done / todo / 否决 |
| [docs/architecture.md](docs/architecture.md) | **框架总览**：组件 / 数据流 / 记忆四层 / 设计决策 |
| [docs/deployment-runbook.md](docs/deployment-runbook.md) | **部署/排错**：A 代码 / B 文档 / C 评测 / D 记忆 |
| [docs/frontend-guide.md](docs/frontend-guide.md) | **前端使用说明**：起服务 / 视图详解 / CLI 对应 |
| [docs/windows-compatibility.md](docs/windows-compatibility.md) | **Win 兼容**：cp936 编码坑 + 修复铁律 |
| [docs/diagrams/](docs/diagrams/README.md) | **流程图**（总览 + agent loop + target 布局 + arms×tools） |
| [CLAUDE.md](CLAUDE.md) | agent 纪律：OpenSpec 铁则 + 记忆四层归属判定 |

## OpenSpec 变更

| 变更 | 状态 | 主题 |
|---|---|---|
| `add-bench-targets` | **进行中**（组 1-8 ✅）| 题库配置化（`targets/` 模型）+ 引擎可移植 + 前端 Gold lab 编辑器 + dock skill |
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

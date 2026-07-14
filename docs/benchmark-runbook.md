# Benchmark Runbook

> 统一 `bench` CLI + 报告自动归档留底。消费 `evaluation` capability 的指标 / gold，
> 不重定义。规格见 `openspec/specs/evaluation/spec.md`（capability）+ archived changes。

## 1. 装

| 依赖 | 用途 | 必需 |
|---|---|---|
| Python 3.12+ | 运行 CLI / 测试 | 是 |
| pytest | 跑测试套件 | 跑测试时 |
| codebase-memory-mcp（cmm） | 代码 KB 评测（code/ab/ab-agent/goldgen 枚举）| 跑真评测时 |
| graphify | 文档 KB 评测（doc/cross、ab doc 臂）| 跑 doc 时 |
| codegraph | 第二代码 KB（ab-agent codegraph 臂、goldgen 枚举）| 跑该臂时 |
| MemPalace 3.5+ | 记忆侧评测（memory）| 跑 memory 时 |
| anthropic SDK + GLM key | agent A/B（ab-agent）、goldgen LLM 拟题 | 跑 ab-agent/goldgen 时 |

> GLM 凭据走 `~/.cc-connect/config.toml`（zhipu/BigModel anthropic 兼容端点）或 env `AB_API_KEY/AB_BASE_URL/AB_MODEL`，**不入库**。
> 测试套件零外部依赖（mock subject），无任何 KB/凭据也能 `pytest eval/tests/`。

## 2. 跑（`bench` CLI）

建议加 alias：`alias bench='python -m eval.cli'`。下文用 `bench` 代指。

> **题目与目标工程绑定 = `eval/targets/<id>/`**（`target.json` 描述工程 + `problems.json` 存题）。`--target` 接 **target id**（如 `godot-core`），不是旧的金模块名。对接自己的工程见 [bench-dock-target skill](../.claude/skills/bench-dock-target/SKILL.md) 或各 target 的 README。

### `bench run <subject>` —— 跑评测并归档

```bash
# 检索层（测工具召回质量）—— --target = target id
bench run code   --target godot-core --method bm25   # 代码侧（cmm）：grep/bm25/semantic
bench run doc    --target godot-docs                  # 文档侧（graphify query）
bench run cross  --target godot-cross                 # 跨工具 anchoring（文档概念→代码）
bench run memory --target engineer-demo-memory        # 记忆侧（MemPalace 召回 hit@k + D1 路由）
bench run quality                                    # 文档答案质量（凭据门控，可能 429）

# agent 层（测"有 vs 无 KB"端到端价值）
bench run ab       --target godot-core                # Stage 0 token 代理（零 LLM：KB vs grep 压缩比）
bench run ab-agent --target godot-core --runs 1 [--arms baseline,kb,doc,codegraph]  # Stage 1 真跑 agent
```

`ab` / `ab-agent` 用 `ab_tools.py` 注册表（接新 KB = 写 executor + register + 挂臂，loop/判分零改）。
内置臂：`baseline`(grep) / `kb`(cmm) / `doc`(graphify) / `codegraph`。

每次 `run`：
1. 调对应 `run_*.py` 的 `run()` 产出报告
2. `normalize_report()` 规范成统一 schema
3. `archive_report()` 落盘到 `eval/reports/archive/<UTC-ts>-<subject>-<variant>.json`（**不覆盖**）
4. 追加 `archive/index.json` 一条记录
5. stdout 打印归档 id / 路径 / aggregate 摘要

### `bench list-reports` —— 列历史归档

输出 `archive/index.json` 全部报告（id / subject/variant / ts / 主指标摘要）。

### `bench show <id>` —— 看单份报告

打印完整归档 JSON（含 `per_query` 与 `lockfile`）。

### `bench compare <id1> <id2>` —— 两份报告对比

仅 `aggregate` 维度 diff（metric / left / right / delta）。用于横向对比"换 method / 换 gold / 调 prompt"前后的指标变化。

### 扩题（`goldgen`）—— agent 挖题 + 实证验收 + 人审

候选**直接进 `targets/<id>/problems.json`（`status: pending` + provenance）**——无 pending.md、无 fold。人审 = 前端逐条 approve。

```
1. bench goldgen <seeds> --target <id> [--dir D] [--n 20]   # codegraph 枚举符号 + LLM 拟 NL 题
                                                            # （gold=符号，构造即正确）→ 写 pending 候选进 problems.json
2. bench goldgen-verify --target <id>                        # 实证验收（零 LLM）：在 pending 候选原地标 verdict（同名歧义）
3. （主 agent spawn 独立 subagent 做语义验收，判 NL query↔gold 匹配）
4. 人审：bench web → Gold lab → pending 候选逐条 ✓ approve（status→accepted）/ 🗑 删
```

- **scope** = 搜索 seed 词（Vector/color/...）指一片代码；`--dir core/math` 从文件名派生 seed 兜底
- gold 来自 codegraph 真实符号 = 构造即正确，**零 LLM judge**（绕开循环）；LLM 只拟 query 措辞
- 手动增/改/删题也走前端 Gold lab 编辑器（schema 校验）或直接编 `problems.json`（loader 校验）
- 改完 `git commit`——前端不自动提交（顶部"待提交"黄条会提示）

### `bench run agent-compare` —— 4 臂（KB×skills）对比 → 目录报告

回答"KB 值不值"和"软件开发 skills（superpowers/openspec）值不值"。4 臂 = 工具集 × skills 注入：

| 臂 | 工具 | 注入 skill |
|---|---|---|
| `no-kb` | grep + read | 无 |
| `kb` | cmm + read | 无 |
| `kb+superpowers` | cmm + read | superpowers SOP |
| `kb+openspec` | cmm + read | openspec SOP |

```bash
bench run agent-compare --target <id> --runs 1           # 4 臂全跑（code_retrieval + bug_fix）
bench run agent-compare --target <id> --subset 6         # pilot（省时省钱）
bench run agent-compare --target <id> --smoke            # mock（无凭据验管道，假数据）
bench run agent-compare --target <id> --arms no-kb,kb    # 只测 KB 价值，省 skill 臂
```

产出**目录报告**（不是单 JSON）：`eval/reports/agent-compare/<ts>-<id>/`
```
result.md        人读：谁赢 + 指标小白说明 + 对比矩阵 + 诚实边界（先看这个）
summary.json     臂×指标矩阵（accuracy/tokens/llm_calls/tool_steps/wall_clock/cost/tool_diversity + KB压缩比，程序消费用）
questions.md     逐题各臂得分对照（每题：答对/答案/指标 × 臂，看哪题谁答对谁省）
arms/<arm>/
  config.md                这臂工具+注入的 skill（透明可审计）
  aggregate.json           这臂指标聚合
  episodes/qNN/
    episode.json           单题执行过程（逐步 tool）+ 指标       [入库]
    session.jsonl          完整会话流                          [本地 gitignore]
    thinking.md            思考过程                            [本地 gitignore]
```

**指标**：accuracy / input·output·total_tokens / llm_calls（LLM 轮数）/ tool_steps / wall_clock_s / cost_$ / context_compression（KB vs 无KB token 比）/ tool_diversity。

**看 skills 价值**：对比 `kb+superpowers`/`kb+openspec` vs `kb` 的 accuracy + tokens。**bug_fix 题上差异最可能显现**（纯 code_retrieval 上 skills 显不出价值——见 `bench-author-problems` skill 的 bug_fix curate 步）。

**诚实边界**（result.md 也标）：① skills 臂注入的是 `eval/arms/skills_bundled/` 的**精简 SOP 文本**，非完整 Claude Code skill 运行时（无触发机制/hook），是 headless 近似 ② accuracy 由 GLM 生成+判分（同家族 self-preference），相对值 ③ `cost_$` 依赖 MODEL_PRICES 单价，可能为 0（占位）④ 样本量小，看趋势勿绝对化。

> bug_fix 题型：`query`=bug 复现，`gold={symbols,files}`，复用 broad match 判分。给 skills 臂发挥空间。

## 3. 读报告

统一 schema（所有 subject 顶层一致）：

```
{
  "subject":      "cmm.bm25" | "graphify.query" | "cross-tool anchoring (graphify→cmm)" | ...,
  "variant":      "godot-bm25" | "godot" | ...,
  "target":       "godot" | "godot-docs-subset" | ...,
  "n":            查询条数,
  "aggregate":    { 主指标: 值, ... },
  "per_query":    [ { query, gold, retrieved_top5, recall@k, ... }, ... ],
  "lockfile":     { temperature, llm_model, cmm_version, graphify_version, mem0_version, mempalace_version },
  "archive_meta": { id, ts, readable_ts, path }
}
```

**指标释义**：

| 指标 | 含义 |
|---|---|
| `recall@k`（strict） | top-k 节点短名精确匹配 gold 的比例 |
| `broad_recall@k` | 归一化匹配：gold 出现在 `node / qualified_name / file` 任一即算命中 |
| `crosstool_success_rate` | 文档概念 → cmm 代码定位的端到端成功率 |
| `graphify_hit_rate` / `cmm_hit_rate@5` | 跨工具链路两段各自命中率 |
| `mean_compression_read` | agent A/B Stage 0：朴素 grep 读 token / KB 注入 token（context 压缩比）|
| `mean_hit@5` / `mean_recall@5` | 记忆侧 / ab 注入命中 |
| `routing_overall_accuracy` | D1 四层路由准确率（记忆侧）|
| `<arm>.accuracy` / `mean_total_tokens` / `mean_steps` | agent A/B Stage 1：各臂终答准确度 / token / 步数 |

> **Godot 级大 C++ 用 broad**：cmm `search_code` 把类埋在方法下，strict 在大库结构性失效（Godot strict@5=0.0）；broad + 归一化才是公平刻度。

## 4. 复现

`lockfile` 锁三项：`temp=0` + 固定 LLM 模型 + 工具版本（cmm/graphify/mem0）。

- 同 lockfile → 跨设备 / 跨时间分数可比
- 代码侧结构指标天然确定（不调 LLM），lockfile 主要记版本便于追溯
- 文档侧 / 记忆侧依赖 LLM 抽取（非确定），lockfile 是可比性前提

## 5. 归档查询

```
eval/reports/archive/
  ├─ <ts>-<subject>-<variant>.json    # 每次跑一份，不覆盖
  ├─ <ts>-<subject>-variant>-2.json   # 秒级冲突加后缀
  └─ index.json                       # 全量清单（追加式）
```

- `ts` = UTC ISO8601 基本格式（`20260711T1430Z`），跨时区可比、文件名安全
- `index.json` 每条含 `readable_ts`（本地可读时间）
- 历史 `eval/reports/*.json`（CLI 时代前的手动落盘）保留在 `reports/` 根，**不**入 archive

## 6. 测试

```bash
python -m pytest eval/tests/ -v
```

四层（43 测试，零外部依赖）：

| 层 | 文件 | 测什么 |
|---|---|---|
| L1 纯函数 | `test_retrieval_metrics` / `test_graph_metrics` / `test_repro` / `test_harness_roundtrip` | metrics / repro / harness 纯函数 |
| L2 端到端 smoke | `test_archive` / `test_memory` / `test_ab_value` / `test_ab_agent` | mock subject → run() → aggregate + 归档 |
| L3 留底机制 | `test_archive::test_archive_no_overwrite` | 跑两次 → 两文件 + index 两条 + 不覆盖 |
| gold 回归 | `test_gold_regression` / `test_gold_memory_snapshot` | gold_*.py 长度 + 首条快照，防漂移 |
| 工具/扩题 | `test_ab_tools` / `test_goldgen` | A/B 工具注册表 + goldgen 枚举/验收/fold |

## 7. 遗留用法

散装 `python -m eval.run_code_baseline --target godot --method bm25` 仍可用（直接 `print` JSON 到 stdout，**不归档**）。新用法一律走 `bench`。

## 8. 前端

报告 = 结构化 JSON（统一 schema），`archive/index.json` 是清单。前端 Measurement Lab 直接消费这俩数据源（不解析 stdout）。起前端：`bench web`（→ http://127.0.0.1:8765），含 Dashboard / Run console / Reports / Compare / Setup / Onboarding / **Gold lab 题库编辑器**（读写 `problems.json`）。详见 `docs/frontend-guide.md`。

## Context

`eval/` benchmark 当前结构（事实）：

- 题库 = `eval/gold_<target>.py` 里的 Python 字面量 `GOLD: list[tuple[str, set[str]]]`（code/docs）/ 四元组（crosstool）/ 两种结构（memory 的 RECALL+ROUTING）。6 个 gold 文件、5 种 gold 形状。
- 造题 = `goldgen.py`：枚举符号 → LLM 拟题 → 写 `gold_pending_<target>.md`（人审）→ `fold()` 调 `write_gold_module()` **全量重写 .py**，丢掉 kind/file/source/verdict。
- 前端 Gold lab = 只读 `gold_pending_*.md` 当纯文本 blob 显示，改题要离开浏览器手编文件。
- 13 处硬编码机器/工程路径：`ab_tools.py:28-29` / `run_ab_value.py:27-28` / `gold_crosstool.py:8` / `run_memory_baseline.py:85` / `run_memory_quality.py:54` / `cli.py:205,215` / `goldgen.py:29,167` / `web/app.js:92,107,382`。
- 快照测试 `test_gold_regression.py` / `test_gold_memory_snapshot` pin `gold_*.py` 长度+首条，**且 pin `PROJECT=="Users-ks-128-..."`**。

仓库既有范式（可直接照搬）：`scaffold/catalog.json`（声明式配置）+ `catalog.local.json`（overlay）+ `scaffold.py` loader + 前端 catalog 视图（读 `/api/catalog`、展示+执行安装）。

约束：本仓库是 spec 仓库，产出提交 main + push；检索层零额外依赖（pytest-only）；不引入 ragas / numpy≥2；`add-bench-frontend` change 已建 Gold lab 视图（15/16 近完成），本变更是其 Tier-2 interactive 需求的延伸。

## Goals / Non-Goals

**Goals:**

- 题库从 Python 字面量迁到声明式配置（type 判别 + 稳定 id + 元数据），前端可读写。
- per-target 目录隔离：每目标工程独立 `targets/<id>/`，引擎零工程假设。
- 可移植：移除全部硬编码路径，拿到别的工程能低成本对接（fork 模板 + target 可拷贝）。
- goldgen 直写配置、废 pending.md + fold，编辑全增量。
- 迁移受控、回归门禁同步更新。

**Non-Goals:**

- **不**做 `eval/core/` 大搬迁（纯 cosmetic，动所有 import，风险大收益零）。引擎文件留 `eval/` flat。
- **不**做 pip 打包 / 独立发版（仓库当 fork 模板，targets/ 可拷贝即够）。
- **不**把 memory 基准纳入「可对接任意项目」——它是自指 engineer_demo 自己 memory 的内置 demo target，别人 fork 后删/换。
- **不**前端自动 commit/push git（前端只写文件，用户自己 commit）。
- **不**引入 YAML/PyYAML（保持检索层零依赖，见决策 D1）。
- **不**解决 memory gold 锚文件名会腐的既有问题（schema 留 notes 标注，已知限制）。

## Decisions

### D1. 配置格式 = JSON，不用 YAML

**选 JSON**（`problems.json` / `target.json` / `target.local.json`）。理由：
- 检索层零依赖是仓库明确 ethos（`requirements.txt`：「检索层零额外依赖——只 pytest」）。加 PyYAML 破坏它。
- 与 `catalog.json` / `catalog.local.json` 完全一致（loader 模式、overlay 模式都照搬）。
- 前端是主编辑路径，JSON 机器读写无碍；诚实标注已迁进结构化字段（tags/notes/provenance），不靠注释。
- stdlib `json` + `ensure_ascii=False` 处理中文 query 无碍。

**考虑过的替代**：YAML（PyYAML，人手编更友好、支持注释/多行）——被零依赖 ethos 否决。TOML（stdlib 3.11+ 只读、写需 tomli-w）——读写不对称，否决。

**取舍**：JSON 无注释、多行 query 需 `\n`。缓解：诚实标注已在结构化字段；多行 query 罕见且前端表单处理无碍。

### D2. 单一 problems.json + type 判别（A1），不分类型文件

**选统一 schema**，`type` 字段决定 gold 形状（discriminated union）。5 型：

| type | gold 形状 | 现有来源 | runner |
|---|---|---|---|
| `code_retrieval` | `{symbols: [...]}` | gold_godot / gold_code | run_code_baseline |
| `doc_retrieval` | `{node_labels: [...]}` | gold_docs | run_doc_baseline |
| `cross_anchor` | `{doc_node_label, cmm_identifier, code_file}` | gold_crosstool | run_crosstool_baseline |
| `memory_recall` | `{source_files: [...]}` | gold_memory.RECALL | run_memory_baseline |
| `memory_routing` | `{layer, signal}` | gold_memory.ROUTING | run_memory_baseline |

**考虑过的替代**：A2 分类型文件（retrieval.json / routing.json / recall.json）——被否，因为它把痛点 2（schema 碎裂）从 .py 搬到 .json，没本质改善，且前端要为每型写分支。

### D3. per-target 目录模型；引擎留 flat

```
targets/
  <id>/
    target.json          # 工程描述（语言/subjects/路径/依赖），提交
    target.local.json    # 机器路径 overlay，gitignored
    problems.json        # 题库，提交
    fixtures/            # 测试 fixture（可选）
```

引擎（`eval/*.py`）保持原位，只改「读取源」+「拔硬编码」。loader 集中在新增 `eval/targets.py`。

**5 个 target 布局**（替换 6 个 gold_*.py）：

```
targets/
  godot-core/          ← code_retrieval（原 gold_godot）
  graphify-pkg/        ← code_retrieval（原 gold_code）
  godot-docs/          ← doc_retrieval（原 gold_docs）
  godot-cross/         ← cross_anchor（原 gold_crosstool）
                         target.json 声明 deps: {doc_graph: godot-docs, cmm: godot-core}
  engineer-demo-memory/  ← memory_recall + memory_routing（原 gold_memory）
                           内置 demo target，自指，不可移植，fork 后可删可换
```

### D4. target.local.json overlay（机器路径可移植）

`target.json` 提交原作者的可跑值（开箱即跑）；`target.local.json`（gitignored，同 `catalog.local.json`）按机器覆盖 `codegraph_root` / `cmm_project` / `graph` 路径。loader 深合并。

### D5. 稳定 id = `<target-id>-<slug>`

slug = query/fact 前 ~3 词 lowercase kebab。撞名加 `-2` / `-3`。迁移脚本 deterministic 生成。

**替代**：纯序号（`godot-01`）——插入会错位，否决。content hash——无意义、难引用，否决。slug 方案对重排稳定，仅 query 措辞大改才变（属真内容变更，可接受）。

### D6. pending 折进 problems.json（废 .md + 废 fold）

候选带 `status: pending` 落 `problems.json`；verify 在原地标 `verdict`/`reason`；人审 = 前端逐条 approve（`status: accepted`）或删。**废除 `gold_pending_<target>.md` + 废除 `fold()` + `write_gold_module()` + 全量重写**。编辑全增量（痛点 4 根治）。

**替代**：保留独立 pending 文件、只把 fold 改写 json——否，两文件双源易飘、fold 全量重写问题没治。

### D7. 迁移 = 受控 big-bang（C1）

数据量小（~70 题 / 6 文件），单次连续提交收口。**不用** dual-read shim（双源易飘）、**不用** yaml-source-py-gen（引入 build 步骤）。快照测试同 PR 改 pin `problems.json`。

### D8. 前端只写文件，不碰 git（D1）

前端 POST/PUT/DELETE → server 写 `problems.json`。显示「待提交」diff 指示器，用户自己 `git commit`（同 catalog install 改 `settings.json`）。并发写 last-write-wins 可接受（localhost 单用户场景）。

### D9. 通用性交付 = fork 模板 + target 可拷贝（E2+E3）

仓库 README 写「fork me → 改 targets/ → 删 demo targets → bench」。`targets/<id>/` 自包含可拷贝给别人仓库。**不**做 pip 打包。

## Schema 样例

### `targets/godot-core/target.json`

```json
{
  "id": "godot-core",
  "language": "C++",
  "subjects": ["code_retrieval"],
  "code": {
    "codegraph_root": "/Users/ks_128/Documents/godot-src/core",
    "cmm_project": "Users-ks-128-Documents-godot-src-core"
  },
  "notes": "Godot 4.7 core/, 13504 节点 / 38470 边"
}
```

### `targets/godot-cross/target.json`（跨 target 依赖）

```json
{
  "id": "godot-cross",
  "subjects": ["cross_anchor"],
  "deps": {"doc_graph": "godot-docs", "cmm": "godot-core"},
  "notes": "graphify 文档概念 → cmm 代码定位"
}
```

### `targets/godot-core/problems.json`（统一 schema，type 判别）

```json
{
  "version": 1,
  "target": "godot-core",
  "problems": [
    {
      "id": "godot-core-color",
      "type": "code_retrieval",
      "query": "color",
      "gold": {"symbols": ["Color"]},
      "tags": ["exact_name"],
      "provenance": {"source_symbol": "Color", "kind": "class", "file": "core/math/color.h"},
      "status": "accepted"
    },
    {
      "id": "godot-core-string-format",
      "type": "code_retrieval",
      "query": "string format",
      "gold": {"symbols": ["vformat"]},
      "tags": ["concept_query"],
      "status": "accepted"
    }
  ]
}
```

memory_routing / memory_recall / doc_retrieval / cross_anchor 的 gold 形状见 D2 表。`status: pending` 候选额外带 `verdict`/`reason`（verify 标注）。

## Risks / Trade-offs

| # | Risk | Mitigation |
|---|---|---|
| R1 | 快照测试 pin `.py` + `PROJECT` 字符串断言 | 同 PR 改 pin `problems.json`（count + 首条 id），拔 `PROJECT` 断言 |
| R2 | goldgen 全链路重写（generate/verify/fold） | 按 D6 重写；旧函数全删，不留兼容 |
| R3 | 稳定 id 分配须 deterministic | `<target>-<slug>` + 撞名后缀（D5），迁移脚本单测覆盖 |
| R4 | `target.json` 机器路径不可移植 | `target.local.json` overlay（D4），gitignore |
| R5 | memory gold 锚 memory 文件名，文件一变 gold 就腐 | schema 留 `notes` 标注；已知限制，本变更不解决 |
| R6 | cross_anchor 跨 target 依赖（doc graph + cmm） | `godot-cross` 独立 target，`deps` 字段声明；loader 校验依赖 target 存在 |
| R7 | 归档报告跨迁移边界不可比 | 报告是不可变快照；runbook 标注迁移分界点；compare 跨边界属 apples-to-oranges |
| R8 | 前端并发写 last-write-wins 丢编辑 | localhost 单用户可接受；写入前读最新版本做乐观比对（可选） |

## Migration Plan

受控 big-bang，连续提交（每步独立提交 main + push）：

1. **加 `eval/targets.py` loader**：`load_target(id)` / `load_problems(id)` / `merge_local()` / `validate_schema()`。→ 验证：单测覆盖 5 type + overlay 合并 + schema 校验。
2. **迁移脚本 `eval/migrate_gold.py`**：读 6 个 `gold_*.py` → 生成 5 个 `targets/<id>/{target.json, problems.json}`，deterministic id。→ 验证：题数守恒（godot 26 / code 21 / docs 10 / cross 8 / memory recall 15 + routing 14），人眼抽查几条。
3. **改 runner + goldgen 读 targets/**：`run_code/doc/crosstool/memory_baseline` + `run_memory_quality` + `run_ab_value` + `ab_tools` + `goldgen` 全部经 loader 取数据，root/project 从 `target.json` 读。→ 验证：`pytest eval/tests/` 全绿（除快照，下一步改）。
4. **拔 13 处硬编码**：删 `cli.py` `--root` 参数及默认值；`goldgen.py` `DEFAULT_ROOT`/`_CMM_PROJ_FALLBACK` 删；`app.js` 默认路径改从首个 target 读或留空提示。→ 验证：`grep -rn "godot-src\|ks-128\|ks_128" eval/ web/` 仅剩 target.json 内（合理）。
5. **重写 goldgen**：generate 直写 `problems.json`（status: pending）；verify 原地标 verdict/reason；删 `write_gold_module`/`fold`/`write_pending`/`parse_pending`/`pending_path`。→ 验证：`test_goldgen.py` 改后全绿；前端 Gold lab ① 挖拟题 → ② verify → ③ approve 走通。
6. **删 gold_*.py + 改快照测试**：删 7 个 gold 文件；`test_gold_regression.py` / `test_gold_memory_snapshot` 改 pin `problems.json`（每 target count + 首条 id）。→ 验证：`pytest eval/tests/ -v` 全绿。
7. **server.py +4 路由 + 前端编辑器**：`GET/POST/PUT/DELETE /api/gold/<target>`；`web/app.js` Gold lab 升级为编辑器（列表/CRUD/batch tag/approve pending + 待提交 diff 指示器）。→ 验证：浏览器内增/改/删一道题、approve 一道 pending、文件落地正确。
8. **文档同步**：`docs/benchmark-runbook.md`（targets/ 模型 + 对接新工程）、`README.md`（fork 模板）、`docs/frontend-guide.md`（编辑器）。→ 验证：新人照 runbook 能对接一个新 target。

**回滚**：迁移是单次连续提交，若发现严重问题 `git revert` 该批提交即可（gold_*.py 仍在 git 历史里）。无不可逆副作用。

## Open Questions

- **OQ1**：`cross_anchor` 的 `deps` 字段校验多深？仅校验依赖 target 存在，还是 loader 主动加载依赖 target 的路径并注入？（设计倾向后者——loader 解析 deps 后把 doc_graph/cmm 路径注入 cross target 的运行上下文，runner 无感。）
- **OQ2**：`engineer-demo-memory` 这个内置 demo target 在 README/onboarding 里如何呈现？是默认展示（教学价值）还是默认折叠（避免误导新用户以为它是可对接模板）？（倾向：默认展示 + 明确标「demo / self-referential，fork 后建议替换」。）
- **OQ3**：`problems.json` 的 `version` 字段当前 = 1。未来加新 type / 新 gold 字段时的 schema 演进策略？（本变更不定，留 v2 时再议；loader 对未知字段宽容忽略。）

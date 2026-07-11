## 1. 归档层与报告 schema（基础，CLI 依赖它）

- [ ] 1.1 建 `eval/archive.py`：`archive_report(report, subject, variant)` → 写 `eval/reports/archive/<UTC-ts>-<subject>-<variant>.json`（不覆盖）+ 追加更新 `archive/index.json`（每条 `{id, ts, subject, variant, target, lockfile, aggregate 摘要, path}`） → 验证：单测跑两次同 subject+variant 产两个文件、index 两条、不覆盖
- [ ] 1.2 定义统一报告 schema：`normalize_report()` 把 `run_*.py` 的 `run()` 输出规范成 `{subject, target, n, aggregate, per_query, lockfile, archive_meta}` → 验证：code / doc / cross 三种输出经 normalize 后顶层字段一致
- [ ] 1.3 建 `eval/reports/archive/` 目录 + `.gitkeep`；现有 `reports/*.json` 保留原处不迁移

## 2. 统一 CLI 入口 `bench`

- [ ] 2.1 建 `eval/cli.py`：argparse 子命令骨架（`run` / `list-reports` / `show` / `compare`）+ `bench` 入口（`python -m eval.cli`） → 验证：`bench --help` 列出全部子命令
- [ ] 2.2 `run code|doc|cross|quality` 子命令：调对应 `run_*.py` 的 `run()` → `normalize_report` → `archive_report` → stdout 打印归档路径 + aggregate 摘要 → 验证：`bench run code --target godot --method bm25` 端到端跑通并归档（有 cmm 时）；mock subject 时归档正确
- [ ] 2.3 `list-reports` 子命令：读 `archive/index.json` 输出表格（id / ts / subject / variant / aggregate 摘要） → 验证：跑过几次后 list 输出含全部记录
- [ ] 2.4 `show <id>` 子命令：按 id 从 archive 读单份报告，打印详情（含 per_query） → 验证：show 输出含 per_query 与 lockfile
- [ ] 2.5 `compare <id1> <id2>` 子命令：**仅 aggregate 对比**（diff 表，决策 OQ1） → 验证：两份 code 报告对比输出 broad@5 等指标差值

## 3. 测试固化（pytest）

- [ ] 3.1 L2 端到端 smoke：mock subject（返回固定检索结果）→ 跑 `run()` → 断言 aggregate 落在预期区间 + 归档文件生成；零外部依赖 → 验证：无 cmm / graphify / Godot 时 `pytest eval/tests/` 通过
- [ ] 3.2 L3 留底机制测试：连续跑两次同 subject+variant → 断言两归档文件 + `index.json` 新增两条 + 既有文件不覆盖 → 验证：测试通过
- [ ] 3.3 gold 回归门禁：`gold_*.py` 的 GOLD 集快照断言（长度 + 首条 query+gold） → 验证：改 gold 长度 / 首条时测试失败
- [ ] 3.4 现有 L1 纯函数测试（metrics / repro / harness）保留通过；`pytest eval/tests/` 全绿

## 4. 文档

- [ ] 4.1 `docs/benchmark-runbook.md`：装 / 跑（`bench` 各子命令 + 参数）/ 读报告（schema + 指标释义）/ 复现（lockfile）/ 归档查询（`list-reports` / `show` / `compare`） → 验证：新人照文档能独立跑一次 code 评测并解释 aggregate
- [ ] 4.2 `eval/README.md` 更新：指向 `bench` CLI + runbook；标注散装 `python -m eval.run_*` 为遗留用法
- [ ] 4.3 根 `README.md` 文档索引补 `docs/benchmark-runbook.md` 链接

## 5. 收尾验证

- [ ] 5.1 `openspec validate add-benchmark-runner` 通过
- [ ] 5.2 端到端冒烟：`bench run code`（mock）→ `list-reports` → `show <id>` → `compare` 全链路通
- [ ] 5.3 提交 main + push（带 Co-Authored-By）

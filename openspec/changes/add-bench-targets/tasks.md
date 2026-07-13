# Tasks · add-bench-targets

按 design.md 的迁移计划（受控 big-bang，8 阶段）拆。每步独立提交 main + push（带 Co-Authored-By）。每 task 带可验证证据。

## 1. Loader 与 schema（eval/targets.py）

- [x] 1.1 新增 `eval/targets.py`：`load_target(id)` / `load_problems(id)` / `list_targets()`；`target.json` + `target.local.json` 深合并（local 覆盖 base）
- [x] 1.2 schema 校验：`type`∈五选一；`gold` 形状匹配 `type`（code→symbols / doc→node_labels / cross→{doc_node_label,cmm_identifier,code_file} / recall→source_files / routing→{layer,signal}）；`id` target 内唯一；必填字段齐全
- [x] 1.3 cross target 的 `deps` 解析：loader 校验依赖 target 存在，解析并注入 doc_graph/cmm 路径到运行上下文
- [x] 1.4 新增 `eval/tests/test_targets_loader.py`：覆盖 5 type 合法加载、overlay 合并、deps 解析、非法 schema 各类失败 case → 全绿（24 测试通过）

## 2. 迁移脚本与 target 数据

- [x] 2.1 新增 `eval/migrate_gold.py`：读 6 个 `gold_*.py` → 生成 5 个 `targets/<id>/{target.json, problems.json}`（godot-core / graphify-pkg / godot-docs / godot-cross / engineer-demo-memory）
- [x] 2.2 deterministic id 生成：`<target-id>-<slug(query/fact 前3词)>`，撞名加 `-2/-3`；slugify 在迁移脚本内
- [x] 2.3 题数守恒验证：godot 26 / code 21 / docs 10 / cross 8 / memory recall 15 + routing 13 = 93（与源文件实数对照，routing 实为 13 非 explore 时误数的 14）；test_targets_loader 集成断言每 target 题数
- [x] 2.4 生成 `targets/<id>/target.json`（机器路径入 base，可跑值）+ `.gitignore` 加 `eval/targets/*/target.local.json` + 每目录留 `target.local.example.json`

## 3. runner 切换到 loader（迁移前过渡）

- [x] 3.1 `run_code_baseline` / `run_doc_baseline` / `run_crosstool_baseline` 改读 `targets/<id>/problems.json`（经 loader），不再 import `gold_*`
- [x] 3.2 `run_memory_baseline` / `run_memory_quality` 改读 `targets/engineer-demo-memory/problems.json`（recall + routing 两种 type）
- [x] 3.3 `run_ab_value` / `ab_tools` 改从 `targets/godot-core/target.json` 读 `cmm_project` / codegraph root（ab_tools DOC_GRAPH 从 godot-docs 读）
- [x] 3.4 并入组 5：`goldgen` 不做过渡改动，直接在组 5 重写（root/project 从 target.json 读）——避免写一次就扔的过渡代码
- [x] 3.5 额外迁移 `run_doc_quality_ragas` + `run_ab_agent`（gold 源 + graph/project 从 target 读）——它们也 import gold_*，不迁移会卡组 6 删除
- [x] 3.6 证据：`pytest eval/tests/`（除 3 个 anthropic-blocked）64 passed；3 个因变更失效的测试（test_ab_value / test_memory::recall_smoke / test_archive::code_smoke）已改 mock loader 全绿

## 4. 拔硬编码（retrieval 层）

- [x] 4.1 retrieval runner 全部拔除：`run_code/doc/crosstool/memory/ab_value` + `ab_tools` 的 `PROJECT`/`GODOT_CORE`/`CMM_PROJECT`/`DOC_GRAPH`/`GRAPH` 字面量改读 target.json
- [~] 4.2 **延期**：`run_doc_quality.py`（GRAPH/DOCS_DIR→godot-render-docs 语料）+ `run_doc_quality_ragas.py:RST_DIR`——anthropic-gated 答案质量 runner，需扩 target schema（`doc.rst_dir`）+ 可能第 6 个 target（godot-render-docs 是与 godot-docs-subset 不同的语料）。不阻塞组 6（它们不 import gold_*），列为后续
- [~] 4.3 **延期**：`web/app.js:92,107,382` 的 `_targetProject` 默认路径是 scaffold 能力目录扫描路径（非 bench target），属 scaffold 可移植性问题，另案。run-console 的 bench target 默认值（code/memory/ab/doc-ragas）已改新 target id
- [ ] 4.4 `goldgen.py:29 DEFAULT_ROOT` + `:167 _CMM_PROJ_FALLBACK` + `cli.py:207,217 --root` → 组 5 重写 goldgen 时一起拔
- [x] 4.5 证据：retrieval 层 `grep "godot-src\|ks-128\|engineer_demo" eval/run_*.py eval/ab_tools.py` 仅剩延期项（doc-quality 路径 + goldgen）；非延期硬编码已清零

## 5. 重写 goldgen（pending 折进 problems.json）

- [x] 5.1 `generate`：候选直接追加进 `targets/<id>/problems.json`，每条 `status: pending` + `provenance`（source_symbol/kind/file）；root/cmm_project 从 target.json 读
- [x] 5.2 `verify_pending` → `verify`：在 problems.json 原 pending 候选上原地标 `verdict`/`reason`（增量、幂等，不全量重写）
- [x] 5.3 删除 `write_gold_module` / `fold` / `write_pending` / `parse_pending` / `pending_path` / `DEFAULT_ROOT` / `_CMM_PROJ_FALLBACK` / `_gold_file_path`（fold 步骤消失）
- [x] 5.4 `cli.py` 删 `goldgen-fold` 子命令 + 处理器；`goldgen` / `goldgen-verify` 删 `--root`、`--target` 必传（target id）
- [x] 5.5 `server.py`：`/api/pending/<target>` 改读 problems.json 的 pending 候选（不再读 .md）；删 `/api/goldgen-fold` 路由
- [x] 5.6 `web/app.js` Gold lab：删 fold 按钮 + glFold（approve/删 编辑器留组 7）；默认 target → godot-core
- [x] 5.7 重写 `eval/tests/test_goldgen.py`：generate→problems.json pending（带 provenance + 稳定 id）+ 跳重复 query、verify 原地标（幂等，accepted 不动）；6 测试全绿
- [x] 5.8 `eval/targets.py` 加 `slugify` / `assign_ids` / `save_problems`（goldgen + 组 7 前端编辑器共用，校验 + 写回）

## 6. 删 gold_*.py + 改快照测试

- [ ] 6.1 删除 `eval/gold_godot.py` / `gold_code.py` / `gold_docs.py` / `gold_crosstool.py` / `gold_memory.py` / `gold_gen.py` / `gold_godot_gen.py`
- [ ] 6.2 重写 `eval/tests/test_gold_regression.py`：pin 每个 target 的 `problems.json`（题数 + 首条 id），断言 `target.json` 的 id/subjects/language（不断言 PROJECT 绝对路径）
- [ ] 6.3 重写 memory 快照测试：pin `targets/engineer-demo-memory/problems.json`（recall + routing 两段）
- [ ] 6.4 证据：`pytest eval/tests/ -v` 全绿（含新 loader / goldgen / 快照测试）

## 7. server 路由 + 前端 Gold lab 编辑器

- [ ] 7.1 `server.py` 新增 `GET /api/gold/<target>`（列题）、`POST`（新增，schema 校验）、`PUT /api/gold/<target>/<id>`（改）、`DELETE /api/gold/<target>/<id>`（删）；校验失败返 schema 错误
- [ ] 7.2 `web/app.js` Gold lab 升级为编辑器：题库表格（列表/新增/改/删），按 type 渲染 gold 字段表单
- [ ] 7.3 approve pending UI（status: pending 候选逐条 approve→accepted 或删）+ 批量打标（tags）
- [ ] 7.4 「待提交」dirty diff 指示器（前端不 commit，提示用户 git commit）
- [ ] 7.5 证据：浏览器内 round-trip——新增一道题 / 改 query / 删一道 / approve 一道 pending，`problems.json` 落地正确 + git 未被触碰

## 8. 文档与 fork 模板

- [ ] 8.1 `docs/benchmark-runbook.md`：targets/ 模型 + 对接新工程步骤（建 target.json + onboarding 索引 + goldgen 造题）
- [ ] 8.2 `README.md`：fork 模板工作流（fork → 删/换 demo targets → 建自己 target → bench）
- [ ] 8.3 `docs/frontend-guide.md`：Gold lab 编辑器用法（读写题库 + approve pending）
- [ ] 8.4 `engineer-demo-memory` demo target 在文档/前端明确标注 self-referential / 不可移植

## 9. 端到端验证

- [ ] 9.1 迁移后 `bench run code --target godot-core --method bm25` 跑通并归档；`bench list-reports` / `show` / `compare` 正常
- [ ] 9.2 `bench run memory --target engineer-demo-memory` 跑通（recall + routing）
- [ ] 9.3 干跑对接新工程：建一个 `targets/<scratch>/`（小代码库）+ onboarding 索引 + goldgen 造几题 + bench，验证「低成本对接」claim
- [ ] 9.4 全量 `pytest eval/tests/ -v` 绿；`grep` 复核零硬编码；迁移脚本可重跑（idempotent）

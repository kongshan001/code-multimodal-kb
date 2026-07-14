# Implementation Tasks

## 1. grep 文件类型过滤 target-aware（①核心）

- [ ] 1.1 在 `eval/ab_tools.py` 加模块级常量 `LANG_GLOBS`（`C++→[*.h,*.cpp,*.hpp]`、`Python→[*.py]`、`TypeScript→[*.ts,*.tsx]`、`Go→[*.go]`、`Rust→[*.rs]`、`Java→[*.java]`；未知 language → 空 list）
- [ ] 1.2 `set_active(target_cfg)` 注入 `_active["globs"]`：优先 `target_cfg["code"].get("globs")`，否则 `LANG_GLOBS.get(language, [])`
- [ ] 1.3 `grep_code(pattern)` 读 `_active["globs"]` 构造 `--include` 参数替代硬编码；globs 为空则不加 `--include`（全文件搜）
- [ ] 1.4 V3 回归断言：`set_active(load_target("godot-core"))` 后 `_active["globs"]` == `["*.h","*.cpp","*.hpp"]`（C++ 推断 = 历史硬编码值，零行为变更）→ 验证：断言通过

## 2. graphify-pkg 补 codegraph_root（②核心）

- [ ] 2.1 创建 `eval/targets/graphify-pkg/target.local.json`（gitignored），含 `code.codegraph_root = /Users/ks_128/.local/share/uv/tools/graphifyy/lib/python3.13/site-packages/graphify`（已实测存在）
- [ ] 2.2 V1 验证：`set_active(load_target("graphify-pkg"))` 后 `grep_code("class")` 返非空（含 `.py` 文件路径），对比现状 `(no matches)` → 验证：返文件数 > 0

## 3. 臂可用性启动检查（④）

- [ ] 3.1 在 `eval/run_ab_agent.py` 的 `run_compare` 跑题前加 `_check_arm_availability(arm, target)`：no-kb 看 `codegraph_root` 存在 + `globs` 非空；kb 系看 `cmm_project` 索引可查（轻量本地探测，不发 LLM）
- [ ] 3.2 探测结果透传进 `run_compare` 返回对象（每臂 `availability: {ok, reason}`）与 `summary.json`
- [ ] 3.3 `eval/agent_compare_report.py` 渲染：不可用臂在 `result.md` 顶部 warning 区呈现（臂名 + 原因 + 「该臂对该 target 的对照无意义」）
- [ ] 3.4 验证标注纪律：探测仅标注，不跳过臂、不中断跑批 → 验证：不可用臂的 episode 仍照常生成（自然失败/空转），无异常抛出

## 4. 端到端验证

- [ ] 4.1 V2 smoke：`bench run agent-compare --target graphify-pkg --arms no-kb,kb --subset 2` → no-kb 的 `tool_calls` 非空、不再系统性失败 → 验证：episode.json 的 `tool_calls` 长度 > 0
- [ ] 4.2 V3 回归：`bench run agent-compare --target godot-core --arms no-kb,kb --subset 2` → no-kb 行为与改动前一致（globs、命中文件集不变），无不可用标注 → 验证：输出对照 baseline 无差异 + 无 availability warning
- [ ] 4.3 文档：dock-target README / bench 文档注明「no-kb 臂需本机 `codegraph_root`（经 `target.local.json`）」+ claude-gui 别机路径属已知前置条件（③，单列后续变更）
- [ ] 4.4 提交：所有代码 + graphify-pkg local 占位说明 + spec/tasks 入 git（local 文件本身 gitignored，仅提交其存在性与对接说明）

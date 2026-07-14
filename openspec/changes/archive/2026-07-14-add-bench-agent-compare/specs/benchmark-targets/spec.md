## ADDED Requirements

### Requirement: Bug-fix problem type

系统 SHALL 支持 `bug_fix` problem type（第 6 型，扩展原 5 型题库 schema）。`bug_fix` 题：`query` = bug 复现/描述（需理解控制流定位，非词面查找），`gold` = `{symbols: [要改的符号], files: [预期文件]}`（均非空 list[str]）。loader SHALL 校验 `bug_fix` 的 gold 含非空 `symbols` 与 `files`。判分 SHALL 复用 code_retrieval 的 broad match（终答含 gold 符号或文件即命中）。`bug_fix` 题的存在是为给 skills 臂（systematic-debugging 等 SOP）发挥空间——纯检索题上 skills 无价值。

#### Scenario: bug_fix gold 形状校验

- **WHEN** loader 加载一道 `type: bug_fix` 的题
- **THEN** SHALL 断言 `gold.symbols` 与 `gold.files` 均为非空 list[str]；缺任一即校验失败

#### Scenario: bug_fix 复用 broad match 判分

- **WHEN** agent 跑 bug_fix 题，终答含 gold.symbols 任一或 gold.files 任一
- **THEN** SHALL 判命中（与 code_retrieval 同口径）

# 逐题得分对照

> 每题各臂的答对 / 答案 / 指标对照（3 题 × 4 臂）。
> 看哪题谁答对、谁省 token、谁卡住（truncated）。

## q01 · code_retrieval
**题**：string format
**gold**：vformat

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | The answer involves `vformat`. | 120 | 2 | 1 | 0.5 |  |
| `kb` | ✓ | The answer involves `vformat`. | 120 | 2 | 1 | 0.5 |  |
| `kb+superpowers` | ✓ | The answer involves `vformat`. | 130 | 3 | 2 | 0.8 |  |
| `kb+openspec` | ✓ | The answer involves `vformat`. | 130 | 3 | 2 | 0.8 |  |

## q02 · code_retrieval
**题**：int to string
**gold**：itos

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✗ | I could not locate it. | 131 | 2 | 1 | 0.57 |  |
| `kb` | ✗ | I could not locate it. | 131 | 2 | 1 | 0.57 |  |
| `kb+superpowers` | ✗ | I could not locate it. | 141 | 3 | 2 | 0.87 |  |
| `kb+openspec` | ✗ | I could not locate it. | 141 | 3 | 2 | 0.87 |  |

## q03 · code_retrieval
**题**：delete object free memory
**gold**：memdelete

| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |
|---|---|---|---|---|---|---|---|
| `no-kb` | ✓ | The answer involves `memdelete`. | 142 | 2 | 1 | 0.64 |  |
| `kb` | ✓ | The answer involves `memdelete`. | 142 | 2 | 1 | 0.64 |  |
| `kb+superpowers` | ✓ | The answer involves `memdelete`. | 152 | 3 | 2 | 0.94 |  |
| `kb+openspec` | ✓ | The answer involves `memdelete`. | 152 | 3 | 2 | 0.94 |  |


# q02 · code_retrieval · arm: `no-kb`

**题**：整数转成字符串用哪个函数？  ·  **gold**：itos
**答对**：✓  ·  **答案**：在 Godot core 中，整数转字符串常用的函数：

- **`String::num()`** — 将整数/浮点数转为字符串（最通用）
- **`String::itos()`** — 专门将 `int` 转为字符串（int to s
**指标**：tokens=442 · llm_calls=1 · tool_steps=0 · 耗时=10.75s · 截断=否

---

**👤 用户**：整数转成字符串用哪个函数？

**🤖 Agent**：在 Godot core 中，整数转字符串常用的函数：

- **`String::num()`** — 将整数/浮点数转为字符串（最通用）
- **`String::itos()`** — 专门将 `int` 转为字符串（int to string）
- **`String::num_int64()`** — 将 `int64_t` 转为字符串，可指定基数（如十六进制）

最直接的是 **`String::itos()`**。


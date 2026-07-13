# graphify-pkg · 反测 graphify 工具自己的代码检索

> 拿 **graphify 这个"文档知识图工具"自己的 Python 源码**当靶子，测代码 KB（cmm）能不能听懂大白话、找到对的函数/类。
> 小而真实的 Python 库，适合做代码检索的**基准尺**（对比 Godot core 那种大型 C++ 库）。

## 测什么

给一句开发者会自然问的大白话（比如 `call llm`、`xlsx to markdown`、`fetch arxiv`），看 cmm（代码知识库）返回的前几个符号里，有没有那个**对的**函数/类。

- **标准答案（gold）从哪来**：不是人拍脑袋写的，是工具从代码结构里挖出来的真实符号名（`_call_llm`、`xlsx_to_markdown`、`_fetch_arxiv`）→ 答案天然正确。
- 21 道题，混了"精确名查询"和"概念查询"。

## 最新结果（2026-07-13 · 21 题 · cmm BM25）

| 指标 | 值 | 大白话 |
|---|---|---|
| `broad_recall@5` | **0.952** | 前 5 个结果里有正确答案的题占 95.2% |
| `recall@5`（严格） | **1.0** | 前 5 个符号"名字"精确命中的比例 |
| `recall@1` | 0.81 | 第 1 个结果就命中的占 81% |

**一句话结论**：小库上 cmm 近乎满分（0.952）。对比 Godot core 大库（0.846）——**库越小越容易找准**，符合预期。

## 数字怎么看

- **`broad_recall@5`**（主指标）：前 5 个返回结果里，只要"名字 / 全名 / 文件路径"任一处对上标准答案，就算赢。
- **`recall@5`（严格）**：要求返回的符号**短名**和标准答案一模一样。小库能看到 1.0；大库里符号常被埋在方法节点下，严格分会被压低（所以大库看 broad 才公平）。

## 怎么自己跑

```bash
bench run code --target graphify-pkg --method bm25   # BM25 检索（主路）
bench run code --target graphify-pkg --method grep   # 对比：纯 grep
```

跑完自动归档（不覆盖历史）。看分数：`bench list-reports`；对比两次：`bench compare <id1> <id2>`。

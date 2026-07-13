# targets/ · 评测目标目录

> 每个**子目录 = 一个被测对象**（一段代码 / 一堆文档 / 一个记忆库）。
> 里面放着针对它的**题目（gold）**和**配置（target.json）**。

## 一个 target 目录里有什么

```
targets/<id>/
  target.json            这是什么对象 + 工具去哪找它（代码库路径 / cmm 项目名 / 文档图路径）
  target.local.json      你本机的路径覆盖（gitignored，别人机器不同）
  problems.json          题库（一道道题 + 标准答案，agent 不改这里，用前端/命令改）
  README.md              ← 你在看的这种：白话讲清楚 + 最新分数
```

## 5 个 target 一览

| 目录 | 测什么 | 最新主分数 | 说明 |
|---|---|---|---|
| [godot-core](godot-core/) | 大型 C++ 代码检索（Godot 引擎） | broad@5 = **0.846** | 大库硬考 |
| [graphify-pkg](graphify-pkg/) | 小型 Python 代码检索（graphify 工具自身） | broad@5 = **0.952** | 小库基准尺 |
| [godot-docs](godot-docs/) | 文档语义检索（Godot 文档） | recall@5 = **0.7** | 概念查询 |
| [godot-cross](godot-cross/) | 文档概念 → 代码定位（跨工具） | 成功率 **1.0** | 端到端链路 |
| [engineer-demo-memory](engineer-demo-memory/) | 本仓库自己的记忆层（demo） | hit@5 = **0.933** / 路由 **1.0** | 自指，不可移植 |

## 怎么跑一个 target

```bash
# 看有哪些 target
python -c "from eval.targets import list_targets; print(list_targets())"

# 跑某个 target 的评测（自动归档，不覆盖历史）
bench run code  --target godot-core   --method bm25
bench run doc   --target godot-docs
bench run cross --target godot-cross
bench run memory --target engineer-demo-memory

# 看历史分数 / 对比两次
bench list-reports
bench compare <id1> <id2>
```

## 给自己的项目建一个 target

1. 新建 `targets/<myproj>/target.json`（填代码库路径 + cmm 项目名；参考任意现有 target）
2. 建索引：`codegraph init <代码库>` + `cmm index`
3. 自动造题：`bench goldgen <seed词> --target <myproj>` → 人审 approve
4. 跑：`bench run code --target <myproj> --method bm25`

详见 `docs/benchmark-runbook.md`。

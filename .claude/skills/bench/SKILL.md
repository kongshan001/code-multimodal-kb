---
name: bench
description: benchmark 的单一入口——用户不用记用哪个 skill、什么顺序、什么命令。任何 benchmark 意图都先走这个："benchmark 我的工程/项目"、"测我的代码（检索准不准）"、"对接 X 到 benchmark"、"给 X 出题跑分"、"对比 KB / superpowers / openspec 价值"、"我想用 benchmark 测我的项目"、"dock my repo"。它先搞清目标（只要检索分数？还是想对比 KB/skills？）+ 探当前状态（对接没？索引没？有题没？），再路由到对的下一步。具体细节 delegate 给 bench-dock-target（对接+检索 benchmark）和 bench-author-problems（出题+4臂 skills 对比）——本 skill 只做"判断+路由"。先走这个，别让用户纠结该用哪个 skill。
---

# benchmark 单一入口

用户说"benchmark 我的工程"就够了——本 skill 判断**目标**+**状态**，路由到对的步骤。用户不用记 skill 名 / 顺序 / 命令。

## 第 0 步：搞清目标（一句话能看出就别问）

| 用户说的 | 目标 | 走向 |
|---|---|---|
| "测我代码检索准不准"、"broad@5 / recall"、"对接 X 跑分" | **A 只要检索质量** | 检索 benchmark |
| "KB 值不值"、"superpowers/openspec 价值"、"有/无 skills 差多少"、"agent 对比" | **B 还要 skills 对比** | 4 臂 agent-compare |
| 模糊（"benchmark 我的工程"） | 先问一句："只要检索分数，还是想看 KB/skills 哪个值？" | 按答走 A/B |

## 第 1 步：探状态（一条命令看对接到哪了）

```bash
bench status <工程路径 或 target-id>      # 不给则列全部 target + 各自状态
```
看输出里的状态：**未对接 / 已对接未索引 / 已索引无题 / 有题未跑 / 已跑过**。

## 第 2 步：路由（目标 × 状态 → 对的下一步）

```
未对接（无论 A/B）
  → 先对接：建 targets/<id>/target.json + 建索引 + goldgen 出 code_retrieval 题
    （详细步骤走 bench-dock-target skill）

已对接 + 目标 A（只要检索分数）
  → bench run code --target <id> --method bm25     （或 doc/cross/memory 按语料）
  → 读 result：bench list-reports / bench show <id> / bench web

已对接 + 目标 B（要 skills 对比）
  → 出 bug_fix 题（手动 curate，给 skills 发挥空间）+ AI 审 + 人工 approve + 4 臂对比
    （详细步骤走 bench-author-problems skill）
  → bench run agent-compare --target <id> --runs 1   （先 --subset 6 试水省钱）
  → 读 result.md（谁赢+指标+逐题对照+诚实边界）
```

## 第 3 步：交付 + 下一步

跑完告诉用户：分数 / 谁赢 + **下一步选项**（如"想确证 skills 价值就多跑几题/多 runs"、"想看自己工程就给 claude-gui 加 bug_fix"）。永远给一个明确的"接下来做什么"。

## 细节 delegate（本 skill 不重复）

- **对接工程 + 跑检索 benchmark**（code/doc/cross/memory，broad@5/recall 那套）→ `bench-dock-target` skill
- **出题（code_retrieval + bug_fix）+ AI 两层审 + 4 臂 skills 对比 + 目录报告** → `bench-author-problems` skill

本 skill 只做：**判断目标 → 探状态 → 路由 → 给下一步**。遇到具体执行，读对应 specialist skill。

## 速查（给用户的一张卡）

```
想 benchmark 我的工程？
  → 跟我说"benchmark <工程>"，或终端 bench status <工程> 看状态
  → 只要检索分数？  bench run code --target <id> --method bm25
  → 要对比 skills？  bench run agent-compare --target <id> --subset 6
```

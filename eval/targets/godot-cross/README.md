# godot-cross · 跨工具定位（文档概念 → 代码实现）

> 测"**从文档概念能不能跳到代码实现**"——文档里讲 `Vector2 Class`，cmm 能不能据此定位到 `math/vector2.cpp`。
> 真实 agent 经常"先查文档懂概念，再跳代码看实现"，这条跨工具链路是否走得通，是端到端能力的关键。

## 这是什么

- **目标**：Godot 文档子集图（依赖 [godot-docs](../godot-docs/)）+ Godot core 的 cmm 索引（依赖 [godot-core](../godot-core/)）的**交叉**。
- `target.json` 里声明 `deps: {doc_graph: godot-docs, cmm: godot-core}`——loader 自动解析两段路径，runner 无感。

## 测什么

8 道题，每道走一条链：

```
概念（vector2 normalization length）
  └─① graphify 在文档图里找 → Vector2 Class        （文档侧命中？）
      └─② 把 "Vector2" 喂给 cmm → 定位 math/vector2  （代码侧命中？）
          └─③ 两边都对 = 端到端成功
```

## 最新结果（2026-07-13 · 8 题）

| 指标 | 值 | 大白话 |
|---|---|---|
| graphify 命中率 | **1.0** | 文档侧 8/8 全找到 |
| cmm 命中率@5 | **1.0** | 代码侧 8/8 全定位对 |
| 端到端成功率 | **1.0** | 两边都对：8/8 = 100% |

**一句话结论**：在向量/数学这片 Godot 子领域，**文档概念 → 代码实现的跳转 100% 走通**。

## 数字怎么看

- **`crosstool_success_rate`**（主指标）：一道题文档侧 + 代码侧**都**命中才算赢。1.0 = 全通。
- 单看 `graphify_hit_rate` / `cmm_hit_rate@5` 能定位断点：哪个低就是哪段断了。

## 怎么自己跑

```bash
bench run cross --target godot-cross
```

前置：godot-docs 文档图 + godot-core cmm 索引都建好（见各自 README）。

## 诚实边界

- 8 道题集中在 vector/math 子领域（覆盖文档子集范围），不代表全 Godot 域都 1.0——扩题见 `goldgen`。

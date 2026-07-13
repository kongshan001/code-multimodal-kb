# claude-gui · Next.js GUI 代码检索

> 拿 **claude-gui**（一个 Claude agent 监控/配置 dashboard，Next.js + TypeScript）当靶子，测代码 KB 在**中小型真实 TS 项目**上能不能听懂大白话、找到对的符号。
> 中小型项目是代码检索的**入门考**——符号少、歧义少，但 "NL 概念 → 符号" 的语义跳跃仍在。

## 这是什么

- **目标代码**：claude-gui 0.1.0（Next.js 14 + TypeScript）。后端 Fastify + WebSocket（`.mjs`），前端 React/Next（`.ts/.tsx`）。**38 个代码文件 / cmm 192 节点 / 317 边**。
- **cmm 项目名**：`D-claude_code_proj-claude_gui`（你机器不同 → 改 `target.local.json`）。
- **结构**：`src/backend/{server,websocket,routes,services,middleware}` + `src/frontend/{app,components,lib}`。

## 测什么

给一句 NL 大白话（`websocket connection manager broadcast`、`parse raw log into structured entries`、`debounce rapidly fired callback`），看 cmm 能不能在前几个结果里找到对的符号（`WebSocketManager`、`LogParser`、`debounce`）。

18 道题，**全部 NL 概念查询**（非精确名查询）——故意考"概念 → 符号"的语义跳跃，覆盖：
- **后端**：`WebSocketManager` / `LogParser` / `LogWatcher` / `ConfigManager` / `errorHandler` / `healthRoutes` / `configRoutes`
- **前端**：`useWebSocket` / `WebSocketMessage` / `debounce` / `throttle` / `useSystemStore` / `Sidebar` / `Header` / `JsonEditor` / `AgentList` / `cn` / `DashboardPage`

gold = codegraph/cmm 确认的真实符号（构造即正确，零 LLM judge）。`goldgen-verify` 实证验收 **17 pass / 1 review**。

## 最新结果

### 代码检索（2026-07-13 · 18 题）

| 方法 | `broad_recall@5` | strict `recall@5` | 大白话 |
|---|---|---|---|
| **BM25**（cmm 主路） | **0.889** | 0.667 | 前 5 命中 88.9% |
| grep（朴素文本搜索） | 0.000 | 0.000 | NL 概念查询字面匹配全失效 |

→ BM25 在 NL 概念查询上完胜 grep。**grep=0 不是 bug**：18 题全是 NL 句（如 `merge tailwind class names conditionally`），grep 字面匹配不到符号名（`cn`）；bm25 靠语义检索跨过"概念 → 符号"的跳跃。这正是 KB 相对朴素搜索的价值刻度。

### Agent A/B（有 KB vs 无 KB · Stage 0，2026-07-13）

| 臂 | 表现 | 大白话 |
|---|---|---|
| **有 KB**（cmm 注入 top5 符号清单） | `kb_hit@5 = 0.889`，注入 **~155 token** | 注一页符号清单就答对 88.9% |
| **无 KB**（朴素 grep + 读文件） | `grep_miss = 18/18`，平均读到 **~1 token** | 18 题**全部检索失败**，agent 拿到 0 信息 |

→ claude-gui 的"有/无 KB"对比比压缩比更极端：**无 KB 不是"多读几个文件"，而是"完全找不到代码"**（NL 概念查询 grep 字面匹配全失效）。KB 把"答不出"变成"~155 token 答对 88.9%"。

> ⚠ 与 godot-core 不同，本 target **不报压缩比**（`mean_compression_read = 0`）。压缩比的前提是 grep 能命中、只是要读很多 token；claude-gui 纯 NL 题 grep 全 miss（`grep_miss_count = 18`），naive 臂直接 0 信息，compression 无意义。godot 的 12.71× 压缩比适用于它"grep 能命中"的精确名/混合题风——两类题风互补。

## 数字怎么看

- **`broad_recall@5`**（主指标）：前 5 结果里有没有 gold 符号名（名字/路径/全名任一命中）。claude-gui 小库，strict 与 broad 的差距（0.667 vs 0.889）来自 cmm 把类埋在方法节点下的结构问题，和 godot-core 同型。
- **grep=0**：题风偏 NL 概念，grep 天然为 0。对照见 godot-core（它混了精确名查询如 `color`→`Color`，故 grep 有 0.692）——两种题风互补。

## 怎么自己跑

```bash
# 前提：cmm 已索引（cmm_project=D-claude_code_proj-claude_gui）+ codegraph 已 init
bench run code --target claude-gui --method bm25   # 主路（语义检索）
bench run code --target claude-gui --method grep   # 对照（字面搜索）
bench list-reports | grep claude-gui                # 历史
```

> **Windows 装码**：`npm i -g @colbymchenry/codegraph`（**必须带 @colbymchenry scope**——`setup.sh` 里写的 `codegraph` 是 npm 上的撞名空壳包），装完把 `~/AppData/Roaming/npm` 加进 PATH，否则 bench 子进程找不到命令。

## 诚实边界

- **2/18 失分**（bm25 broad@5=0）：`cn`（2 字母超短通用名，bm25 排到 5 名外，返回 `WebSocketManager`/`ConfigManager`）、`useSystemStore`（`zustand global state store` 概念跳跃，bm25 返回 `readGlobalConfig`/`writeGlobalConfig`）。真实检索盲点，非 gold 错误。
- **backend `.mjs` class**（LogParser/LogWatcher/ConfigManager）：`goldgen-verify` 时 `via_cmm=False`（按符号名直查未召回），但 bm25 用 NL query 实跑仍 broad@5=1.0——说明符号在索引里，只是"按名直查"与"NL 语义查"召回路径不同。
- **`WebSocketManager`**：`goldgen-verify` 标 review（同名多模块 `server`/`websocket`），但 broad_recall（名字命中）下不失分，保留。
- **grep=0**：题风纯 NL 概念所致，非检索器故障。

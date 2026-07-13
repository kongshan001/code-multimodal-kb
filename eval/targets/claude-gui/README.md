# claude-gui · Next.js GUI 代码检索

> 拿 **claude-gui**（一个 Claude agent 监控/配置 dashboard，Next.js + TypeScript）当靶子，测代码 KB 在**中小型真实 TS 项目**上能不能听懂大白话、找到对的符号。
> 中小型项目是代码检索的**入门考**——符号少、歧义少，但 "NL 概念 → 符号" 的语义跳跃仍在。本 target 还加了**中英双语 query 对照**，暴露跨语言检索的真空地带。

## 这是什么

- **目标代码**：claude-gui 0.1.0（Next.js 14 + TypeScript）。后端 Fastify + WebSocket（`.mjs`），前端 React/Next（`.ts/.tsx`）。**38 个代码文件 / cmm 192 节点 / 317 边**。
- **cmm 项目名**：`D-claude_code_proj-claude_gui`（你机器不同 → 改 `target.local.json`）。
- **结构**：`src/backend/{server,websocket,routes,services,middleware}` + `src/frontend/{app,components,lib}`。

## 测什么

给一句 NL 大白话，看 cmm 能不能在前几个结果里找到对的符号。**36 道题 = 18 英文 query + 18 中文 query**，gold 完全相同（同一批真实符号），唯一变量是 query 语言——可直接对比"中英文问法"对同一符号的检索差异。

- **英文 query**（NL 概念）：`websocket connection manager broadcast`、`parse raw log into structured entries`、`debounce rapidly fired callback`
- **中文 query**（纯中文概念，不泄露符号名）：`管理长连接并广播消息的类`、`把原始日志文本解析成结构化数据`、`防抖 短时间内多次触发只执行末次`

覆盖符号（中英共享 gold）：
- **后端**：`WebSocketManager` / `LogParser` / `LogWatcher` / `ConfigManager` / `errorHandler` / `healthRoutes` / `configRoutes`
- **前端**：`useWebSocket` / `WebSocketMessage` / `debounce` / `throttle` / `useSystemStore` / `Sidebar` / `Header` / `JsonEditor` / `AgentList` / `cn` / `DashboardPage`

gold = codegraph/cmm 确认的真实符号（构造即正确，零 LLM judge）。英文题 `goldgen-verify` 验收 17 pass / 1 review；中文题为对照追加（gold 同英文，已 accept）。

## 最新结果

### 代码检索（2026-07-13 · 36 题 = 18 英文 + 18 中文）

| 方法 | 英文 query (18) | 中文 query (18) | 全部 (36) |
|---|---|---|---|
| **BM25**（cmm 主路）`broad_recall@5` | **0.889** | **0.056** | 0.472 |
| grep（朴素文本搜索）`broad_recall@5` | 0.000 | 0.000 | 0.000 |

→ 两条独立结论：
- **英文**：BM25（0.889）完胜 grep（0）——cmm 语义检索跨过"概念 → 符号"的跳跃，grep 字面匹配全失效。
- **中文**：BM25 也基本垮（0.056，18 题只 1 题命中）——**cmm 对中文 query 几乎无跨语言能力**。grep 同样 0。

### 中文 query 跨语言（核心发现）

| query 语言 | n | bm25 `broad_recall@5` | 满分率 |
|---|---|---|---|
| 英文 NL | 18 | **0.889** | 16/18 |
| 中文 NL | 18 | **0.056** | 1/18 |

→ **cmm bm25 对中文 query 基本失效**（0.056 vs 英文 0.889，差 ~16×）。根因：BM25 是**词面匹配**，中文 query（`管理长连接并广播消息的类`）与英文符号名（`WebSocketManager`）/ 代码文本词面完全不重叠，跨语言召回近零。18 道中文题 gold 与英文题**完全相同**（同一批真实符号），唯一变量是 query 语言——所以这是**纯粹的跨语言检索弱点**，非 gold 错误、非符号缺失。

中文题唯一命中：`展示任务执行体列表与实时状态` → `AgentList`（"列表"等词恰与代码注释/相关英文词字符级重叠）。

**含义**：对中文为主的团队，cmm 的 bm25 主路不够用——需要 ① agent 先把中文 query 译成英文关键词再查，或 ② semantic/embedding 臂补跨语言，或 ③ 索引层做中文分词。这正是 benchmark 暴露问题的价值。

### Agent A/B（有 KB vs 无 KB · Stage 0，2026-07-13）

| 臂 | 英文 query | 中文 query | 大白话 |
|---|---|---|---|
| **有 KB**（cmm 注入 top5）`kb_hit@5` | **0.889**（~155 token） | **0.056**（~167 token） | 英文：注一页清单答对 88.9%；中文：KB 也救不了 |
| **无 KB**（朴素 grep） | grep_miss 18/18（~1 token） | grep_miss 18/18（~1 token） | 中英都**全部检索失败**，0 信息 |

→ **有/无 KB 在中英下表现分化**：英文题 KB 救场（0.889 vs grep 0）；**中文题 KB 和 grep 都失败**（0.056 vs 0）——cmm 对中文 NL 无论注不注入都接近答不出，根因还是跨语言词面不匹配。

**Token 消耗明细（Stage 0 均值）**：

| 臂 | 输入 token | 命中 gold（英 / 中） | 解读 |
|---|---|---|---|
| 有 KB（cmm 注入 top5 符号清单） | **155–167**（38–241） | 16/18 / 1/18 | token 量与语言无关（都注 top5），命中差在语义层 |
| 无 KB（朴素 grep + 读文件） | **1** | 0/18 / 0/18 | ⚠ token 少是**失效假象** |

⚠ 单看 token 会得出"无 KB 更省（1 < 155）"的**误导结论**：无 KB 的 1 token 不是省，是 grep 全 miss（`naive_file_count` 均值 0）→ 没检索到文件、无内容可注入。**控制变量（都答对题）才可比**：若 grep 能命中，naive 需读 ≤3 文件（ab 配置 `naive_per_file_cap_chars = 4000`）≈ **数千 token**，远高于 KB 的 155 token——这正是 godot-core 12.71× 压缩比的场景。claude-gui 题风纯 NL，grep 连命中都做不到，故只给有效性维度。

> ⚠ 与 godot-core 不同，本 target **不报压缩比**（`mean_compression_read = 0`）：压缩比前提是 grep 能命中、只是要读很多 token；claude-gui 纯 NL 题 grep 全 miss（`grep_miss_count = 36`），naive 臂 0 信息，compression 无意义。

## 数字怎么看

- **`broad_recall@5`**（主指标）：前 5 结果里有没有 gold 符号名（名字/路径/全名任一命中）。strict 与 broad 的差距（英文 0.667 vs 0.889）来自 cmm 把类埋在方法节点下的结构问题，和 godot-core 同型。
- **grep=0**：题风偏 NL 概念，grep 天然为 0。对照见 godot-core（混了精确名查询如 `color`→`Color`，故 grep 0.692）——两种题风互补。
- **中文 0.056**：BM25 词面匹配的跨语言真空。不是符号不在索引里（英文同 gold 能 0.889），是中文 query 触达不到英文符号的词面。

## 怎么自己跑

```bash
# 前提：cmm 已索引（cmm_project=D-claude_code_proj-claude_gui）+ codegraph 已 init
bench run code --target claude-gui --method bm25   # 主路（36 题，中英都跑）
bench run code --target claude-gui --method grep   # 对照
bench run ab   --target claude-gui                  # 有/无 KB token 对比
bench list-reports | grep claude-gui                # 历史
```

> **Windows 装码**：`npm i -g @colbymchenry/codegraph`（**必须带 @colbymchenry scope**——`setup.sh` 里写的 `codegraph` 是 npm 上的撞名空壳包），装完把 `~/AppData/Roaming/npm` 加进 PATH，否则 bench 子进程找不到命令。

## 诚实边界

- **英文 2/18 失分**（bm25 broad@5=0）：`cn`（2 字母超短通用名，bm25 排到 5 名外，返回 `WebSocketManager`/`ConfigManager`）、`useSystemStore`（`zustand global state store` 概念跳跃，bm25 返回 `readGlobalConfig`/`writeGlobalConfig`）。真实检索盲点，非 gold 错误。
- **中文 17/18 失分**：BM25 跨语言词面不匹配，非 gold 错误（gold 与英文题同源，英文 16/18 命中）。唯一命中的 `AgentList` 是字符级巧合。
- **backend `.mjs` class**（LogParser/LogWatcher/ConfigManager）：`goldgen-verify` 时 `via_cmm=False`（按符号名直查未召回），但英文 bm25 用 NL query 实跑仍 broad@5=1.0——"按名直查"与"NL 语义查"召回路径不同。
- **`WebSocketManager`**：`goldgen-verify` 标 review（同名多模块 `server`/`websocket`），但 broad_recall（名字命中）下不失分，保留。
- **grep=0**：题风纯 NL 概念所致，非检索器故障。
- **中文题未单独跑 goldgen-verify**：gold 复用英文题同源符号（已验证真实），仅 query 措辞改中文；如需可对中文题补跑 `goldgen-verify`（零 LLM，验可检索性）。

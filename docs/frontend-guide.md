# 前端使用说明 · Measurement Lab

> bench 评测系统的可视化界面。命令行的每一句，这里都有一个对应的页面。
> 起一个命令，浏览器开——不用记 CLI 参数。

---

## 1. 起服务

```bash
# 方式一：bench 子命令（推荐，加 alias 后直接 bench web）
python -m eval.cli web --port 8765

# 方式二：直接跑 server 模块
python -m eval.server --port 8765
```

终端输出：
```
measurement lab → http://127.0.0.1:8765
  环境 就绪 ✓          # 或 ⚠ 有缺项（进 Setup 视图装）
  报告 16 份归档
  Ctrl-C 停
```

浏览器打开 **http://127.0.0.1:8765** → 自动进 Dashboard。

**停服务**：终端 `Ctrl-C`。

---

## 2. 界面布局

```
┌──────────┬──────────────────────────────────────┐
│          │                                      │
│ 接入     │                                      │
│  环境体检 │           主视图区                    │
│  目标接入 │     （Dashboard / Reports / ...）     │
│          │                                      │
│ 评测     │                                      │
│  Dashboard│                                      │
│  Run console│                                   │
│  归档     │                                      │
│  对比     │                                      │
│  Gold lab │                                      │
│          │                                      │
└──────────┴──────────────────────────────────────┘
   左侧导航           右侧内容（hash 路由切换）
```

点左侧导航切视图。URL 带 `#/view-name`，可直接书签/分享。

---

## 3. 八个视图 · 逐个说明

### 3.1 Dashboard（首页 · 一眼看全貌）

**打开即看**：4 个大数字——系统最硬的结论一眼可见。

| 指标 | 含义 | 示例值 |
|---|---|---|
| 代码检索 broad@5 | cmm 在你的代码库上的召回率 | 0.846 |
| 记忆召回 hit@5 | MemPalace 召回准确率 | 0.933 |
| A/B 压缩比 | 有 KB vs 无 KB 的 context token 压缩 | 12.71× |
| 答案 faithfulness | RAG 答案忠实度（LLM-judged） | 0.971 |

下方**归档列表**：最近 8 次评测，点行进详情。

### 3.2 Run console（触发评测）

**从浏览器跑 benchmark**，不用开终端。

1. 选 **subject**（code/memory/ab/doc-ragas）
2. 填 **target**（target id，如 godot-core / engineer-demo-memory）
3. 选 **method**（bm25/grep/semantic，仅 code 需要）
4. 点 **"跑 ▸"**
5. 等几十秒（后端 subprocess 调 `eval.cli`），结果显示在下方

跑完自动归档，Dashboard 刷新即可见。

> ⚠ agent A/B（ab-agent）和 memory-quality 暂需 CLI 跑（需 LLM 凭据 + 较长时间），前端暂只支持 code/memory/ab/doc-ragas。

### 3.3 归档（Reports archive）

**所有历史评测**：16+ 份归档报告，按时间倒序。

| 列 | 含义 |
|---|---|
| id | 归档唯一标识（时间戳+subject+variant）|
| subject | 评测对象（cmm.bm25 / mempalace / ab-agent-stage1 ...）|
| variant | 变体（godot-bm25 / engineer_demo / ...）|
| ts | 时间 |
| headline | 主指标摘要 |

点任意行 → 进 Report detail。

### 3.4 Report detail（单份报告详情）

展开一份报告的全部数据：
- **aggregate**：所有聚合指标（recall@k / hit@k / faithfulness / 压缩比 ...）
- **per_query**：逐题明细（query + 各指标值）
- **lockfile**：版本锁定（cmm/graphify/mempalace 版本 + temp + LLM 模型）

> 带 `LLM-judged` 徽标的指标 = 同家族 GLM 判分（self-preference 风险，当相对值看）。

### 3.5 Compare（两份报告对比）

**看改了什么后效果变好/变差了**：

1. 左下拉选一份报告（改前）
2. 右下拉选一份报告（改后）
3. 点 **"对比 ▸"**
4. 显示 metric × {left, right, delta} 表——每行一个指标的差值

典型用法：跑了两次 code（bm25 vs grep），对比看 recall@5 差多少。

### 3.6 Setup · 环境体检（接入段）

**检查环境是否齐**，缺什么一目了然。

- **KB 工具**：cmm / graphify / codegraph / mempalace —— 每项 ✓ 版本号 或 ✗ 缺
- **Python / 渲染 / 凭据**：pytest+anthropic / rsvg-convert / GLM key —— 同上
- **健康门禁**：顶端绿灯"环境就绪"或黄灯"有缺项"
- **依赖坑提示**：每项附注（如 mempalace "Intel Mac 必须 py3.11"、python "✗ 勿装 ragas"）

缺项装法：终端跑 `./setup.sh tools`（或 `./setup.sh python` 等）。

### 3.7 Project · 目标接入（接入段 · 5 步向导）

**把自己的代码库接进来跑 benchmark**——5 步走完。

| 步 | 做什么 | 命令 | 注意 |
|---|---|---|---|
| 01 连代码库 | 填路径 → codegraph 建索引 | `codegraph init <path>` | 静态零 LLM，秒级 |
| 02 文档图（可选）| 填文档目录 → graphify 建图 | `graphify build <path>` | ⚠ **花 LLM 钱**，先看成本估算 |
| 03 会话 mine（可选）| 填 ~/.claude/projects/ → mempalace mine | `mempalace mine <path>` | ⚠ **勿配 auto-save hook**（会 bloat，见 runbook §D.4）|
| 04 生成 gold | → 跳 Gold lab | goldgen | 给自己的代码造测试题 |
| 05 就绪 | → 跳 Run console | bench run | 跑自己的系统 |

每步：填路径 → 点"跑"→ 看输出（exit code + stdout 摘要）。可跳过/重跑。

### 3.8 Gold lab · 题库编辑器（评测段）

**直接在浏览器读写题库** `eval/targets/<id>/problems.json`——列表 / 新增 / 改 / 删 / approve pending，不碰命令行、不手编文件。

顶部先选 **target**（下拉，列全部 target）。然后两条路：

**自动造题**（code_retrieval target）：
```
① goldgen     填 seed 词（如 "Vector color Node"）→ codegraph 枚举真实符号 + GLM 拟 NL 题
              （gold = 符号，构造即正确，零 LLM judge）→ 候选以 status: pending 进表
② 实证验收    codegraph 查同名歧义（零 LLM），在 pending 候选原地标 verdict
✓ approve     逐条审：好的点 ✓ approve（status→accepted），差的点 🗑 删
```

**手动增/改/删**：右上 "+ 新增题目" 或行尾 ✎ → 表单。**type 下拉决定 gold 字段**：
- `code_retrieval` → symbols（逗号分）
- `doc_retrieval` → node_labels
- `cross_anchor` → doc_node_label / cmm_identifier / code_file
- `memory_recall` → source_files
- `memory_routing` → layer（objective/procedural/episodic/subjective）+ signal

行尾 🗑 删除（带确认）。

**前端不自动 git commit**——任何写操作后顶部亮"待提交"黄条，提示你 `git add eval/targets/ && git commit && git push`（带"已提交，隐藏"按钮）。后端 schema 校验：type 非法 / gold 形状不匹配 / query 空 → 400 + 中文错误，文件不动。

---

## 4. 典型工作流

### A. "我想看我的 KB 好不好"

1. `bench web` → Dashboard 看 4 个 hero 指标
2. 点归档行 → Detail 看逐题明细
3. 对比两次 → Compare 看 delta

### B. "我想 benchmark 一个新代码库"

1. Setup → 确认环境就绪（缺项先 `./setup.sh tools`）
2. Project onboarding → 01 填你的代码库路径 → codegraph init
3. Gold lab → 填 seed 词 → 挖拟题 → 验收 → fold（生成你的 gold）
4. Run console → 选 subject + target → 跑
5. Dashboard → 看结果

### C. "我改了检索策略，效果变好了吗"

1. Run console → 跑一次（改后）
2. Compare → 左选改前归档、右选改后归档 → 看 delta

### D. "我想扩测试题"

1. Gold lab → 选 target → 填 seed 词（指一片代码区域，如 "physics collision"）→ ① goldgen
2. ② 实证验收 → pending 候选逐条 ✓ approve（好的）/ 🗑 删（差的）
3. 改完记得 `git commit`（前端顶部"待提交"黄条会提示）

---

## 5. 技术细节

| 项 | 值 |
|---|---|
| 后端 | `eval/server.py`（stdlib http.server，**零额外依赖**）|
| 前端 | `web/`（vanilla JS SPA，**无构建步骤**）|
| API | `/api/reports` `/api/report/<id>` `/api/health` `/api/run` `/api/goldgen*` `/api/onboard` `/api/pending/<target>` |
| 美学 | Measurement Lab（奶油底 #f8f6f3 + Fraunces/JetBrains Mono + 烟花橙 #c75b39）|

后端不改 CLI——前端是消费层，`eval.cli` 仍是自动化/CI 通路。

---

## 6. 排错

| 问题 | 解 |
|---|---|
| 页面空白/loading 卡住 | 后端没起？检查 `python -m eval.cli web` 终端有无报错 |
| `/api/health` 显示有缺项 | 终端跑 `./setup.sh tools` 装缺的工具 |
| Run console 跑出来 exit≠0 | 看 stdout/stderr 输出；多半是工具没装好或索引未建 |
| Gold lab "无 pending" | 先点"① 挖+拟题"生成候选，再"③ 看候选" |
| Onboarding codegraph init 失败 | 确认路径存在 + codegraph 已装（`./setup.sh tools`）|
| 端口 8765 被占 | `--port 8766` 换一个 |
| 旧页面缓存（显示过时）| URL 加 `?v=2` 强制刷新（或浏览器 hard refresh）|

---

## 7. 与 CLI 的对应关系

| 前端视图 | 对应 CLI 命令 |
|---|---|
| Dashboard | `bench list-reports`（聚合）|
| Run console | `bench run <subject> [--target] [--method]` |
| Reports | `bench list-reports` |
| Detail | `bench show <id>` |
| Compare | `bench compare <id1> <id2>` |
| Setup | `./setup.sh python/tools/creds` |
| Onboarding | `codegraph init` / `graphify build` / `mempalace mine` |
| Gold lab | `bench goldgen` / `goldgen-verify` + 题库 CRUD（`/api/gold/*`，前端编辑器）|

**前端和 CLI 完全等价**——同一后端，两种入口。自动化用 CLI，日常用前端。

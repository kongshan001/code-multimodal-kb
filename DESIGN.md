# DESIGN.md · Measurement Lab 设计系统

> **给 AI 编程 agent 的设计记忆。** 这个文件同时伺候两类读者：YAML 令牌给机器精确值，
> Markdown 散文告诉 AI 这些值背后是什么意图、什么时候用、什么时候绝对不能用。
>
> **每次改前端前先读这个文件。** 它是设计一致性的唯一真相源。

---

## 设计参照（一句话锚定，不是形容词清单）

> **Edward Tufte 设计的一份 benchmark 报告 + 实验室记录本的温度。**
>
> 想象一份 1970 年代老牌大学的讲义：暖色纸张底、衬线标题像学术期刊的版面、
> 等宽字体像终端输出和实验数据、表格密度高但不拥挤、留白克制但呼吸感够。
> 它不发光、不用渐变、不追求"科技感"——它追求的是**可信、可读、像一份认真的出版物**。

这个参照锚定了以下所有决策。当你犹豫"该不该加某个效果"时，问自己：**Tufte 的讲义会这样做吗？**

---

## YAML 设计令牌

```yaml
colors:
  # 底色系——暖纸，不是冷灰
  cream: "#f8f6f3"          # 主背景，像旧纸
  ink: "#1a1814"            # 主文字，暖黑不是纯黑
  ink2: "#5a544a"           # 次要文字，暖灰
  rule: "#d9d2c4"           # 分割线/边框，淡棕灰

  # 强调色——克制的大地色系
  accent: "#c75b39"         # 赤陶橙，用于关键数字/链接/激活态（唯一的"热"色）
  teal: "#9dd4c7"           # 柔青，用于正向数据/KB 相关
  beige: "#f4e4c1"          # 米黄，用于背景区分

  # 语义色——低饱和，不像红绿灯
  good: "#3f7d5f"           # 深绿（通过/提升）
  warn: "#b07a1e"           # 琥珀（警告）
  bad: "#b3462a"            # 砖红（失败/下降）

  # 绝对不用
  # - 纯黑 #000 / 纯白 #fff（太冷，破坏暖纸感）
  # - 霓虹色 / 荧光色（不属于讲义）
  # - 蓝紫色系（SaaS dashboard 味，不是学术出版物）

typography:
  heading: "Fraunces"          # 衬线，标题/品牌，有文学温度
  body: "IBM Plex Sans"        # 无衬线，正文，清晰可读
  mono: "JetBrains Mono"       # 等宽，所有数据/数字/代码/标签
  # 字号层级
  size_h1: 38px                # 页面标题
  size_h2: 22px                # 段落标题
  size_body: 15px              # 正文
  size_data: 12px              # 表格/数据
  size_label: 9px              # 标签/uppercase 小字
  # 绝对不用
  # - Inter / Roboto / system-ui（太通用，没有性格）
  # - 标题用无衬线（失去编辑器身份）
  # - 数据用非等宽（失去实验室精确感）

spacing:
  base: 8px                    # 基准网格单位
  page_padding: 40px 44px      # 主内容区内边距
  card_padding: 22px 20px      # 卡片内边距
  section_gap: 32px            # 段落间距
  # 原则：慷慨但不浪费——Tufte 的留白是呼吸，不是空虚

radius:
  card: 10px                   # 卡片圆角，柔和但不圆滑
  button: 2px                  # 按钮近直角，编辑器感
  # 绝对不用 >16px 圆角（太"app"，不够出版物）

shadow:
  card_rest: "0 1px 3px rgba(26,24,20,0.04)"     # 极淡，仅暗示深度
  card_hover: "0 8px 20px rgba(26,24,20,0.08)"    # hover 时加深
  # 绝对不用重阴影（不是 material design，不是卡片堆叠游戏）

motion:
  duration: "0.15s"            # 过渡时长，快但不突兀
  easing: "cubic-bezier(0.4, 0, 0.2, 1)"         # 标准缓动
  # 原则：过渡是润滑，不是表演。Tufte 的讲义不弹跳、不滑入。
  # 绝对不用：bounce / elastic / >0.3s 动画 / 连续循环动画（除非进度条）
```

---

## 散文：设计意图（比令牌重要）

### 这个界面是什么

Measurement Lab 是一个 **benchmark 评测系统的可视化前端**——给开发者看的数字仪表盘，
不是给终端消费者的产品页面。用户是工程师/研究者，他们要的是：**数字准、层级清、一眼找到要的指标**。

### 核心视觉隐喻：实验室记录本

整个界面的视觉身份是 **"一份认真的实验室记录本"**：

- **暖色底（cream #f8f6f3）**：像旧纸/牛皮纸，不是冷冰冰的灰白。传达"这是人做的认真工作"，不是机器自动生成的。
- **衬线标题（Fraunces）**：像学术期刊的版面标题。有文学温度，不是冰冷的 Helvetica。
- **等宽数据（JetBrains Mono）**：所有数字/指标/代码都用等宽。传达"这是精确的测量数据"，像终端输出。
- **赤陶橙强调（accent #c75b39）**：唯一的"热"色。用于关键数字、激活状态、链接。克制使用——整个页面不应该超过 3-4 处 accent。
- **线条而非色块**：用细线（1px rule）分隔区域，不用粗边框/色块。Tufte 原则——数据墨水比最大化。

### 什么时候用什么

| 场景 | 用什么 | 为什么 |
|---|---|---|
| 页面标题 | Fraunces 38px 800 | 期刊封面感 |
| 段落标题 | Fraunces 22px 600 + 编号 | 章节编号，像论文结构 |
| 数字指标 | JetBrains Mono 32px 700 | 等宽对齐，精确感 |
| 表格数据 | JetBrains Mono 12px | 密度高但可读 |
| 标签/分类 | JetBrains Mono 9px uppercase + letter-spacing | 像实验标签 |
| 正文 | IBM Plex Sans 15px | 清晰可读，不抢数据 |
| 卡片 | 10px 圆角 + 极淡阴影 | 有深度但不"飘" |
| 按钮 | 2px 圆角 + 边框 | 近直角，编辑器感 |
| 悬浮 | translateY(-2~3px) + shadow 加深 | 暗示可交互，但不弹跳 |

---

## 禁止项（不做定义性格）

> 以下是**绝对不能做的**。它们不属于这个设计宇宙。如果你想做这些，你走错了方向。

1. **不用渐变背景**（sidebar 的微妙白→cream 除外）。讲义是纯色纸，不是 gradient mesh。
2. **不用毛玻璃 / glassmorphism / backdrop-filter**。对比度硬伤 + 不属于纸质隐喻。
3. **不用深色模式**。暖色 cream 底是身份核心。如果非要做暗色，那是另一个设计系统。
4. **不用霓虹/荧光色**。大地色系是底线。
5. **不用圆角 >16px**。10px 是上限。更圆 = 更"app" = 更不像出版物。
6. **不用重阴影 / 多层投影**。阴影仅暗示深度（0-8px），不是 material elevation。
7. **不用 emoji 当 UI 图标**。用文字标签或几何符号（▸ ✓ ✗ →）。
8. **不用弹跳/弹性动画**。cubic-bezier 标准缓动是上限。
9. **标题不用无衬线字体**。衬线 = 编辑器身份。
10. **不用 blue/purple 主色调**。那是 SaaS dashboard 的默认色，不是这里的。

---

## 组件级指导

### Hero 指标卡
- 独立卡片（不共享 border），10px 圆角，极淡阴影。
- hover 时 translateY(-3px) + shadow 加深 + 顶部 accent 色条淡入。
- 入场用 fadeUp 动画（错峰 0.05s 递增），但不循环。
- 数字用 JetBrains Mono 32px，标签用 9px uppercase。

### 表格
- 斑马纹（偶数行 cream 40% 透明）。
- hover 时整行白底 + 左侧 3px accent 色条。
- 表头 JetBrains Mono 9px uppercase。
- 数据 JetBrains Mono 12px。

### 侧边栏
- 渐变背景（白→cream），200px 宽。
- 导航项 hover → cream 底；active → 左侧 accent border + cream 底。
- 自定义 4px 细滚动条。

### 按钮
- 近直角（2px），边框 + 白底。
- hover → translateY(-1px) + cream 底。
- `.fill` 变体：accent 底 + 白字。

### Compare 差值
- 正向 delta → `--good` 绿色 + `+` 前缀。
- 负向 delta → `--bad` 红色。
- 零/无数据 → `--ink2` 灰色。

---

## 当前实现位置

| 文件 | 角色 |
|---|---|
| `web/app.css` | 设计令牌（`:root` 变量）+ 组件样式 |
| `web/app.js` | SPA 逻辑（views、routing、API） |
| `web/index.html` | 结构 + 字体加载 |
| `eval/server.py` | HTTP 服务（端口 8765） |
| **本文件** | 设计意图 + 令牌定义 + 禁止项（**改 CSS 前先读**） |

"""记忆侧 gold 集（task 4.2 / 4.3）。

两部分：
  RECALL_GOLD  — (nl_query, gold_source_files) 用于测 MemPalace 召回 recall@k / hit@k。
  ROUTING_GOLD — (candidate_fact, gold_layer) 用于测 D1 四层路由准确率。

gold 来源（诚实标注）：
  - RECALL_GOLD 的 gold_source 是**实测可召回**的 source_file（仿 gold_godot 锚真实
    符号）：4 个 memory 文件（agent-memory-approach / prefer-global-tool-sharing /
    commit-every-change-to-git / MEMORY.md）+ 4 个会话 jsonl（经 mempalace search 探测
    确认其内容含答案）。memory 文件召回干净；会话碎片召回偏松散（见报告盲区分析）。
  - ROUTING_GOLD 是人工标注的 4 类候选事实（客观/程序/事件/主观各 3–4 条），
    覆盖 D1 归属规则的可操作场景；signal 字段标注判定线索，便于 router 调试。

所有 source_file 取 mempalace search 输出的 `Source:` basename（不含路径）。
"""
from __future__ import annotations

# ── 召回 gold：主观记忆按主题召回 ──────────────────────────────────────────
# 每个 query 是用户/agent 会自然问的 NL；gold_source_files 是其内容确实回答该 query
# 的 source_file 集合（召回任一即算命中）。前 8 条锚 memory 文件（主观层应强召回），
# 后 7 条锚会话（情景/程序内容）。其中 "记忆四层归属"、"文档质量 429" 是诚实探针：
# 答案原文在 CLAUDE.md / 报告（未被 mine），仅会话碎片提及 → 预期召回偏弱。

# 主观层目标（memory/*.md）—— 应干净召回
_MEMORY_APPROACH = "agent-memory-approach.md"
_GLOBAL_TOOLS = "prefer-global-tool-sharing.md"
_COMMIT_DISC = "commit-every-change-to-git.md"
_MEMORY_IDX = "MEMORY.md"

# 会话目标（jsonl，已 mine）—— 内容经探测确认含答案
_SESS_RULES = "f4c1e4e6-d496-4489-a33b-a9c43b6bdac8.jsonl"      # openspec/记忆规则主会话
_SESS_INSTALL = "de6c53eb-9070-4c8d-8ea1-70ff16c41f83.jsonl"     # MemPalace 安装 + benchmark 跑数
_SESS_ARCH = "4cc582e9-94b7-4559-a0b6-c9f668c50c08.jsonl"        # 图检索 vs 向量（architecture room）
_AGENT_ANCHOR = "agent-af1fd348c7bad4c83.jsonl"                  # anchoring 阈值对抗 review

RECALL_GOLD: list[tuple[str, set[str]]] = [
    # ── memory 文件目标（主观层，应强召回）──
    ("记忆层选型 MemPalace 还是 Mem0", {_MEMORY_APPROACH}),
    ("为什么不用 Mem0 改用 MemPalace", {_MEMORY_APPROACH}),
    ("Mem0 三容器凭据墙阻塞", {_MEMORY_APPROACH}),
    ("工具 skills commands 全局共享 ~/.claude", {_GLOBAL_TOOLS}),
    ("openspec skills 提取到全局 ~/.claude", {_GLOBAL_TOOLS}),
    ("每次改动提交 git main 并 push", {_COMMIT_DISC, _MEMORY_IDX}),
    ("commit message 结尾 Co-Authored-By", {_COMMIT_DISC, _MEMORY_IDX}),
    ("MEMORY.md 索引现在有几条记忆", {_MEMORY_IDX}),
    # ── 会话目标（情景/程序， mined 碎片）──
    ("新需求一律走 openspec 先 spec 后码", {_SESS_RULES}),
    ("Intel Mac onnxruntime 必须 python 3.11 装 mempalace", {_SESS_INSTALL}),
    ("代码检索 BM25 broad@5 0.846 grep 0.692", {_SESS_INSTALL}),
    ("跨工具 anchoring 文档到代码 成功率", {_AGENT_ANCHOR, _SESS_INSTALL}),
    ("图检索对精确片段召回弱于向量", {_SESS_ARCH}),
    # ── 诚实探针：答案原文未 mine，预期偏弱 ──
    ("记忆四层归属判定测试金句", {_SESS_RULES}),
    ("文档答案质量 faithfulness 卡 429 限流", {_SESS_RULES}),
]


# ── 路由 gold：D1 四层归属准确率 ──────────────────────────────────────────
# 四类：objective(客观→KB) / procedural(程序→skills) /
#       episodic(事件→git/tasks) / subjective(主观→memory)
# 每条 signal 标注人类判定线索；router 用规则近似该判定（见 routing.py）。
# 注：本集为人工标注，router 是规则近似——高准确率部分源于集与规则同源，
# 真实泛化需更大标注集（见报告边界）。

ROUTING_GOLD: list[tuple[str, str, str]] = [
    # 客观（代码/文档本身说了什么 → KB）
    ("cmm 的 search_code 接口返回 node 和 file 字段", "objective", "API 结构事实"),
    ("metrics.py 的 recall_at_k 计算 top-k 命中 gold 的比例", "objective", "代码事实"),
    ("graphify 文档图节点带 source_location 属性", "objective", "文档结构事实"),
    # 程序（如何做 → skills）
    ("部署 MemPalace 用 uv tool install --python 3.11", "procedural", "安装步骤"),
    ("跑代码侧评测用 bench run code --target godot --method bm25", "procedural", "运行命令"),
    ("给项目装 openspec 工具的步骤", "procedural", "how-to"),
    # 事件（何时做了何事 → git/tasks）
    ("2026-07-11 归档了 add-agent-memory change", "episodic", "日期+事件"),
    ("commit a940259 同步了 agent-memory 主 spec", "episodic", "commit SHA+事件"),
    ("昨天装好 MemPalace 3.5.0 并 mine 了 1484 drawers", "episodic", "时态+事件"),
    # 主观（用户/工作方式/决策 → memory）
    ("用户偏好工具装全局 ~/.claude 共享", "subjective", "用户偏好"),
    ("记忆层选型决定走 MemPalace 而非 Mem0", "subjective", "决策结论"),
    ("每次改动都要提交 git main 并 push", "subjective", "工作方式铁则"),
    ("用户最看重 agent 用证据消解不确定", "subjective", "用户工作偏好"),
]

LAYERS = ("objective", "procedural", "episodic", "subjective")

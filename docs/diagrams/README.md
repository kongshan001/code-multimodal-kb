# 流程图索引（fireworks-tech-graph 生成）

> 用 [fireworks-tech-graph](https://github.com/yizhiyanhua-ai/fireworks-tech-graph) skill（style 6 Claude 官方风）从工程实际产出绘制。
> SVG 为源（GitHub README 原生渲染）；PNG 由 cairosvg/rsvg-convert 导出（1920px）。

## 1. 系统架构（D1 记忆四层归属 + Benchmark 评测）

![系统架构](architecture.svg)

四层归属纪律（D1 判定金句）+ 顶部 Benchmark 评测层。候选事实经「忘了这条 agent 会不会被纠正？」路由到：
- **会纠正 → Memory**（MemPalace，主观层）
- **被问起 → KB**（cmm + graphify，客观层）
- **怎么做 → Skills**（~/.claude/skills，程序层）
- **何时发生 → Git/OpenSpec**（情景层）

## 2. Agent A/B Benchmark 流程（有 KB vs 无 KB）

![A/B 流程](ab-benchmark-flow.svg)

同一批 gold_godot 26 题，两 stage：
- **Stage 0**（零 LLM token 代理）：KB 注入 vs 朴素 grep+读 → 压缩 12.7× / kb_hit@5=0.846
- **Stage 1**（真跑 agent loop）：四臂 baseline/kb/doc/codegraph 对照 → 准确度 + token + 步数

注册表 `ab_tools.py`：接新 KB = executor + register + 挂臂，loop/判分零改。

## 3. Goldgen 扩题流程（agent 挖题 + 两层验收 + 人审）

![Goldgen 流程](goldgen-flow.svg)

低成本扩 gold 集，**人审前过两层自动 vet**：
- ① generate：codegraph 枚举真实符号 + LLM 拟题（gold 构造即正确，零 judge）
- ② 实证 verify（零 LLM）：抓同名歧义
- ③ 独立 subagent 验收：抓 NL query↔gold 语义错配（实证漏的）
- ④ 人审 → fold 进 gold

成本分离：gold 自证（0）+ LLM 拟措辞（便宜）+ 人审 query（轻）。

## 4. ab_agent.py — run_episode() 执行流程

![run_episode 执行流程](ab_agent_flow.svg)

Stage 1 agent loop 控制流（ReAct + token 累计 + 429 退避 + 收敛纪律）：初始化 → 迭代守卫 `i < max_steps` → `_create_with_retry()` LLM 调用 → 序列化本轮响应/累计 token → 判定 `stop_reason`：
- **tool_use**（循环回边）：遍历 tool_use blocks → `_exec_tool` / `ab_tools.exec_tool` → 截断 2000 写回 messages → 下一轮 `i++`
- **end_turn**：`break` 直接收尾
- **max_steps 耗尽**（for-else）：`truncated=True` + 强制作答（再调 LLM，`tools=[]` 禁 tool_use）→ 收尾

## 5. ab_agent.py — LLM 调用链路（_create_with_retry）

![LLM 调用链路](ab_agent_llm_call.svg)

聚焦 LLM 如何被调用（第 4 节的子流程细化）：调用入口（主循环带 tools / 强制作答 `tools=[]`）→ `make_client()` + `load_creds()`（env 优先，否则 `~/.cc-connect/config.toml`，都无 `RuntimeError`）→ `client.messages.create`（glm-5.x · max_tokens=1024 · temperature=0）：
- **成功**：累计 `resp.usage` tokens、`llm_calls++`、返回 resp
- **可重试异常**（RateLimit / 429 / 500·502·503·529）：`sleep 2^i`（1,2,4,8s）指数退避 → 回到 create；重试 5 次仍失败 → `RuntimeError`
- **其他异常**：直接 `raise` 中断 episode

## 6. bench 完整测试流程（dock → 造题 → 验收 → 人审 → 跑分 → 报告）

![bench 完整流程](bench-full-flow.svg)

端到端 6 阶段，每阶段含「做什么 + 实现原理」：
- **① Dock**：建 `target.json` + `cmm`/`graphify` 索引（索引一次查询多次；引擎零硬编码路径）
- **② 造题 goldgen**：codegraph 枚举真实符号（gold 自证正确）+ LLM 仅拟 NL query 措辞 → 零 judge
- **③ 验收 goldgen-verify**：实证（同名歧义 / 检索一致，零 LLM）+ 独立 subagent 语义匹配
- **④ 人审 approve**：前端 approve 翻 `status`（唯一主观关口，前端不碰 git）
- **⑤ 跑分**：Stage 0（零 LLM token 代理：cmm bm25 vs grep+读 top3，压缩比 / kb_hit@5 / grep 盲区率）｜ Stage 1（真跑 4 臂 agent loop，准确率 / token / cost）
- **⑥ 报告**：`result.md` + `summary.json` + `arms/<arm>/` 目录（人读 + 程序双出口，诚实边界标注）

---

## 重新生成

```bash
# 装渲染器（任一）：brew install librsvg ｜ pip install cairosvg（需 libcairo）
# SVG 源在 docs/diagrams/*.svg，可直接编辑后重导 PNG：
rsvg-convert -w 1920 architecture.svg -o architecture.png
```

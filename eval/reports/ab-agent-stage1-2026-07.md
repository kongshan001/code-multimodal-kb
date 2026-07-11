# Agent A/B Stage 1 报告 · 2026-07-11（真跑 agent，准确度 + token + 效率）

> Stage 0（`ab-value-baseline-2026-07.md`）证了**检索层** KB 省 context token。本报告是 **Stage 1**：
> 真跑 agent loop（glm-5.x，temp=0），测"配 vs 不配代码 KB"在 **agent 终答准确度 + 端到端 token + 步数**
> 上的差异——回答用户最核心的"这套系统到底让 agent 干得更好/更省吗"。
> 数字来自归档 `reports/archive/20260711T120018Z-ab-agent-stage1-godot-stage1-r1.json`（`bench run ab-agent` 实跑），
> 可由 `eval/run_ab_agent.py` 复现。LLM 走本地 cc-connect 的 zhipu/BigModel anthropic 端点（不入库）。

## 0. 实验设置

| 项 | 值 |
|---|---|
| 题集 | gold_godot 26 条代码定位题（符号 gold，零 LLM judge） |
| Arm A baseline | agent + {grep_code, read_file}（朴素检索） |
| Arm B KB | agent + {cmm_search, read_file}（差异 = 发现工具：词面 grep vs 语义 KB） |
| LLM | glm-5.x（BigModel anthropic 兼容），temp=0，max_steps=6 |
| 判分 | 终答命中（gold ∈ 终答，broad 子串）+ 检索命中（gold ∈ 终答 ∪ 工具结果） |
| 重复 | 1 run（单 run；方差见 §4 边界） |

## 1. 核心结果

```
                      baseline      KB          差距 (KB − baseline)
终答准确度             0.923 (24/26) 0.923 (24/26)  0.0   ← 并列天花板
检索命中               0.923         0.923          0.0
mean 总 token          1625          688           −936.5 (−58%)  ◀ KB 大幅省 token
mean input token       1360          507           −853 (−63%)
mean 步数              3.42          2.12          −1.3 (−38%)
token / 正确答         1760          746           −1014  → KB 2.4× 更省
truncated              1/26          0/26          prompt 收敛纪律生效
```

**一句话价值**：配代码 KB 的 agent 与朴素 grep agent **答对率相同（0.923，并列天花板）**，
但 KB 用 **58% 更少的 token**、**2.4× 更低的"每对一答成本"** 拿到同样结果——**KB 的价值在
经济性，不在准确度上限**。

## 2. 准确度：为什么并列而不是 KB 赢？

两臂都 24/26，**漏的是不同的题**（互补，非谁压谁）：

| 漏题 | baseline | KB | 根因 |
|---|---|---|---|
| `string format`→vformat | ✗ | ✗ | 共漏：概念词代码里不出现（硬限，见 value-benchmark §2.3） |
| `int to string`→itos | ✗ | ✓ | KB 救回：cmm 语义检索到 itos（grep "int to string" 0 命中） |
| `delete object free memory`→memdelete | ✓ | ✗ | baseline 救回：grep "delete/free" 命中（cmm 没把聚合宏排上来） |

→ **天花板 0.923 是检索无关的硬限**（概念盲区）。baseline 的 grep 在这些**精确名为主的题**上已经够准，
KB 没有准确度提升空间——但 KB **救回了 grep 救不动的概念题**（int to string），丢了一道 grep 能拼到的（delete object）。

## 3. Token / 效率：KB 的真实价值（用户诉求 ①③）

| 维度 | baseline | KB | 价值 |
|---|---|---|---|
| 总 token（每题） | 1625 | 688 | **省 58%** |
| input token | 1360 | 507 | 省 63%（KB 注入更精，不需读大文件） |
| 步数 | 3.42 | 2.12 | 少 38%（KB 一次命中即答，grep 要 grep→读→定位） |
| token/正确答 | 1760 | 746 | **2.4× 成本效率** |

26 题总量：baseline ~42k token vs KB ~18k token，**省 ~24k token**。与 Stage 0 的"context 压缩 12.7×"
一致——KB 在检索层省的 token，**在 agent 层兑现成了端到端 token 节省 + 更少步数**。

## 4. 诚实边界（引用须注明）

1. **准确度并列 ≠ "KB 没用"**：baseline grep 在精确名题上已够准；KB 的差异化在**概念题补救**（int to string）
   + **token 经济性**。换更难/更概念化的题集（KB 的主场），准确度差可能拉开。
2. **单 run，n=26**：temp=0 但 agent tool-use 仍有非确定性；Δaccuracy=0.0 在此规模下分辨不出小差。
   要 ±5pp 分辨需 ≥3 run + 更大题集（scale-up）。
3. **LLM 是 glm-5.x**：换更强模型（Claude/GPT）收敛更稳，准确度天花板与 token 节省比例可能变。
4. **baseline 是朴素 grep+读**：非"裸答"。裸答（LLM 仅凭训练知识）因 Godot 公开会被污染（design F2）。
5. **仅 cmm 一臂**：graphify 文档 KB / mempalace 记忆未含（design F4）。
6. **v1 教训**：首版收敛 prompt 弱 → 54% episode truncated → 准确度被"没收敛"污染（v1 baseline 0.462/kb 0.423
   是假象）。v2 加"查到即答、最多 2 次工具"收敛纪律后 truncation→0，真信号浮现。两臂对称改进，非偏袒 KB。

## 5. 价值定位（接 Stage 0 + value-benchmark）

| 维度 | Stage 0（检索层） | **Stage 1（agent 层）** | 证据 |
|---|---|---|---|
| context token | 压缩 12.7× | **端到端省 58%** | ●●●○ |
| 准确度 | kb_hit@5=0.846（注入） | **0.923 并列**（终答，天花板）| ●●●○ |
| 效率 | — | **2.4× token/正确答，步数 −38%** | ●●●○ |
| 概念题补救 | grep 盲 7→KB 盲 2 | KB 救回 int to string | ●●○○ |

**总判断**：KB 的价值命题被两 stage 一致坐实为 **"同等正确，更省成本"**——
检索层（Stage 0）注入更精 → agent 层（Stage 1）端到端 token −58% / 步数 −38% / 每答成本 2.4×。
准确度无差是因为 baseline grep 在本题集已触顶；KB 的差异化在概念题补救 + 经济性。
"配系统让 agent 答得更对"在本题集不成立（已触顶），"配系统让 agent 答得更省"**成立且量化**。

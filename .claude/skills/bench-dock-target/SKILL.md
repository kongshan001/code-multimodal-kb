---
name: bench-dock-target
description: Dock a target project (a codebase / doc set / memory corpus) into the engineer_demo benchmark so its retrieval quality gets measured with real numbers. Use this whenever the user wants to point the benchmark at THEIR OWN project — including phrases like "对接 X 工程到 benchmark", "dock my repo to bench", "给 X 建 benchmark target", "测我代码库的检索质量", "给 X 造测试题", "我想用 benchmark 测我的项目", or any time the user gives a code/docs path and wants bench scores. Covers creating targets/<id>/, building indexes, generating problems, running bench, and reading results. Do NOT use just to read existing reports (that's plain `bench list-reports`) or for benchmark-internal development.
---

# Dock a target project into the benchmark

This skill turns "I want benchmark numbers for MY project" into a working `targets/<id>/` that the bench can run against. The benchmark lives in the `engineer_demo` repo (or any fork of it). Everything below runs **inside that repo**.

The mental model: the bench engine (`eval/*.py`) is project-agnostic. All project-specific data — what code to search, what the gold answers are, where indexes live — lives in **one self-contained directory** `eval/targets/<id>/`. Docking = creating that directory + building its indexes + giving it problems. Nothing in the engine gets hardcoded to your project.

## Before you start

Confirm the target tools are installed (`bench web` → 环境体检, or `./setup.sh tools`). You need at least the tool for the subject you want to measure:
- **code retrieval** → `codegraph` + `codebase-memory-mcp` (cmm)
- **doc retrieval** → `graphify`
- **memory** → `mempalace`

If a tool is missing, install it via the scaffold (能力目录 → 安装) or its runbook. The harness itself is zero-extra-dependency (pytest only); never `pip install ragas` or bump `numpy≥2` (known conflicts in this repo).

## The 6-step docking workflow

Pick a kebab-case `<id>` for the target (e.g. `my-app`, `acme-docs`). Then:

### 1. Create the target directory

Create `eval/targets/<id>/target.json`. Copy the closest existing target as a template (`eval/targets/godot-core/`, `godot-docs/`, or `engineer-demo-memory/`) and edit. Shape depends on what you're measuring:

```jsonc
// code_retrieval
{
  "id": "my-app",
  "language": "Python",                 // or C++/Go/TS/...; helps future tooling
  "subjects": ["code_retrieval"],
  "code": {
    "codegraph_root": "/abs/path/to/your/repo",
    "cmm_project": "<cmm project name — see step 2>"
  },
  "notes": "what this is, one line"
}

// doc_retrieval
{
  "id": "my-docs",
  "language": "rst",                    // or md
  "subjects": ["doc_retrieval"],
  "doc": { "graph": "/abs/path/to/graphify-out/graph.json" },
  "notes": "..."
}

// cross_anchor (doc concept → code; spans two other targets)
{
  "id": "my-cross",
  "subjects": ["cross_anchor"],
  "deps": { "doc_graph": "<doc-target-id>", "cmm": "<code-target-id>" },
  "notes": "..."
}
```

**Machine-specific paths go in `target.json` as working values** (so it runs out-of-box on your machine), but other machines will differ. For those, create `eval/targets/<id>/target.local.json` (gitignored — same pattern as `scaffold/catalog.local.json`) overriding `codegraph_root` / `cmm_project` / `graph` with that machine's paths. The loader deep-merges base + local. There's a `target.local.example.json` in each existing target showing the shape.

Why this split: the repo should clone-and-run for you, but stay portable. Commit your real paths in `target.json`; everyone else overrides in their own `.local`.

### 2. Build the indexes

Run only what your `subjects` need:

| Subject | Index command | Notes |
|---|---|---|
| code_retrieval | `codegraph init <codegraph_root>` | static, zero LLM, seconds |
| code_retrieval | cmm index：`./setup-kb.py --code <codegraph_root>`（推荐，仓库封装）或直接 `codebase-memory-mcp cli index_repository`（跑 `cli index_repository --help` 看当前 flags；旧的 `cli index_repository '<json>'` raw-JSON 形式已 deprecated） | 建 cmm 知识图 |
| doc_retrieval | `graphify build <docs-dir>` | **spends LLM tokens** — estimate cost first; the resulting `graph.json` can be committed for team sharing |
| memory | `mempalace mine <session-dir> --mode convos` | ⚠ do NOT enable a non-idempotent auto-save hook alongside it (causes memory bloat — see `docs/deployment-runbook.md §D`) |

**Find the cmm project name** after indexing: `python -c "from eval.subjects import cmm_list_projects; print(cmm_list_projects())"`. cmm derives the project name from the indexed path (a munged form like `Users-name-path-to-repo`). Paste that exact string into `target.json` → `code.cmm_project`. Getting this wrong is the #1 docking failure (bench runs but returns empty results).

### 3. Create problems (the test questions + gold answers)

`eval/targets/<id>/problems.json` holds the questions. Two paths:

**Auto-generate (recommended for code):**
```bash
bench goldgen <seed words> --target <id>          # codegraph enumerates real symbols + LLM phrases NL questions
bench goldgen-verify --target <id>                 # empirical vetting: flags ambiguous gold (zero LLM)
```
> `goldgen` 需要 `anthropic` SDK + LLM 凭据（GLM 走 `~/.cc-connect/config.toml`）。没装/没凭据 → `pip install anthropic`，或走下面的手动路径（不调 LLM）。
Then review the `status: pending` candidates and approve the good ones:
```bash
bench web          # open browser → Gold lab (#/goldlab) → select target → ✓ approve good ones, 🗑 drop bad ones
```
Why this works: gold = the real symbol codegraph found, so the answer is correct by construction (no LLM judging the gold). The LLM only phrases the *question*.

**Manual (for docs / memory / curated sets):** use the Gold lab editor in `bench web` (add problems through the form — it validates the schema), or write `problems.json` directly.

Each problem must match its type's gold shape (the loader validates and rejects mismatches):

| type | text field | gold shape |
|---|---|---|
| `code_retrieval` | `query` | `{"symbols": ["FuncName", "ClassName"]}` |
| `doc_retrieval` | `query` | `{"node_labels": ["Node Label"]}` |
| `cross_anchor` | `query` | `{"doc_node_label": "...", "cmm_identifier": "...", "code_file": "path/substr"}` |
| `memory_recall` | `query` | `{"source_files": ["file.md", "session.jsonl"]}` |
| `memory_routing` | `fact` (not query!) | `{"layer": "objective\|procedural\|episodic\|subjective", "signal": "hint"}` |

Every problem needs a stable `id`. Convention: `<target-id>-<slug(first 3 words of query/fact)>` (e.g. `my-app-call-llm`). The loader/goldgen assign these automatically; if hand-writing, the `eval.targets.slugify` helper applies the same rule. Duplicate ids within a target are rejected.

Optional fields per problem: `tags` (e.g. `concept_query`, `known_weak_probe`), `provenance` (source symbol/kind/file), `notes`, `verdict`/`reason` (set by goldgen-verify).

### 4. Run the benchmark

```bash
bench run code   --target <id> --method bm25    # code retrieval (also: grep, semantic)
bench run doc    --target <id>                   # doc retrieval
bench run cross  --target <id>                   # cross-tool (needs deps targets indexed)
bench run memory --target <id>                   # memory recall + routing
```
Each run archives a structured JSON report (never overwrites) under `eval/reports/archive/` and prints the headline metric + archive id.

### 5. Read the results

```bash
bench list-reports                 # all archived runs
bench show <id>                    # full report (per-query + lockfile)
bench compare <id1> <id2>          # aggregate diff between two runs
bench web                          # browser Dashboard / Reports / Compare
```

### 6. Write the target README

Every target dir gets a beginner-friendly `README.md` (see existing 5 for the template): **这是什么 / 测什么 / 最新结果 / 数字怎么看 / 怎么自己跑 / 诚实边界**. Fill in your target's latest headline number from step 5. This is what makes the target self-explaining to a newcomer.

## Verification standard — docking succeeded when

- [ ] `python -c "from eval.targets import load; print(load('<id>')['problems'][0])"` returns a problem with no error (schema valid)
- [ ] `bench run <subject> --target <id>` completes, archives a report, and the headline metric is **non-trivial** (not all zeros — all-zero usually means `cmm_project` is wrong or the index is empty)
- [ ] `bench show <latest-id>` shows per-query rows with real retrieved results
- [ ] The target `README.md` cites the latest number

If results are all-zero: 90% of the time `cmm_project` in `target.json` doesn't match the name cmm actually indexed (`cmm_list_projects` to check), or `codegraph_root`/`graph` path is wrong.

## Common pitfalls

- **Wrong `cmm_project`** → bench runs, returns empty/zero. Always copy the exact name from `cmm_list_projects()`.
- **Machine-specific paths committed** → breaks for other devs. Put your real path in `target.json` (it's fine — that's your machine's working value), and document the override in `target.local.example.json`. Others create their own `target.local.json`.
- **graphify cost** → `graphify build` calls LLM per node. Estimate before running on a huge doc set; commit the resulting `graph.json` so the team doesn't re-pay.
- **mempalace auto-save hook** → non-idempotent hooks bloat the palace and crash recall (0.933→0.6 observed). Mine once manually, don't leave an auto-save hook running.
- **Chinese Windows** → subprocess encoding is already handled repo-wide (`eval/_subproc.run_text` forces UTF-8). You don't need to do anything; if you hit a decode error, it's a missed call site — route it through `run_text`.
- **memory benchmark is self-referential** → `engineer-demo-memory` measures engineer_demo's *own* memory. It's a demo, not portable. Docking someone else's memory needs their own mempalace corpus + fresh problems.

## Commit the work

Per repo discipline: commit `targets/<id>/` (target.json + problems.json + README.md) to main + push, with `Co-Authored-By: Claude <noreply@anthropic.com>`. Never commit `target.local.json` (it's gitignored — machine-specific).

## Quick command reference

```bash
alias bench='python -m eval.cli'
bench goldgen <seeds> --target <id>          # auto-generate code problems
bench goldgen-verify --target <id>           # vet pending candidates
bench run code --target <id> --method bm25   # run + auto-archive
bench list-reports / show <id> / compare <a> <b>
bench web                                    # Gold lab editor + Dashboard
```

// ═══ Measurement Lab · "Laboratory Ledger" SPA ═══
// vanilla JS，hash 路由，读 /api/* 真实数据。设计见 DESIGN.md。
const $ = (s, p = document) => p.querySelector(s);
const fetchJSON = async u => (await fetch(u)).json();
const fmt = n => typeof n === "number" ? (n !== 0 && Math.abs(n) < 1 ? n.toFixed(3) : n) : (n ?? "—");

// ── helpers ──
function latest(rs, sub) { const f = rs.filter(r => (r.subject||"").includes(sub) || (r.variant||"").includes(sub)); return f[f.length - 1]; }
function headline(r) {
  if (!r || !r.aggregate) return "—";
  for (const k of ["mean_broad_recall@5","mean_hit@5","mean_compression_read","mean_faithfulness","routing_overall_accuracy","crosstool_success_rate"])
    if (k in r.aggregate) return r.aggregate[k];
  return "—";
}
function bar(val, max, isBest) {
  if (!max || typeof val !== "number") return "";
  const w = Math.max(2, Math.min(100, (val / max) * 100));
  return `<span class="bar ${isBest?'acc':''}" style="width:${w}px"></span>`;
}

// ── topbar + page wrapper ──
const NAV = [["dashboard","Dashboard"],["compare","Compare"],["run","Run"],["goldlab","Gold lab"],["setup","Setup"],["reports","归档"],["catalog","能力目录"]];
function render(active, html) {
  $("#app").innerHTML = `<div class="topbar">
    <div class="brand">measurement <em>lab</em></div><span class="tag">engineer_demo · bench</span>
    <nav>${NAV.map(([r,l])=>`<a href="#/${r}" class="${r===active?'active':''}">${l}</a>`).join("")}</nav>
  </div><div class="main">${html}</div>`;
  $("#app").scrollIntoView();
}

// ═══════════════════════════════════════════════════
// DASHBOARD — 指标条 + agent-compare 矩阵表 + 归档
// ═══════════════════════════════════════════════════
async function dashboard() {
  const [rep, ac] = await Promise.all([fetchJSON("/api/reports"), fetchJSON("/api/agent-compare")]);
  const reports = rep.reports || [];
  const code = latest(reports, "cmm.bm25") || latest(reports, "cmm.");
  const mem = latest(reports, "mempalace");
  const ab = latest(reports, "ab-value");
  const doc = latest(reports, "doc-quality");

  // agent-compare 最新 run
  const acRuns = (ac.runs || []).filter(r => !r.smoke);
  const lac = acRuns[acRuns.length - 1];
  let acHTML = "";
  if (lac && lac.matrix) {
    const arms = Object.keys(lac.matrix);
    const metrics = [
      ["accuracy","准确率", true],
      ["mean_total_tokens","tokens", false],
      ["no_tool_rate","no_tool", false],
      ["truncated_rate","truncated", false],
      ["mean_llm_calls","llm_calls", false],
    ];
    // 找 accuracy 最高的臂
    const bestArm = arms.reduce((b, a) => (lac.matrix[a]?.accuracy ?? 0) > (lac.matrix[b]?.accuracy ?? 0) ? a : b, arms[0]);
    acHTML = `
      <div class="sec-h"><span class="n">01</span><h2>agent-compare · 最新</h2><span class="line"></span></div>
      <p class="note-sm" style="margin:-8px 0 12px">${lac.model||'?'} · engine=${lac.engine||'sdk'} · ${lac.n_questions||'?'} 题 · <span class="mono">${lac.run_id||''}</span></p>
      <table class="matrix">
        <tr><th>metric</th>${arms.map(a=>`<th class="${a===bestArm?'best':''}">${a}</th>`).join("")}</tr>
        ${metrics.map(([k,label,lowerBetter]) => {
          const vals = arms.map(a => lac.matrix[a]?.[k]);
          const max = Math.max(...vals.filter(v => typeof v === "number"), 0.001);
          const min = Math.min(...vals.filter(v => typeof v === "number"), 0);
          const best = lowerBetter ? min : max;
          return `<tr><td>${label}</td>${arms.map((a,i) => {
            const v = vals[i]; const isBest = v === best && typeof v === "number";
            return `<td class="${isBest?'best':''}">${fmt(v)}${bar(v, max, isBest)}</td>`;
          }).join("")}</tr>`;
        }).join("")}
      </table>`;
  }

  render("dashboard", `
    <h1>dashboard</h1>
    <p class="lede">知识库 / 记忆系统的体检台 — 不评感觉，评数字。</p>
    <div class="strip">
      <div class="cell"><div class="lbl">代码检索 broad@5</div><div class="val">${fmt(headline(code))}</div><div class="ctx">${code?code.subject:"—"}</div></div>
      <div class="cell"><div class="lbl">记忆召回 hit@5</div><div class="val">${fmt(mem?headline(mem):"—")}</div><div class="ctx">${mem?mem.subject:"—"}</div></div>
      <div class="cell"><div class="lbl">A/B 压缩比</div><div class="val acc">${ab?headline(ab)+"×":"—"}</div><div class="ctx">${ab?ab.subject:"—"}</div></div>
      <div class="cell"><div class="lbl">答案 faithfulness</div><div class="val">${fmt(headline(doc))}<span class="badge">LLM</span></div><div class="ctx">${doc?doc.subject:"—"}</div></div>
    </div>
    ${acHTML}
    <div class="sec-h"><span class="n">${lac?'02':'01'}</span><h2>归档 · 最近跑过</h2><span class="line"></span></div>
    <table class="tbl"><tr><th>time</th><th>subject</th><th>variant</th><th>headline</th><th></th></tr>
    ${reports.slice().reverse().slice(0,8).map(r=>`<tr onclick="location.hash='#/report/${r.id}'">
      <td>${(r.readable_ts||r.ts||"").slice(5,16)}</td><td class="sb">${r.subject}</td><td>${r.variant}</td><td>${headline(r)}</td><td>▸</td></tr>`).join("")}
    </table>`);
}

// ═══════════════════════════════════════════════════
// COMPARE — 两个 agent-compare run 矩阵 diff
// ═══════════════════════════════════════════════════
async function compare() {
  const ac = await fetchJSON("/api/agent-compare");
  const runs = (ac.runs || []).filter(r => !r.smoke);
  const opts = runs.map(r => `<option value="${r.run_id}">${r.run_id.slice(0,24)} ${r.model||''} ${r.n_questions||'?'}题</option>`);
  render("compare", `
    <h1>compare <em>· 矩阵 diff</em></h1>
    <p class="lede">选两个 agent-compare run，看 4 臂指标 diff。</p>
    <div style="display:flex;gap:8px;align-items:center;margin-bottom:20px;flex-wrap:wrap">
      <select id="cmpA">${opts}</select>
      <span class="note-sm">vs</span>
      <select id="cmpB">${opts.slice(1)}</select>
      <button class="btn fill" onclick="doCmp()">对比 ▸</button>
    </div>
    <div id="cmpOut"><p class="note-sm">选两个 run 点"对比"。</p></div>`);

  window.doCmp = async () => {
    const [aId, bId] = [$("#cmpA").value, $("#cmpB").value];
    const a = runs.find(r => r.run_id === aId);
    const b = runs.find(r => r.run_id === bId);
    if (!a || !b) return;
    const arms = [...new Set([...Object.keys(a.matrix||{}), ...Object.keys(b.matrix||{})])];
    const keys = ["accuracy","mean_total_tokens","no_tool_rate","truncated_rate","mean_llm_calls","mean_tool_steps"];
    $("#cmpOut").innerHTML = `
      <table class="matrix">
        <tr><th>metric</th>${arms.map(ar=>`<th>${ar}</th>`).join("")}</tr>
        ${keys.map(k => `<tr><td>${k}</td>${arms.map(ar => {
          const x = a.matrix?.[ar]?.[k], y = b.matrix?.[ar]?.[k];
          const d = (typeof x==="number" && typeof y==="number") ? y - x : null;
          const dn = parseFloat(d?.toFixed(3));
          const cls = d===null ? 'delta-zero' : dn>0?'delta-pos' : dn<0?'delta-neg':'delta-zero';
          const sign = dn>0?'+':'';
          return `<td>${fmt(x)} → ${fmt(y)} <span class="${cls}">${d===null?'—':sign+dn}</span></td>`;
        }).join("")}</tr>`).join("")}
      </table>
      <p class="note-sm" style="margin-top:12px">左: ${a.model} ${a.engine} · 右: ${b.model} ${b.engine}</p>`;
  };
}

// ═══════════════════════════════════════════════════
// RUN CONSOLE — 从浏览器触发 bench
// ═══════════════════════════════════════════════════
function runConsole() {
  render("run", `
    <h1>run console <em>· 触发评测</em></h1>
    <p class="lede">从浏览器跑 bench（后端 subprocess 调 eval.cli）。</p>
    <div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin-bottom:16px">
      <select id="rcSubj" onchange="rcUpd()">
        <option value="agent-compare">agent-compare（4 臂）</option>
        <option value="code">code（代码检索）</option>
        <option value="memory">memory（记忆召回）</option>
        <option value="ab">ab（Stage0 token 代理）</option>
      </select>
      <span id="rcOpts"></span>
      <button class="btn fill" onclick="doRun()">跑 ▸</button>
    </div>
    <div id="rcOut" class="out-box">选参数点"跑"——结果这里出。</div>`);
  window.rcUpd = () => {
    const s = $("#rcSubj").value;
    const tgt = {code:"godot-core",memory:"engineer-demo-memory",ab:"godot-core","agent-compare":"godot-core"};
    const showTgt = s !== "agent-compare";
    $("#rcOpts").innerHTML = showTgt
      ? `<input id="rcTarget" value="${tgt[s]||'godot-core'}" style="width:140px"/>
         ${s==='code'?'<select id="rcMethod"><option>bm25</option><option>grep</option><option>semantic</option></select>':''}`
      : `<span class="note-sm">37 题 × 4 臂（~15-25 min）</span>`;
  };
  window.doRun = async () => {
    const s = $("#rcSubj").value;
    $("#rcOut").textContent = "running…（可能要几分钟）";
    try {
      const body = {subject: s};
      if (s !== "agent-compare") body.target = $("#rcTarget")?.value || "godot-core";
      if (s === "code") body.method = $("#rcMethod")?.value || "bm25";
      const r = await fetch("/api/run", {method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(body)});
      const o = await r.json();
      $("#rcOut").innerHTML = `<b style="color:${o.rc===0?'var(--good)':'var(--bad)'}">exit ${o.rc}</b>\n\n${(o.stdout||"").slice(-2000)}${o.stderr?"\n\n"+o.stderr.slice(-400):""}`;
    } catch(e) { $("#rcOut").textContent = "error: " + e; }
  };
  rcUpd();
}

// ═══════════════════════════════════════════════════
// REPORTS — 归档列表 + 详情
// ═══════════════════════════════════════════════════
async function reports() {
  const { reports } = await fetchJSON("/api/reports");
  render("reports", `
    <h1>归档 <em>· reports</em></h1>
    <p class="lede">${reports.length} 份历史评测。</p>
    <table class="tbl"><tr><th>id</th><th>subject</th><th>variant</th><th>ts</th><th>headline</th></tr>
    ${reports.slice().reverse().map(r=>`<tr onclick="location.hash='#/report/${r.id}'">
      <td>${r.id.slice(0,24)}…</td><td class="sb">${r.subject}</td><td>${r.variant}</td>
      <td>${(r.readable_ts||r.ts||"").slice(5,16)}</td><td>${headline(r)}</td></tr>`).join("")}
    </table>`);
}
async function reportDetail(id) {
  const r = await fetchJSON("/api/report/" + id);
  const agg = r.aggregate || {}, pq = r.per_query || [];
  render("", `
    <h1>${r.subject} <em>· detail</em></h1>
    <p class="lede">${r.variant} · n=${r.n||pq.length} · ${r.target||""}</p>
    <div class="sec-h"><span class="n">A</span><h2>aggregate</h2><span class="line"></span></div>
    <div class="kv">${Object.entries(agg).map(([k,v])=>`<span>${k}</span> = <b>${fmt(v)}</b><br>`).join("")}</div>
    <div class="sec-h"><span class="n">B</span><h2>per_query (${pq.length})</h2><span class="line"></span></div>
    <table class="tbl"><tr><th>query</th><th>headline</th></tr>
    ${pq.slice(0,30).map(q=>`<tr><td>${(q.query||"").slice(0,50)}</td><td>${headline({aggregate:q})}</td></tr>`).join("")}
    </table>`);
}

// ═══════════════════════════════════════════════════
// SETUP — 环境体检
// ═══════════════════════════════════════════════════
async function setup() {
  const h = await fetchJSON("/api/health");
  const d = h.deps || {};
  const row = (n,k,desc) => `<tr><td class="sb">${n}</td><td style="color:${d[k]?'var(--good)':'var(--bad)'}">${d[k]?"✓ "+d[k]:"✗ 缺"}</td><td class="note-sm">${desc}</td></tr>`;
  render("setup", `
    <h1>setup <em>· 环境体检</em></h1>
    <p class="lede">${h.ready?"环境就绪，可进评测。":"有缺项——装齐再 bench。"}</p>
    <div class="gate ${h.ready?'ok':''}"><span class="dot"></span><b>${h.ready?"环境就绪 ✓":"有缺项"}</b> <button class="btn" style="margin-left:auto" onclick="location.reload()">刷新</button></div>
    <div class="sec-h"><span class="n">A</span><h2>KB 工具</h2><span class="line"></span></div>
    <table class="tbl">${row("cmm","cmm","代码符号 KB")}${row("graphify","graphify","文档图 KB")}${row("codegraph","codegraph","第二代码 KB")}${row("mempalace","mempalace","记忆层")}</table>
    <div class="sec-h"><span class="n">B</span><h2>Python / 凭据</h2><span class="line"></span></div>
    <table class="tbl">${row("python","python","pytest + anthropic")}${row("render","render","SVG→PNG")}${row("LLM 凭据","creds","agent + judge 用")}</table>`);
}

// ═══════════════════════════════════════════════════
// GOLD LAB — 题目编辑器（精简版）
// ═══════════════════════════════════════════════════
async function goldlab() {
  let targets = [];
  try { targets = (await fetchJSON("/api/targets")).targets; } catch {}
  const tid = targets[0]?.id || "godot-core";
  render("goldlab", `<h1>gold lab <em>· 题库</em></h1><p class="lede">选择 target 浏览/编辑 gold problems。</p>
    <div style="margin-bottom:16px"><select id="glTgt" onchange="glLoad()">${targets.map(t=>`<option value="${t.id}">${t.id} (${t.language||'?'})</option>`).join("")}</select></div>
    <div id="glBody"><div class="loading">loading…</div></div>`);
  window.glLoad = async () => {
    const t = $("#glTgt")?.value || tid;
    $("#glBody").innerHTML = `<div class="loading">loading ${t}…</div>`;
    try {
      const d = await fetchJSON("/api/gold/" + encodeURIComponent(t));
      const ps = d.problems || [];
      const goldStr = p => {
        const g = p.gold||{};
        return g.symbols?.join(", ")||g.files?.join(", ")||g.node_labels?.join(", ")||g.layer||"";
      };
      $("#glBody").innerHTML = `
        <p class="note-sm" style="margin-bottom:12px">${ps.length} 题 · types: ${ [...new Set(ps.map(p=>p.type))].join(", ") }</p>
        <table class="tbl"><tr><th>id</th><th>type</th><th>status</th><th>query</th><th>gold</th></tr>
        ${ps.map(p=>`<tr><td class="mono" style="font-size:9px">${(p.id||'').slice(0,20)}</td><td>${p.type||''}</td>
          <td style="color:${p.status==='accepted'?'var(--good)':'var(--warn)'}">${p.status||''}</td>
          <td>${(p.query||p.fact||'').slice(0,40)}</td><td>${goldStr(p).slice(0,30)}</td></tr>`).join("")}
        </table>`;
    } catch(e) { $("#glBody").innerHTML = `<p class="note-sm" style="color:var(--bad)">加载失败: ${e}</p>`; }
  };
  glLoad();
}

// ═══════════════════════════════════════════════════
// CATALOG — 能力目录（精简版）
// ═══════════════════════════════════════════════════
async function catalog() {
  render("catalog", `
    <h1>能力目录 <em>· scaffold</em></h1>
    <p class="lede">检测目标工程 → 浏览/安装策展能力。</p>
    <div class="gate"><span class="dot" style="background:var(--teal)"></span>
      <input id="catPath" value="/Users/ks_128/Documents/godot-src/core" style="flex:1"/>
      <button class="btn fill" onclick="catLoad()">检测 ▸</button></div>
    <div id="catBody"><p class="note-sm">点"检测"扫描目标工程。</p></div>`);
  window.catLoad = async () => {
    const path = $("#catPath").value;
    $("#catBody").innerHTML = `<div class="loading">检测 ${path}…</div>`;
    try {
      const d = await fetchJSON(`/api/catalog?project=${encodeURIComponent(path)}`);
      const cats = (d.categories||[]).filter(c => c.id !== "engineering-practices");
      const total = cats.reduce((s,c)=>s+c.capabilities.length,0);
      const inst = cats.reduce((s,c)=>s+c.capabilities.filter(x=>x.installed).length,0);
      $("#catBody").innerHTML = `
        <p class="note-sm" style="margin:12px 0">${d.detection?.language||'?'} · ${inst}/${total} 能力可用</p>
        <div class="ctabs">${cats.map((c,i)=>`<div class="ctab ${i===0?'active':''}" onclick="catTab(${i})">${c.name}</div>`).join("")}</div>
        <div id="catList"></div>`;
      window._cats = cats;
      catTab(0);
    } catch(e) { $("#catBody").innerHTML = `<p style="color:var(--bad)">检测失败: ${e}</p>`; }
  };
  window.catTab = i => {
    document.querySelectorAll(".ctab").forEach((t,j)=>t.classList.toggle("active",j===i));
    const c = window._cats?.[i]; if(!c) return;
    $("#catList").innerHTML = `<table class="tbl">${c.capabilities.map(cap=>`<tr>
      <td><b>${cap.name}</b> <span class="note-sm">${cap.type||''}</span><br><span class="note-sm">${cap.desc||''}</span></td>
      <td style="text-align:right">${cap.installed?'<span style="color:var(--good)">✓ 已装</span>':cap.installable?'<span class="note-sm">可装</span>':'<span class="note-sm">—</span>'}</td>
    </tr>`).join("")}</table>`;
  };
}

// ── router ──
const routes = { dashboard, compare, run:runConsole, reports, setup, goldlab, catalog,
  report: id => reportDetail(id) };
async function router() {
  const h = location.hash.slice(2) || "dashboard";
  const parts = h.split("/");
  const route = parts[0];
  const arg = parts.slice(1).join("/");
  try {
    if (route === "report" && arg) await reportDetail(arg);
    else if (routes[route]) await routes[route]();
    else render("", `<h1>404</h1><p class="lede">"${h}" not found.</p>`);
  } catch(e) { render("", `<h1>error</h1><p class="lede">${e}</p>`); }
}
window.addEventListener("hashchange", router);
router();

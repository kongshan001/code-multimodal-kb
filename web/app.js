// ═══ Measurement Lab · Benchmark Explorer（4 层下钻）═══
const $ = (s, p = document) => p.querySelector(s);
const fetchJSON = async u => (await fetch(u)).json();
const fmt = n => typeof n === "number" ? (n !== 0 && Math.abs(n) < 1 ? n.toFixed(3) : n > 999 ? Math.round(n).toLocaleString() : n) : (n ?? "—");
const esc = s => String(s ?? "").replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");
const ARMS = ["no-kb","kb","kb+superpowers","kb+openspec"];

function bar(val, max, isBest) {
  if (!max || typeof val !== "number" || val === 0) return "";
  const w = Math.max(2, Math.min(70, (Math.abs(val) / Math.abs(max)) * 70));
  return `<span class="bar ${isBest?'acc':''}" style="width:${w}px"></span>`;
}

function render(html) {
  $("#app").innerHTML = `<div class="topbar">
    <div class="brand">measurement <em>lab</em></div><span class="tag">benchmark explorer</span>
    <nav><a href="#/targets">Targets</a><a href="#/compare">Compare</a></nav>
  </div><div class="main">${html}</div>`;
}

// breadcrumb helper
function crumb(...parts) {
  return `<div class="crumb">${parts.map((p,i) => {
    const last = i === parts.length - 1;
    return last ? `<span>${p[0]}</span>` : `<a href="${p[1]}">${p[0]}</a> <span class="sep">/</span>`;
  }).join(" ")}</div>`;
}

// ═══════════════════════════════════════════════════
// Level 1: TARGETS — 工程列表
// ═══════════════════════════════════════════════════
async function targets() {
  render(`<h1>targets <em>· benchmark 工程</em></h1><p class="lede">选择被测工程查看题目设计与历史报告。</p><div class="loading">loading…</div>`);
  const [tg, ac] = await Promise.all([fetchJSON("/api/targets"), fetchJSON("/api/agent-compare")]);
  const runs = (ac.runs || []).filter(r => !r.smoke);
  // 按 target 分组，取最新 run
  const latestByTarget = {};
  for (const r of runs) { const t = r.target; if (!latestByTarget[t] || r.run_id > latestByTarget[t].run_id) latestByTarget[t] = r; }

  const cards = (tg.targets || []).map(t => {
    const lr = latestByTarget[t.id];
    const bestAcc = lr ? Math.max(...(Object.values(lr.matrix || {})).map(m => m?.accuracy ?? 0)) : null;
    return `<a href="#/target/${t.id}" class="tgt-card">
      <div class="tgt-name">${t.id}</div>
      <div class="tgt-lang">${t.language || "—"} · ${(t.subjects || []).join(", ") || ""}</div>
      ${lr ? `<div class="tgt-run"><span class="mono">${lr.model}</span> · acc <b>${bestAcc?.toFixed(3)}</b> · ${lr.n_questions}题</div>
              <div class="tgt-date mono">${lr.run_id.slice(0,16)}</div>`
           : `<div class="tgt-run note-sm">暂无 agent-compare 报告</div>`}
    </a>`;
  }).join("");

  $("#app .main").innerHTML = `<h1>targets <em>· benchmark 工程</em></h1>
    <p class="lede">${tg.targets?.length || 0} 个被测工程。点击进入查看题目设计与历史报告。</p>
    <div class="tgt-grid">${cards}</div>`;
}

// ═══════════════════════════════════════════════════
// Level 2: TARGET DETAIL — 题目 + 历史 Run + 配置
// ═══════════════════════════════════════════════════
async function targetDetail(tid) {
  render(crumb(["targets","#/targets"], [tid,`#/target/${tid}`]) +
    `<h1>${tid}</h1><div class="loading">loading…</div>`);
  const [gd, ac] = await Promise.all([fetchJSON("/api/gold/" + tid), fetchJSON("/api/agent-compare")]);
  const t = gd.target || {};
  const problems = gd.problems || [];
  const runs = (ac.runs || []).filter(r => !r.smoke && r.target === tid).reverse();
  const goldStr = p => { const g = p.gold||{}; return g.symbols?.join(", ")||g.files?.join(", ")||g.node_labels?.join(", ")||g.layer||""; };

  const tabs = `
    <div class="tabs">
      <div class="tab active" onclick="tgtTab('problems')">题目设计 (${problems.length})</div>
      <div class="tab" onclick="tgtTab('runs')">历史 Run (${runs.length})</div>
      <div class="tab" onclick="tgtTab('config')">配置</div>
    </div>`;

  const problemsHTML = `<div id="tab-problems" class="tab-panel">
    <table class="tbl"><tr><th>id</th><th>type</th><th>status</th><th>query / fact</th><th>gold</th></tr>
    ${problems.map(p=>`<tr><td class="mono" style="font-size:9px">${(p.id||'').slice(0,24)}</td>
      <td style="font-size:9px;color:var(--ink3)">${p.type||''}</td>
      <td style="color:${p.status==='accepted'?'var(--good)':'var(--warn)'};font-size:9px">${p.status||''}</td>
      <td style="font-size:10px">${esc((p.query||p.fact||'').slice(0,50))}${(p.query||'').length>50?'…':''}</td>
      <td style="font-size:10px">${esc(goldStr(p).slice(0,30))}</td></tr>`).join("")}
    </table></div>`;

  const runsHTML = `<div id="tab-runs" class="tab-panel" style="display:none">
    ${runs.length ? `<table class="tbl"><tr><th>run</th><th>model</th><th>engine</th><th>题数</th><th>最高 acc</th><th></th></tr>
    ${runs.map(r => {
      const best = Math.max(...Object.values(r.matrix||{}).map(m=>m?.accuracy||0), 0);
      return `<tr onclick="location.hash='#/run/${r.run_id}'">
        <td class="mono" style="font-size:9px">${r.run_id.slice(0,20)}…</td>
        <td>${r.model||'?'}</td><td>${r.engine||'sdk'}</td><td>${r.n_questions||'?'}</td>
        <td style="color:var(--accent);font-weight:600">${best.toFixed(3)}</td><td>▸</td></tr>`;
    }).join("")}</table>` : `<p class="note-sm">该工程暂无 agent-compare 报告。</p>`}</div>`;

  const configHTML = `<div id="tab-config" class="tab-panel" style="display:none">
    <div class="kv">
      <span>language</span> = <b>${t.language || '—'}</b><br>
      <span>subjects</span> = <b>${(t.subjects||[]).join(', ') || '—'}</b><br>
      <span>notes</span> = <b>${esc(t.notes || '—')}</b><br>
      ${t.code ? `<span>codegraph_root</span> = <b>${esc(t.code.codegraph_root || '—')}</b><br>
                  <span>cmm_project</span> = <b>${esc(t.code.cmm_project || '—')}</b>` : ''}
      ${t.doc ? `<span>doc_graph</span> = <b>${esc(t.doc.graph || '—')}</b>` : ''}
      ${t.memory ? `<span>palace</span> = <b>${esc(t.memory.palace || '—')}</b>` : ''}
    </div></div>`;

  $("#app .main").innerHTML = `${crumb(["targets","#/targets"], [tid,`#/target/${tid}`])}
    <h1>${tid} <em>· ${t.language || ''}</em></h1>
    <p class="lede">${(t.subjects||[]).join(' / ')||''} ${t.notes ? '· '+esc(t.notes.slice(0,60)) : ''}</p>
    ${tabs}${problemsHTML}${runsHTML}${configHTML}`;
}

window.tgtTab = name => {
  document.querySelectorAll(".tab-panel").forEach(p => p.style.display = "none");
  document.querySelectorAll(".tab").forEach(t => t.classList.remove("active"));
  $(`#tab-${name}`).style.display = "";
  [...document.querySelectorAll(".tab")].find(t => t.textContent.includes(name === "problems" ? "题目" : name === "runs" ? "Run" : "配置"))?.classList.add("active");
};

// ═══════════════════════════════════════════════════
// Level 3: RUN DETAIL — 矩阵 + 逐题
// ═══════════════════════════════════════════════════
async function runDetail(runId) {
  render(crumb(["targets","#/targets"], ["run",""], [runId.slice(0,20)+"…"]) + `<h1>run detail</h1><div class="loading">loading…</div>`);
  const [summary, qData] = await Promise.all([
    fetchJSON(`/api/agent-compare/${runId}`),
    fetchJSON(`/api/agent-compare/${runId}/questions`),
  ]);
  const m = summary.matrix || {};
  const arms = summary.arms || ARMS;
  const bestArm = arms.reduce((b,a) => (m[a]?.accuracy ?? 0) > (m[b]?.accuracy ?? 0) ? a : b, arms[0]);
  const metrics = [["accuracy","准确率",true],["mean_total_tokens","tokens",false],["no_tool_rate","no_tool",false],
    ["truncated_rate","trunc",false],["mean_llm_calls","calls",false],["mean_tool_steps","tools",false],["mean_cost_$","cost $",false]];

  const matrixHTML = `<table class="matrix">
    <tr><th>metric</th>${arms.map(a=>`<th class="${a===bestArm?'best':''}">${a}</th>`).join("")}</tr>
    ${metrics.map(([k,label,lower]) => {
      const vals = arms.map(a => m[a]?.[k]); const nums = vals.filter(v => typeof v === "number");
      const best = lower ? Math.min(...nums, Infinity) : Math.max(...nums, -Infinity);
      return `<tr><td>${label}</td>${arms.map((a,i) => {
        const v = vals[i]; const isBest = v === best && typeof v === "number";
        return `<td class="${isBest?'best':''}">${fmt(v)}${bar(v, Math.max(...nums.map(Math.abs)), isBest)}</td>`;
      }).join("")}</tr>`;
    }).join("")}</table>`;

  const qs = qData.questions || {}; const qids = Object.keys(qs).sort();
  const qHTML = `<table class="tbl" id="qTable">
    <tr><th>qid</th><th>type</th><th>query</th>${arms.map(a=>`<th class="arm-h">${a.replace('kb+','').replace('kb','kb')}</th>`).join("")}<th></th></tr>
    ${qids.map(qid => {
      const q = qs[qid];
      const cells = arms.map(a => {
        const ep = q[a]; if (!ep) return '<td class="cell-na">—</td>';
        const c = ep.correct ? 'var(--good)' : 'var(--bad)'; const sym = ep.correct ? '✓' : '✗';
        const trunc = ep.truncated ? '<span style="color:var(--warn);font-size:7px">⚠</span>' : '';
        return `<td class="cell-ok" style="color:${c}" onclick="location.hash='#/run/${runId}/${qid}/${encodeURIComponent(a)}'">${sym}${trunc}</td>`;
      }).join("");
      const diverge = arms.some(a => q[a] && arms.some(b => q[b] && q[a]?.correct !== q[b]?.correct));
      return `<tr class="${diverge?'row-diverge':''}">
        <td class="mono" style="font-size:9px">${qid}</td><td style="font-size:9px;color:var(--ink3)">${q.type||''}</td>
        <td style="font-size:10px">${esc((q.query||'').slice(0,42))}${(q.query||'').length>42?'…':''}</td>
        ${cells}<td class="note-sm">▸</td></tr>`;
    }).join("")}</table>
    <p class="note-sm" style="margin-top:8px">✓=答对 ✗=答错 ⚠=截断 · 橙底=臂间分化 · 点 ✓/✗ 看完整回答</p>`;

  $("#app .main").innerHTML = `${crumb(["targets","#/targets"], ["run",""], [runId.slice(0,16)+"…"])}
    <h1>${summary.model || '?'} <em>· ${summary.engine || 'sdk'} · ${summary.n_questions || '?'}题</em></h1>
    <p class="lede mono" style="font-size:11px">${runId}</p>
    <div class="sec-h"><span class="n">A</span><h2>矩阵</h2><span class="line"></span></div>${matrixHTML}
    <div class="sec-h"><span class="n">B</span><h2>逐题 (${qids.length})</h2><span class="line"></span></div>${qHTML}`;
}

// ═══════════════════════════════════════════════════
// Level 4: EPISODE DETAIL — 完整回答 + 工具链 + session + thinking
// ═══════════════════════════════════════════════════
async function episodeDetail(runId, qid, arm) {
  arm = decodeURIComponent(arm);
  render(crumb(["targets","#/targets"], ["run",`#/run/${runId}`], [qid,`#/run/${runId}`], [arm]) +
    `<h1>episode</h1><div class="loading">loading…</div>`);

  // 拿逐题数据 + session + thinking（并行）
  const armEnc = encodeURIComponent(arm);
  const [qData, sess, think] = await Promise.all([
    fetchJSON(`/api/agent-compare/${runId}/questions`),
    fetchJSON(`/api/agent-compare/${runId}/arms/${armEnc}/episodes/${qid}/session`).catch(() => ({session:[]})),
    fetchJSON(`/api/agent-compare/${runId}/arms/${armEnc}/episodes/${qid}/thinking`).catch(() => ({thinking:""})),
  ]);
  const q = (qData.questions || {})[qid] || {};
  const ep = q[arm] || {};
  const session = sess.session || [];
  const thinking = think.thinking || "";

  // session 逐轮渲染
  const renderContent = (content) => {
    if (typeof content === "string") return `<div class="turn-text">${esc(content)}</div>`;
    if (!Array.isArray(content)) return "";
    return content.map(b => {
      if (typeof b === "string") return `<div class="turn-text">${esc(b)}</div>`;
      const t = b.type || b.role || "";
      if (t === "text") return `<div class="turn-text">${esc(b.text || '')}</div>`;
      if (t === "tool_use") return `<div class="turn-tool">🔧 <b>${b.name||'?'}</b>(${esc(JSON.stringify(b.input||{}))})</div>`;
      if (t === "tool_result") return `<div class="turn-result">↳ ${esc((b.content||'').slice(0,300))}${(b.content||'').length>300?'…':''}</div>`;
      if (t === "thinking") return `<div class="turn-think">💭 ${esc((b.text||'').slice(0,200))}…</div>`;
      return `<div class="turn-text">${esc(JSON.stringify(b).slice(0,200))}</div>`;
    }).join("");
  };
  const sessionHTML = session.length ? session.map(m => {
    const role = m.role || "?";
    const cls = role === "assistant" ? "turn-asst" : role === "user" ? "turn-user" : "turn-other";
    return `<div class="turn ${cls}"><div class="turn-role">${role}</div><div class="turn-body">${renderContent(m.content)}</div></div>`;
  }).join("") : `<p class="note-sm">无 session 记录。</p>`;

  $("#app .main").innerHTML = `${crumb(["targets","#/targets"], ["run",`#/run/${runId}`], [qid,`#/run/${runId}`], [arm])}
    <h1>${qid} <em>· ${arm}</em></h1>
    <p class="lede">${esc(q.query || '')}</p>

    <div class="ep-hero">
      <div class="ep-result ${ep.correct ? 'ep-ok' : 'ep-fail'}">${ep.correct ? '✓ 正确' : '✗ 错误'}</div>
      <div class="ep-ans"><span class="note-sm">答案</span><br>${esc(ep.answer || '(空)')}</div>
      <div class="ep-meta">
        <span><b>${ep.llm_calls||0}</b> calls</span>
        <span><b>${ep.total_tokens||0}</b> tokens</span>
        <span><b>${ep.tool_steps||0}</b> tools</span>
        ${ep.truncated ? '<span class="badge" style="color:var(--warn);border-color:var(--warn)">⚠ 截断</span>' : ''}
      </div>
    </div>
    <div class="ep-gold"><span class="note-sm">gold</span> ${esc((q.gold||[]).join(', '))}</div>

    <div class="sec-h"><span class="n">A</span><h2>工具调用链</h2><span class="line"></span></div>
    <div class="tool-chain">${(ep.tool_calls||[]).length ? (ep.tool_calls||[]).map((t,i) =>
      `<span class="tool-node">${t}</span>${i < (ep.tool_calls||[]).length-1 ? '<span class="tool-arrow">→</span>' : ''}`
    ).join("") : '<span class="note-sm">未调用工具</span>'}</div>

    ${thinking ? `<div class="sec-h"><span class="n">B</span><h2>思考过程</h2><span class="line"></span></div>
    <div class="think-box">${esc(thinking)}</div>` : ''}

    <div class="sec-h"><span class="n">${thinking?'C':'B'}</span><h2>对话过程 (${session.length} 轮)</h2><span class="line"></span></div>
    <div class="session">${sessionHTML}</div>`;
}

// ═══════════════════════════════════════════════════
// COMPARE — 两个 run 矩阵 diff
// ═══════════════════════════════════════════════════
async function compare() {
  const ac = await fetchJSON("/api/agent-compare");
  const runs = (ac.runs || []).filter(r => !r.smoke);
  const opts = runs.slice().reverse().map(r => `<option value="${r.run_id}">${r.run_id.slice(0,20)}… ${r.model||''} ${r.n_questions||'?'}题</option>`).join("");
  render(`<h1>compare <em>· 矩阵 diff</em></h1>
    <p class="lede">选两个 run 看指标 diff。</p>
    <div style="display:flex;gap:8px;align-items:center;margin-bottom:20px;flex-wrap:wrap">
      <select id="cmpA">${opts}</select><span class="note-sm">vs</span>
      <select id="cmpB">${opts}</select>
      <button class="btn fill" onclick="doCmp()">对比 ▸</button>
    </div>
    <div id="cmpOut"><p class="note-sm">选两个 run 点"对比"。</p></div>`);
  window.doCmp = async () => {
    const [aId, bId] = [$("#cmpA").value, $("#cmpB").value];
    const [a, b] = await Promise.all([fetchJSON(`/api/agent-compare/${aId}`), fetchJSON(`/api/agent-compare/${bId}`)]);
    const arms = [...new Set([...(a.arms||[]),...(b.arms||[])])];
    const keys = [["accuracy","acc",true],["mean_total_tokens","tokens",false],["no_tool_rate","no_tool",false],
                  ["truncated_rate","trunc",false],["mean_llm_calls","calls",false],["mean_cost_$","cost",false]];
    $("#cmpOut").innerHTML = `<table class="matrix">
      <tr><th>metric</th>${arms.map(ar=>`<th>${ar}<br><span class="note-sm" style="font-weight:400">${a.model||''} → ${b.model||''}</span></th>`).join("")}</tr>
      ${keys.map(([k,label]) => `<tr><td>${label}</td>${arms.map(ar => {
        const x = a.matrix?.[ar]?.[k], y = b.matrix?.[ar]?.[k];
        const d = (typeof x==="number" && typeof y==="number") ? y - x : null;
        const dn = d !== null ? parseFloat(d.toFixed(3)) : null;
        const cls = dn===null?'delta-zero':dn>0?'delta-pos':dn<0?'delta-neg':'delta-zero';
        return `<td>${fmt(x)} → ${fmt(y)} <span class="${cls}">${dn===null?'—':(dn>0?'+':'')+dn}</span></td>`;
      }).join("")}</tr>`).join("")}</table>
      <p class="note-sm" style="margin-top:10px">左: ${a.model} ${a.engine} · 右: ${b.model} ${b.engine}</p>`;
  };
}

// ── router ──
async function router() {
  const h = location.hash.slice(2) || "targets";
  const parts = h.split("/");
  try {
    if (parts[0] === "compare") await compare();
    else if (parts[0] === "target" && parts[1]) await targetDetail(decodeURIComponent(parts[1]));
    else if (parts[0] === "run" && parts[1] && parts[2] && parts[3]) await episodeDetail(parts[1], parts[2], parts[3]);
    else if (parts[0] === "run" && parts[1]) await runDetail(parts[1]);
    else if (parts[0] === "targets" || parts[0] === "dashboard") await targets();
    else render(`<h1>404</h1><p class="lede">"<a href="#/targets">targets</a>"</p>`);
  } catch(e) { render(`<h1>error</h1><p class="lede">${esc(e.message||e)}</p>`); }
}
window.addEventListener("hashchange", router);
router();

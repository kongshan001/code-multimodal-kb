// ═══ Measurement Lab · Benchmark Viewer ═══
// 纯 benchmark 焦点：Dashboard（矩阵+逐题）+ Compare（diff）
const $ = (s, p = document) => p.querySelector(s);
const fetchJSON = async u => (await fetch(u)).json();
const fmt = n => typeof n === "number" ? (n !== 0 && Math.abs(n) < 1 ? n.toFixed(3) : n > 999 ? Math.round(n).toLocaleString() : n) : (n ?? "—");
const esc = s => String(s ?? "").replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");
const ARMS = ["no-kb","kb","kb+superpowers","kb+openspec"];

function bar(val, max, isBest) {
  if (!max || typeof val !== "number" || val === 0) return "";
  const w = Math.max(2, Math.min(80, (Math.abs(val) / Math.abs(max)) * 80));
  return `<span class="bar ${isBest?'acc':''}" style="width:${w}px"></span>`;
}

function render(active, html) {
  $("#app").innerHTML = `<div class="topbar">
    <div class="brand">measurement <em>lab</em></div><span class="tag">benchmark viewer</span>
    <nav><a href="#/dashboard" class="${active==='dashboard'?'active':''}">Dashboard</a>
    <a href="#/compare" class="${active==='compare'?'active':''}">Compare</a></nav>
  </div><div class="main">${html}</div>`;
}

// ═══ DASHBOARD — run 选择器 + 矩阵 + 逐题 ═══
async function dashboard(runId) {
  const ac = await fetchJSON("/api/agent-compare");
  const runs = (ac.runs || []).filter(r => !r.smoke);
  if (!runs.length) { render("dashboard", `<h1>dashboard</h1><p class="lede">还没有 agent-compare 结果。先跑一次：<code class="mono">bench run agent-compare</code></p>`); return; }
  const sel = runId || runs[runs.length - 1].run_id;
  const opts = runs.slice().reverse().map(r => `<option value="${r.run_id}" ${r.run_id===sel?'selected':''}>${r.run_id.slice(0,20)}… ${r.model||''} ${r.n_questions||'?'}题 ${r.engine||''}</option>`).join("");
  render("dashboard", `
    <h1>dashboard</h1>
    <p class="lede">agent-compare benchmark 结果。</p>
    <div style="margin-bottom:20px"><select id="runSel" onchange="location.hash='#/dashboard/'+this.value">${opts}</select></div>
    <div id="dashBody"><div class="loading">loading…</div></div>`);
  // 加载选定 run 的矩阵 + 逐题
  const [summary, qData] = await Promise.all([
    fetchJSON(`/api/agent-compare/${sel}`),
    fetchJSON(`/api/agent-compare/${sel}/questions`),
  ]);
  const m = summary.matrix || {};
  const arms = summary.arms || ARMS;
  const bestArm = arms.reduce((b,a) => (m[a]?.accuracy ?? 0) > (m[b]?.accuracy ?? 0) ? a : b, arms[0]);
  const metrics = [
    ["accuracy","准确率",true],["mean_total_tokens","tokens",false],
    ["no_tool_rate","no_tool",false],["truncated_rate","trunc",false],
    ["mean_llm_calls","llm_calls",false],["mean_tool_steps","tool_steps",false],
    ["mean_cost_$","cost $",false],
  ];

  // 矩阵表
  const matrixHTML = `
    <div class="sec-h"><span class="n">A</span><h2>矩阵 · ${summary.model||'?'} · ${summary.engine||'sdk'}</h2><span class="line"></span></div>
    <table class="matrix">
      <tr><th>metric</th>${arms.map(a=>`<th class="${a===bestArm?'best':''}">${a}</th>`).join("")}</tr>
      ${metrics.map(([k,label,lower]) => {
        const vals = arms.map(a => m[a]?.[k]);
        const nums = vals.filter(v => typeof v === "number");
        const best = lower ? Math.min(...nums, Infinity) : Math.max(...nums, -Infinity);
        return `<tr><td>${label}</td>${arms.map((a,i) => {
          const v = vals[i]; const isBest = v === best && typeof v === "number";
          return `<td class="${isBest?'best':''}">${fmt(v)}${bar(v, Math.max(...nums.map(Math.abs)), isBest)}</td>`;
        }).join("")}</tr>`;
      }).join("")}
    </table>`;

  // 逐题表
  const qs = qData.questions || {};
  const qids = Object.keys(qs).sort();
  const qHTML = `
    <div class="sec-h"><span class="n">B</span><h2>逐题 · ${qids.length} 题</h2><span class="line"></span></div>
    <table class="tbl" id="qTable">
      <tr><th>qid</th><th>type</th><th>query</th>${arms.map(a=>`<th style="text-align:center">${a.replace('kb+','').replace('kb','kb')}</th>`).join("")}<th></th></tr>
      ${qids.map(qid => {
        const q = qs[qid];
        const cells = arms.map(a => {
          const ep = q[a]; if (!ep) return '<td style="text-align:center;color:var(--ink3)">—</td>';
          const c = ep.correct ? 'var(--good)' : 'var(--bad)';
          const sym = ep.correct ? '✓' : '✗';
          const trunc = ep.truncated ? '<span style="color:var(--warn);font-size:8px">⚠</span>' : '';
          return `<td style="text-align:center;color:${c};font-weight:600">${sym}${trunc}</td>`;
        }).join("");
        const diverge = arms.some(a => q[a] && arms.some(b => q[b] && q[a]?.correct !== q[b]?.correct));
        return `<tr style="${diverge?'background:rgba(199,91,57,.04)':''}" onclick="qDetail('${sel}','${qid}')">
          <td class="mono" style="font-size:9px">${qid}</td><td style="font-size:9px;color:var(--ink3)">${q.type||''}</td>
          <td style="font-size:10px">${esc((q.query||'').slice(0,42))}${(q.query||'').length>42?'…':''}</td>
          ${cells}<td style="font-size:9px;color:var(--ink3)">▸</td></tr>`;
      }).join("")}
    </table>
    <p class="note-sm" style="margin-top:8px">✓=答对 ✗=答错 ⚠=截断(truncated) · 底色高亮=臂间分化 · 点行看详情</p>`;

  $("#dashBody").innerHTML = matrixHTML + qHTML;
}

// 逐题详情（弹出层）
window.qDetail = async (runId, qid) => {
  const qData = await fetchJSON(`/api/agent-compare/${runId}/questions`);
  const q = (qData.questions || {})[qid];
  if (!q) return;
  const arms = ARMS.filter(a => q[a]);
  const detail = arms.map(a => {
    const ep = q[a];
    return `<div style="padding:10px 0;border-bottom:1px solid var(--rule)">
      <div style="display:flex;align-items:center;gap:8px;margin-bottom:4px">
        <span class="mono" style="font-size:10px;font-weight:600">${a}</span>
        <span style="color:${ep.correct?'var(--good)':'var(--bad)'};font-weight:700">${ep.correct?'✓ 正确':'✗ 错误'}</span>
        ${ep.truncated?'<span class="badge" style="color:var(--warn);border-color:var(--warn)">⚠ 截断</span>':''}
        <span class="note-sm" style="margin-left:auto">${ep.llm_calls} calls · ${ep.total_tokens} tok · ${ep.tool_steps} tools</span>
      </div>
      <div style="font-size:11px;color:var(--ink2);margin-bottom:4px">答: ${esc(ep.answer||'(空)')}</div>
      <div class="mono" style="font-size:9px;color:var(--ink3)">工具: ${(ep.tool_calls||[]).join(' → ')||'(未用)'}</div>
    </div>`;
  }).join("");
  // 替换表格下方的详情区（或追加）
  let panel = $("#qPanel");
  if (panel) panel.remove();
  const row = [...document.querySelectorAll('#qTable tr')].find(tr => tr.textContent.includes(qid));
  if (row) {
    panel = document.createElement('div');
    panel.id = 'qPanel';
    panel.style.cssText = 'padding:14px 18px;background:var(--paper);border:1px solid var(--ink);border-radius:4px;margin:8px 0 20px';
    panel.innerHTML = `
      <div style="display:flex;align-items:center;gap:10px;margin-bottom:10px">
        <b class="mono" style="font-size:12px">${qid}</b>
        <span class="note-sm">${esc(q.query||'')}</span>
        <span class="note-sm" style="margin-left:auto">gold: ${esc((q.gold||[]).join(', '))}</span>
        <button class="btn" style="font-size:9px;padding:2px 8px" onclick="this.parentElement.parentElement.remove()">✕</button>
      </div>
      ${detail}`;
    row.parentNode.insertBefore(panel, row.nextSibling);
  }
};

// ═══ COMPARE — 两个 run 矩阵 diff ═══
async function compare() {
  const ac = await fetchJSON("/api/agent-compare");
  const runs = (ac.runs || []).filter(r => !r.smoke);
  const opts = runs.slice().reverse().map(r => `<option value="${r.run_id}">${r.run_id.slice(0,20)}… ${r.model||''} ${r.n_questions||'?'}题</option>`).join("");
  render("compare", `
    <h1>compare <em>· 矩阵 diff</em></h1>
    <p class="lede">选两个 agent-compare run 看指标 diff。</p>
    <div style="display:flex;gap:8px;align-items:center;margin-bottom:20px;flex-wrap:wrap">
      <select id="cmpA">${opts}</select>
      <span class="note-sm">vs</span>
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
    $("#cmpOut").innerHTML = `
      <table class="matrix">
        <tr><th>metric</th>${arms.map(ar=>`<th>${ar}<br><span class="note-sm" style="font-weight:400">${a.model||''} → ${b.model||''}</span></th>`).join("")}</tr>
        ${keys.map(([k,label]) => `<tr><td>${label}</td>${arms.map(ar => {
          const x = a.matrix?.[ar]?.[k], y = b.matrix?.[ar]?.[k];
          const d = (typeof x==="number" && typeof y==="number") ? y - x : null;
          const dn = d !== null ? parseFloat(d.toFixed(3)) : null;
          const cls = dn===null?'delta-zero':dn>0?'delta-pos':dn<0?'delta-neg':'delta-zero';
          const sign = dn>0?'+':'';
          return `<td>${fmt(x)} → ${fmt(y)} <span class="${cls}">${dn===null?'—':sign+dn}</span></td>`;
        }).join("")}</tr>`).join("")}
      </table>
      <p class="note-sm" style="margin-top:10px">左: ${a.model} ${a.engine} ${a.n_questions}题 · 右: ${b.model} ${b.engine} ${b.n_questions}题</p>`;
  };
}

// ── router ──
async function router() {
  const h = location.hash.slice(2) || "dashboard";
  const parts = h.split("/");
  try {
    if (parts[0] === "compare") await compare();
    else if (parts[0] === "dashboard") await dashboard(parts[1]);
    else render("", `<h1>404</h1><p class="lede">"${h}" — 只有 <a href="#/dashboard">Dashboard</a> 和 <a href="#/compare">Compare</a>。</p>`);
  } catch(e) { render("", `<h1>error</h1><p class="lede">${esc(e.message||e)}</p>`); }
}
window.addEventListener("hashchange", router);
router();

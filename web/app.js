// measurement lab · SPA（vanilla JS，读真实归档 JSON）
const $ = (s, p = document) => p.querySelector(s);
const view = () => $("#view");
const fetchJSON = async (u) => (await fetch(u)).json();

// ── helpers ──
function latest(reports, subjContains) {
  const rs = reports.filter(r => r.subject.includes(subjContains) || r.variant.includes(subjContains));
  return rs[rs.length - 1];  // index 追加式，最后 = 最新
}
function headline(r) {
  if (!r || !r.aggregate) return "—";
  const a = r.aggregate;
  for (const k of ["mean_broad_recall@5", "mean_hit@5", "mean_compression_read",
                   "mean_faithfulness", "routing_overall_accuracy", "crosstool_success_rate"])
    if (k in a) return a[k];
  return "—";
}
function fmt(n) { return typeof n === "number" ? (Math.abs(n) < 1 && n !== 0 ? n.toFixed(3) : n) : n; }

// ── views ──
async function dashboard() {
  const { reports } = await fetchJSON("/api/reports");
  const code = latest(reports, "cmm.bm25") || latest(reports, "cmm.");
  const mem = latest(reports, "mempalace");
  const ab = latest(reports, "ab-value");
  const doc = latest(reports, "doc-quality");
  const memHit = mem ? headline(mem) : "—";
  view().innerHTML = `
    <h1>dashboard</h1>
    <p class="lede">知识库 / 记忆系统的体检台 — 不评感觉，评数字。</p>
    <section class="hero">
      <div class="m"><div class="lbl">代码检索 broad@5</div><div class="num">${fmt(headline(code))}</div><div class="ctx">${code ? code.subject : "—"}</div></div>
      <div class="m"><div class="lbl">记忆召回 hit@5</div><div class="num">${fmt(memHit)}</div><div class="ctx">${mem ? mem.subject : "—"}</div></div>
      <div class="m"><div class="lbl">A/B 压缩比</div><div class="num acc">${ab ? headline(ab) + "×" : "—"}</div><div class="ctx">${ab ? ab.subject : "—"}</div></div>
      <div class="m"><div class="lbl">答案 faithfulness</div><div class="num">${fmt(headline(doc))}<span class="badge">LLM-judged</span></div><div class="ctx">${doc ? doc.subject : "—"}</div></div>
    </section>
    <div class="h"><span class="n">01</span><h2>归档 · 最近跑过</h2><span class="line"></span></div>
    <table class="t"><tr><th>time</th><th>subject</th><th>variant</th><th>headline</th><th></th></tr>
    ${reports.slice().reverse().slice(0, 8).map(r => `<tr onclick="location.hash='#/report/${r.id}'">
      <td>${(r.readable_ts || r.ts || "").slice(5, 16)}</td>
      <td class="sb">${r.subject}</td><td>${r.variant}</td><td>${headline(r)}</td><td>show ▸</td></tr>`).join("")}
    </table>`;
}

async function reports() {
  const { reports } = await fetchJSON("/api/reports");
  view().innerHTML = `<h1>归档 <em>· reports</em></h1><p class="lede">${reports.length} 份历史评测，点行看详情。</p>
    <table class="t"><tr><th>id</th><th>subject</th><th>variant</th><th>ts</th><th>headline</th></tr>
    ${reports.slice().reverse().map(r => `<tr onclick="location.hash='#/report/${r.id}'">
      <td>${r.id.slice(0, 24)}…</td><td class="sb">${r.subject}</td><td>${r.variant}</td>
      <td>${(r.readable_ts || r.ts || "").slice(5, 16)}</td><td>${headline(r)}</td></tr>`).join("")}</table>`;
}

async function reportDetail(id) {
  const r = await fetchJSON("/api/report/" + id);
  const agg = r.aggregate || {};
  const pq = r.per_query || [];
  view().innerHTML = `
    <h1>${r.subject} <em>· detail</em></h1>
    <p class="lede">${r.variant} · n=${r.n || pq.length} · ${r.target || ""}</p>
    <div class="h"><span class="n">A</span><h2>aggregate</h2><span class="line"></span></div>
    <div class="kv">${Object.entries(agg).map(([k, v]) => `<span>${k}</span> = <b>${fmt(v)}</b><br>`).join("")}</div>
    <div class="h"><span class="n">B</span><h2>per_query（${pq.length}）</h2><span class="line"></span></div>
    <table class="t"><tr><th>query</th><th>headline</th></tr>
    ${pq.slice(0, 30).map(q => `<tr><td>${(q.query || "").slice(0, 50)}</td><td>${headline({aggregate: q})}</td></tr>`).join("")}</table>
    <p class="lede" style="margin-top:18px">lockfile: ${JSON.stringify(r.lockfile || {})}</p>`;
}

async function compare() {
  const { reports } = await fetchJSON("/api/reports");
  const opts = reports.map(r => `<option value="${r.id}">${r.id.slice(0, 20)}… ${r.subject}`).join("");
  view().innerHTML = `<h1>compare <em>· 对比</em></h1><p class="lede">选两份归档，看 aggregate diff。</p>
    <p style="margin:12px 0"><select id="cmpA" class="btn">${opts}</select>
    <select id="cmpB" class="btn">${opts}</select>
    <button class="btn fill" onclick="doCompare()">对比 ▸</button></p>
    <div id="cmpResult"></div>`;
  window.doCompare = async () => {
    const a = await fetchJSON("/api/report/" + $("#cmpA").value);
    const b = await fetchJSON("/api/report/" + $("#cmpB").value);
    const keys = [...new Set([...Object.keys(a.aggregate || {}), ...Object.keys(b.aggregate || {})])].sort();
    $("#cmpResult").innerHTML = `<table class="t"><tr><th>metric</th><th>left</th><th>right</th><th>delta</th></tr>
      ${keys.map(k => { const x = a.aggregate?.[k], y = b.aggregate?.[k];
        const d = (typeof x === "number" && typeof y === "number") ? (y - x).toFixed(3) : "—";
        return `<tr><td>${k}</td><td>${fmt(x)}</td><td>${fmt(y)}</td><td>${d}</td></tr>`; }).join("")}</table>`;
  };
}

// ── 能力目录（scaffold catalog · 页签版 · 面向目标工程）──
async function catalogView() {
  // 默认目标工程
  window._targetProject = window._targetProject || "/Users/ks_128/Documents/godot-src/core";

  view().innerHTML = `
    <h1>能力目录 <em>· agent scaffold</em></h1>
    <p class="lede">选择目标工程 → 浏览策展能力 → 按需装/卸到该工程。</p>

    <!-- 目标工程选择 -->
    <div style="display:flex;gap:10px;align-items:center;margin-bottom:20px;padding:14px 18px;border:1.5px solid var(--ink);background:#fff">
      <label class="mono" style="font-size:10px;color:var(--ink2);letter-spacing:1px">目标工程</label>
      <input id="tgtPath" class="btn" value="${window._targetProject}" style="flex:1;text-align:left;font-family:'JetBrains Mono',monospace"/>
      <button class="btn fill" onclick="loadCatalogFor()">检测 ▸</button>
    </div>
    <div id="catalogArea"><div class="loading">点"检测"扫描目标工程…</div></div>`;

  window.loadCatalogFor = async () => {
    window._targetProject = $("#tgtPath").value || "/Users/ks_128/Documents/godot-src/core";
    $("#catalogArea").innerHTML = `<div class="loading">检测 ${window._targetProject}…</div>`;
    const url = `/api/catalog?project=${encodeURIComponent(window._targetProject)}`;
    const data = await fetchJSON(url);
    window._catData = data;
    const d = data.detection;
    const s = data.summary;

    const tabs = data.categories.filter(c => c.id !== "engineering-practices").map((cat, i) => {
      const inst = cat.capabilities.filter(c => c.installed).length;
      return `<div class="ctab ${i===0?"active":""}" onclick="switchCat(${i})">${cat.name}<span class="badge">${inst}/${cat.capabilities.length}</span></div>`;
    }).join("");

    $("#catalogArea").innerHTML = `
      <!-- 检测摘要 -->
      <div class="gate ${s.not_installed_recommended === 0 ? "ok" : ""}">
        <span class="dot"></span>
        <div><b>${d.language}</b> · ${d.has_code?"源码✓":""} ${d.has_docs?"文档✓":""} ${d.has_tests?"测试✓":""} ${d.has_frontend?"前端✓":""}
          <div style="font-size:11px;color:var(--ink2);margin-top:2px">${s.installed}/${s.total} 能力可用 · ${s.recommended} 项推荐 · 路径：<span class="mono" style="font-size:10px">${d.path}</span></div>
        </div>
      </div>
      <div class="ctabs">${tabs}</div>
      <div id="catBody"></div>`;
    renderCat(0);
  };

  window.renderCat = (i) => {
    const cat = window._catData.categories[i];
    const rb = c => c.recommendation === "推荐" ? `<span style="color:var(--accent);font-size:10px;font-weight:600">推荐</span>`
      : c.cost ? `<span style="color:var(--warn);font-size:10px">⚠ ${c.cost}</span>` : `<span style="color:var(--ink2);font-size:10px">可选</span>`;
    $("#catBody").innerHTML = `
      <p style="font-size:12px;color:var(--ink2);margin:0 0 14px">${cat.desc}</p>
      <table class="t">
        ${cat.capabilities.map(cap => `<tr>
          <td>
            <div style="font-weight:500;font-size:13px">${cap.name} <span style="font-size:9px;color:var(--ink2)">[${cap.type}]</span> ${rb(cap)}</div>
            <div style="font-size:11px;color:var(--ink2)">${cap.desc}</div>
            ${cap.value ? `<div style="font-size:11px;color:var(--good);margin-top:3px">📊 ${cap.value}</div>` : ""}
            ${cap.guide ? `<details style="margin-top:4px"><summary style="font-size:10px;color:var(--ink2);cursor:pointer">📖 使用指南</summary><div style="font-size:11px;color:var(--ink2);padding:6px 0 2px;line-height:1.5">${cap.guide}</div></details>` : ""}
            ${(cap.docs||[]).length ? `<div style="margin-top:3px">${cap.docs.map(d => `<a href="${d.url}" target="_blank" style="font-size:10px;margin-right:10px;text-decoration:underline">🔗 ${d.title}</a>`).join("")}</div>` : ""}
            ${cap.source ? `<div style="margin-top:2px"><a href="${cap.source}" target="_blank" style="font-size:10px;color:var(--ink2);text-decoration:underline">📦 ${cap.source.replace('https://github.com/','github.com/')}</a></div>` : ""}
          </td>
          <td style="text-align:right;width:100px;white-space:nowrap">
            ${cap.installable && !cap.installed
              ? `<button class="btn fill" style="font-size:10px;padding:4px 12px" onclick="toggleCap('${cap.id}','${cap.name}')">安装</button>`
              : `<span class="st ${cap.installed?'ok':'miss'}" style="font-size:11px">${cap.installed?'✓ 已装':'☐ 未装'}</span>`}
          </td>
        </tr>`).join("")}
      </table>`;
  };
  window.switchCat = (i) => {
    document.querySelectorAll(".ctab").forEach((t, j) => t.classList.toggle("active", j === i));
    window.renderCat(i);
  };
  window.toggleCap = async (capId, capName) => {
    const cap = window._catData?.categories?.flatMap(c => c.capabilities).find(c => c.id === capId);
    if (!cap) { return; }
    const isUninstall = cap.installed;
    const action = isUninstall ? "卸载" : "安装";
    const cmd = isUninstall ? (cap.uninstall_cmd || "") : (cap.install_cmd || "");
    const apiPath = isUninstall ? "/api/uninstall" : "/api/install";

    // 找到按钮行
    const btn = [...document.querySelectorAll('button')].find(b => b.getAttribute('onclick')?.includes(capId));
    const row = btn?.closest('tr');
    const btnOriginal = btn ? btn.outerHTML : '';
    if (btn) { btn.disabled = true; btn.textContent = "⏳ 执行中..."; btn.style.opacity = "0.6"; }

    // 在按钮行下方插入日志行（不受 catalog 刷新影响——直到手动刷新）
    let logRow = document.querySelector('#capLogRow');
    if (logRow) logRow.remove();
    logRow = document.createElement('tr');
    logRow.id = 'capLogRow';
    logRow.innerHTML = `<td colspan="4" style="padding:14px 16px;background:#fff;border:1.5px solid var(--ink);font-family:'JetBrains Mono',monospace;font-size:11px;white-space:pre-wrap;line-height:1.6;color:var(--ink)">
      <b style="color:var(--accent);font-size:13px">${action} ${capName}</b>
<span style="color:var(--ink2)">执行指令：</span>
<code style="color:var(--ink)">$ ${cmd || '(内部操作)'}</code>

<span style="color:var(--ink2)">⏳ 正在执行...</span></td>`;
    if (row?.parentNode) row.parentNode.insertBefore(logRow, row.nextSibling);

    if (isUninstall && !confirm(`确定${action} ${capName}？`)) {
      if (btn) { btn.disabled = false; btn.outerHTML = btnOriginal; }
      logRow.remove();
      return;
    }

    try {
      const payload = {id: capId};
      if (!isUninstall) payload.project = window._targetProject;
      const r = await fetch(apiPath, {method:"POST", headers:{"Content-Type":"application/json"}, body: JSON.stringify(payload)});
      const o = await r.json();
      const ok = o.rc === 0;
      const output = (o.stdout || o.error || "").slice(0, 500);
      const color = ok ? 'var(--good)' : 'var(--bad)';
      logRow.innerHTML = `<td colspan="4" style="padding:14px 16px;background:#fff;border:1.5px solid var(--ink);font-family:'JetBrains Mono',monospace;font-size:11px;white-space:pre-wrap;line-height:1.6;color:var(--ink)">
        <b style="color:${color};font-size:13px">${ok?'✓':'⚠'} ${action}${ok?'成功':'失败'}：${capName}</b>
<span style="color:var(--ink2)">执行指令：</span>
<code style="color:var(--ink)">$ ${cmd || '(内部操作)'}</code>

<span style="color:var(--ink2)">输出：</span>
${output}

<span style="color:var(--ink2)">→ </span><a href="#/catalog" onclick="setTimeout(()=>window.loadCatalogFor(),100);return true;" style="color:var(--accent);text-decoration:underline">刷新状态</a></td>`;
    } catch(e) {
      logRow.innerHTML = `<td colspan="4" style="padding:14px;background:#fff;border:1.5px solid var(--bad);font-family:monospace;font-size:11px;color:var(--bad)">⚠ 操作失败: ${e}</td>`;
    }
  };
  window.loadCatalogFor();  // 首次自动加载
}

function runConsole() {
  view().innerHTML = `
    <h1>run console <em>· 触发评测</em></h1>
    <p class="lede">从浏览器跑 bench（后端 subprocess 调 eval.cli）。跑完自动进归档。</p>
    <div style="display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin-bottom:18px">
      <label class="mono" style="font-size:10px;color:var(--ink2)">subject</label>
      <select id="rcSubj" class="btn" onchange="rcUpdateForm()">
        <option value="code">code（代码检索）</option>
        <option value="memory">memory（记忆召回+路由）</option>
        <option value="ab">ab（Stage0 token 代理）</option>
        <option value="doc-ragas">doc-ragas（答案质量）</option>
      </select>
      <span id="rcTargetWrap"><label class="mono" style="font-size:10px;color:var(--ink2)">target</label>
      <input id="rcTarget" class="btn" value="godot-core" style="width:120px"/></span>
      <span id="rcMethodWrap"><label class="mono" style="font-size:10px;color:var(--ink2)">method</label>
      <select id="rcMethod" class="btn"><option>bm25</option><option>grep</option><option>semantic</option></select></span>
      <button class="btn fill" onclick="doRun()">跑 ▸</button>
    </div>
    <div id="rcOut" class="mono" style="background:#fff;border:1px solid var(--rule);padding:16px;font-size:11px;white-space:pre-wrap;min-height:80px;color:var(--ink2)">选参数点"跑"——结果这里出。</div>`;
  window.rcUpdateForm = () => {
    const subj = $("#rcSubj").value;
    // 只有 code 有 method
    $("#rcMethodWrap").style.display = subj === "code" ? "" : "none";
    // 各 subject 的默认 target
    const defaults = {code:"godot-core", memory:"engineer-demo-memory", ab:"godot-core", "doc-ragas":"godot-docs"};
    $("#rcTarget").value = defaults[subj] || "godot";
  };
  window.doRun = async () => {
    const subj = $("#rcSubj").value;
    $("#rcOut").textContent = "running…（" + subj + "，可能要几秒～几分钟）";
    try {
      const payload = {subject: subj, target: $("#rcTarget").value};
      if (subj === "code") payload.method = $("#rcMethod").value;
      const r = await fetch("/api/run", {method: "POST", headers: {"Content-Type": "application/json"},
        body: JSON.stringify(payload)});
      const o = await r.json();
      $("#rcOut").innerHTML = `<b style="color:${o.rc === 0 ? "var(--good)" : "var(--bad)"}">exit ${o.rc}</b>\n\n${(o.stdout || "").slice(-1500)}${o.stderr ? "\n⚠ " + o.stderr.slice(-300) : ""}`;
    } catch (e) { $("#rcOut").textContent = "⚠ " + e; }
  };
}

async function setupView() {
  const h = await fetchJSON("/api/health");
  const d = h.deps || {};
  const row = (name, key, desc, warn) => `<tr>
    <td class="nm">${name}</td><td class="st ${d[key] ? "ok" : "miss"}">${d[key] ? "✓ " + d[key] : "✗ 缺"}</td>
    <td style="color:var(--ink2);font-size:11px">${desc}${warn ? `<br><i style="color:var(--warn)">${warn}</i>` : ""}</td></tr>`;
  view().innerHTML = `
    <h1>setup <em>· 环境体检</em></h1>
    <p class="lede">工具与凭据状态。${h.ready ? "环境就绪，可进评测。" : "有缺项——装齐再 bench。"}</p>
    <div class="gate ${h.ready ? "ok" : ""}"><span class="dot"></span>
      <b>${h.ready ? "环境就绪 ✓" : "有缺项"}</b>　<button class="btn" onclick="location.reload()">刷新</button></div>
    <div class="h"><span class="n">A</span><h2>KB 工具</h2><span class="line"></span></div>
    <table class="t dep">${row("cmm","cmm","代码符号/调用图 KB")}
      ${row("graphify","graphify","文档图 KB（建图花 LLM）")}
      ${row("codegraph","codegraph","第二代码 KB（A/B + goldgen）","")}
      ${row("mempalace","mempalace","记忆层","⚠ Intel Mac 必须 py3.11")}</table>
    <div class="h"><span class="n">B</span><h2>Python / 凭据</h2><span class="line"></span></div>
    <table class="t dep">${row("python","python","pytest + anthropic","✗ 勿装 ragas（库冲突）/ numpy≥2")}
      ${row("render","render","SVG→PNG（流程图用）")}
      ${row("LLM 凭据","creds","agent A/B + 答案质量用","⚠ 同家族 self-preference")}</table>
    <p class="lede" style="margin-top:18px">后端是 setup.sh——这里只体检。装缺的跑：<code class="mono">./setup.sh tools</code></p>`;
}

function placeholder(title, desc, mockup) {
  view().innerHTML = `<h1>${title}</h1><p class="lede">${desc}</p>
    <div class="h"><span class="n">→</span><h2>设计 mockup</h2><span class="line"></span></div>
    <p style="font-size:13px;color:var(--ink2)">详细交互设计见 <a href="${mockup}">${mockup}</a>（已做 HTML mockup）。</p>`;
}

// ── onboarding 5 步向导 ──
function onboardView() {
  const steps = [
    {n:"01", t:"连代码库 · 索引", act:"codegraph", lbl:"代码库路径", val:"/path/to/your/repo", desc:"codegraph init（静态零 LLM，秒级）"},
    {n:"02", t:"文档图（可选）", act:"docgraph", lbl:"文档目录", val:"/path/to/docs", desc:"graphify build · ⚠ 花 LLM（按量计费，先估成本）", warn:"建图调 LLM 抽取，按量计费。graph.json 可提交 repo 团队共享。"},
    {n:"03", t:"会话 mine（可选）", act:"mine", lbl:"会话目录 ~/.claude/projects/<proj>", val:"", desc:"mempalace mine --mode convos", warn:"⚠ 勿配非 idempotent 的 auto-save hook（会 bloat，实测召回 0.933→0.6，见 runbook §D.4）。这里只手动 mine 一次。"},
  ];
  view().innerHTML = `
    <h1>project <em>· 接入你的工程</em></h1>
    <p class="lede">5 步把你的代码库/文档/会话接进来。每步可跳过，跑完进 Gold lab 造题。</p>
    ${steps.map(s => `
      <div style="border:1.5px solid var(--ink);background:#fff;padding:20px;margin-bottom:16px">
        <div class="mono" style="font-size:10px;color:var(--accent);letter-spacing:1px">${s.n}</div>
        <h3 style="font-family:Fraunces,serif;font-size:18px;margin:2px 0 4px">${s.t}</h3>
        <p style="font-size:12px;color:var(--ink2);margin-bottom:12px">${s.desc}</p>
        ${s.warn ? `<div style="border-left:3px solid var(--warn);background:#fdf6e9;padding:8px 12px;font-size:11px;margin-bottom:12px">${s.warn}</div>` : ""}
        <div style="display:flex;gap:8px">
          <input id="ob_${s.act}" class="btn" placeholder="${s.lbl}" value="${s.val}" style="flex:1;text-align:left"/>
          <button class="btn fill" onclick="doOnboard('${s.act}')">跑 ▸</button>
        </div>
        <div id="ob_out_${s.act}" class="mono" style="margin-top:10px;font-size:11px;color:var(--ink2);min-height:14px"></div>
      </div>`).join("")}
    <div style="border:1.5px solid var(--ink);background:var(--cream);padding:20px;margin-bottom:16px">
      <div class="mono" style="font-size:10px;color:var(--accent);letter-spacing:1px">04</div>
      <h3 style="font-family:Fraunces,serif;font-size:18px;margin:2px 0 4px">生成 gold</h3>
      <p style="font-size:12px;color:var(--ink2)">给接进来的代码造题（agent 挖符号 + 两层验收 + 人审）→ <a href="#/goldlab">进 Gold lab ▸</a></p>
    </div>
    <div style="border:1.5px solid var(--ink);background:var(--cream);padding:20px">
      <div class="mono" style="font-size:10px;color:var(--good);letter-spacing:1px">05</div>
      <h3 style="font-family:Fraunces,serif;font-size:18px;margin:2px 0 4px">就绪 → bench</h3>
      <p style="font-size:12px;color:var(--ink2)">接好了 → <a href="#/run">Run console</a> 跑你自己的系统。</p>
    </div>`;
  window.doOnboard = async (act) => {
    const path = $(`#ob_${act}`).value;
    $(`#ob_out_${act}`).textContent = "running…";
    try {
      const r = await fetch("/api/onboard", {method:"POST", headers:{"Content-Type":"application/json"},
        body: JSON.stringify({action: act, path})});
      const o = await r.json();
      $(`#ob_out_${act}`).innerHTML = `<b style="color:${o.rc===0?"var(--good)":"var(--bad)"}">exit ${o.rc}</b> ${(o.stdout||"").slice(-400)}${o.stderr?" ⚠ "+o.stderr.slice(-150):""}`;
    } catch(e) { $(`#ob_out_${act}`).textContent = "⚠ " + e; }
  };
}

// ── gold lab（扩题 4 阶段）──
// ── gold lab 题库编辑器（读写 targets/<id>/problems.json）──
const _GOLD_FIELDS = {
  code_retrieval:  [{k:'symbols', label:'gold 符号（逗号分隔，如 Color, vformat）', list:true}],
  doc_retrieval:   [{k:'node_labels', label:'文档节点 label（逗号分隔）', list:true}],
  cross_anchor:    [{k:'doc_node_label', label:'文档节点 label'},
                    {k:'cmm_identifier', label:'喂给 cmm 的标识符'},
                    {k:'code_file', label:'期望代码文件（子串，如 math/vector2）'}],
  memory_recall:   [{k:'source_files', label:'source 文件（逗号分隔，如 agent-memory-approach.md）', list:true}],
  memory_routing:  [{k:'layer', label:'归属层', select:['objective','procedural','episodic','subjective']},
                    {k:'signal', label:'判定线索 signal（如 用户偏好）'}],
};
const _TEXT_FIELD = {memory_routing:'fact'};  // 其余 type 用 query
const _TYPES = Object.keys(_GOLD_FIELDS);
function _esc(s){return String(s==null?'':s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));}
function _goldText(p){return p[_TEXT_FIELD[p.type]||'query']||'';}
function _goldSummary(p){
  const g=p.gold||{};
  switch(p.type){
    case 'code_retrieval': return (g.symbols||[]).join(', ');
    case 'doc_retrieval': return (g.node_labels||[]).join(', ');
    case 'memory_recall': return (g.source_files||[]).join(', ');
    case 'memory_routing': return `layer=${g.layer}` + (g.signal?` · ${g.signal}`:'');
    case 'cross_anchor': return `${g.cmm_identifier} → ${g.code_file}`;
  } return JSON.stringify(g);
}

async function goldlabView() {
  window._goldTarget = window._goldTarget || 'godot-core';
  let targets = [];
  try { targets = (await fetchJSON('/api/targets')).targets; }
  catch(e) {}
  if (!targets.length) targets = [{id: window._goldTarget, subjects:[]}];
  view().innerHTML = `
    <h1>gold lab <em>· 题库编辑器</em></h1>
    <p class="lede">直接读写 <code>targets/&lt;id&gt;/problems.json</code>——列表 / 新增 / 改 / 删 / approve pending。<b>前端不自动 git commit</b>，改完记得自行提交。</p>
    <div id="goldDirty" style="display:none;border-left:3px solid var(--warn);background:#fdf6e9;padding:10px 14px;margin-bottom:14px;font-size:12px">
      ⚠ 题库已改 —— 记得 <code class="mono">git add eval/targets/ && git commit && git push</code>（前端不替你提交）
      <button class="btn" style="font-size:10px;margin-left:12px" onclick="$('#goldDirty').style.display='none'">已提交，隐藏</button>
    </div>
    <div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin-bottom:14px">
      <label class="mono" style="font-size:10px;color:var(--ink2)">target</label>
      <select id="glTarget" class="btn" onchange="window._goldTarget=this.value;goldRender()">${targets.map(t=>`<option value="${t.id}" ${t.id===window._goldTarget?'selected':''}>${t.id} [${(t.subjects||[]).join(',')||'?'}]</option>`).join('')}</select>
      <button class="btn" onclick="goldRender()">刷新</button>
      <span style="flex:1"></span>
      <input id="glSeeds" class="btn" placeholder="seed 词（goldgen 用，如 Vector color）" style="width:220px;text-align:left"/>
      <button class="btn" onclick="goldGen()">① goldgen</button>
      <button class="btn" onclick="goldVerify()">② 验收</button>
      <button class="btn fill" onclick="goldFormOpen(null)">+ 新增题目</button>
    </div>
    <div id="goldForm"></div>
    <div id="goldOut" class="mono" style="font-size:11px;color:var(--ink2);min-height:14px;margin:8px 0"></div>
    <div class="h"><span class="n">题库</span><h2 id="goldCount">…</h2><span class="line"></span></div>
    <div id="goldTable"><div class="loading">loading…</div></div>`;
  await goldRender();
}

async function goldRender() {
  const tgt = window._goldTarget;
  let data;
  try { data = await fetchJSON('/api/gold/' + encodeURIComponent(tgt)); }
  catch(e){ $('#goldTable').innerHTML = `<div class="loading">⚠ ${e}</div>`; return; }
  window._goldProblems = data.problems;
  const ps = data.problems;
  const npend = ps.filter(p=>p.status==='pending').length;
  $('#goldCount').textContent = `${tgt} · ${ps.length} 题（pending ${npend}）`;
  $('#goldForm').innerHTML = '';  // 收起表单
  if (!ps.length) { $('#goldTable').innerHTML = `<p class="lede">（空）点 "+ 新增题目" 手动加，或 ① goldgen 自动造题</p>`; return; }
  $('#goldTable').innerHTML = `<table class="t"><tr><th>id</th><th>type</th><th>query / fact</th><th>gold</th><th>status</th><th>tags</th><th style="text-align:right">操作</th></tr>
    ${ps.map(p=>{
      const pend = p.status==='pending';
      return `<tr>
        <td class="mono" style="font-size:10px;color:var(--ink2)">${_esc(p.id)}</td>
        <td style="font-size:11px">${p.type}</td>
        <td style="max-width:280px">${_esc(_goldText(p)).slice(0,60)}</td>
        <td style="font-size:11px;color:var(--ink2)">${_esc(_goldSummary(p))}</td>
        <td><span class="st ${pend?'miss':'ok'}" style="font-size:10px">${pend?'.Pending':'.accepted'}</span>${p.verdict?` <span style="font-size:9px;color:${p.verdict==='pass'?'var(--good)':'var(--warn)'}">${p.verdict}</span>`:''}</td>
        <td style="font-size:10px;color:var(--accent)">${(p.tags||[]).join(' ')}</td>
        <td style="text-align:right;white-space:nowrap">
          ${pend?`<button class="btn" style="font-size:10px;padding:3px 10px" onclick="goldApprove('${_esc(p.id)}')">✓ approve</button>`:''}
          <button class="btn" style="font-size:10px;padding:3px 10px" onclick="goldFormOpen('${_esc(p.id)}')">✎</button>
          <button class="btn" style="font-size:10px;padding:3px 10px" onclick="goldDelete('${_esc(p.id)}')">🗑</button>
        </td></tr>`;
    }).join('')}</table>`;
}

function _goldFieldsHTML(type, gold) {
  gold = gold || {};
  return _GOLD_FIELDS[type].map(f=>{
    const val = f.list ? (gold[f.k]||[]).join(', ') : (gold[f.k]||'');
    if (f.select) return ` <select id="gf_${f.k}" class="btn">${f.select.map(o=>`<option ${o===val?'selected':''}>${o}</option>`).join('')}</select>`;
    return ` <input id="gf_${f.k}" class="btn" value="${_esc(val)}" placeholder="${_esc(f.label)}" style="flex:1;text-align:left;min-width:160px"/>`;
  }).join('');
}
function _goldRead(type) {
  const gold = {};
  for (const f of _GOLD_FIELDS[type]) {
    const el = document.getElementById('gf_'+f.k);
    const raw = el ? el.value : '';
    gold[f.k] = f.list ? raw.split(/[,，]\s*/).map(s=>s.trim()).filter(Boolean) : raw.trim();
  }
  return gold;
}

function goldFormOpen(pid) {
  const ps = window._goldProblems || [];
  const p = pid ? ps.find(x=>x.id===pid) : null;
  const edit = !!p;
  window._goldEditId = edit ? pid : null;
  const type = p ? p.type : 'code_retrieval';
  const tf = _TEXT_FIELD[type]||'query';
  $('#goldForm').innerHTML = `
    <div style="border:1.5px solid var(--ink);background:#fff;padding:18px 20px;margin-bottom:16px">
      <div class="mono" style="font-size:10px;color:var(--accent);letter-spacing:1px;margin-bottom:10px">${edit?'✎ 编辑 '+_esc(pid):'+ 新增题目'}</div>
      <div style="display:flex;gap:8px;flex-wrap:wrap;align-items:center">
        <label class="mono" style="font-size:10px;color:var(--ink2);width:50px">type</label>
        <select id="gfType" class="btn" ${edit?'disabled':''} onchange="goldFormRerender()">${_TYPES.map(t=>`<option value="${t}" ${t===type?'selected':''}>${t}</option>`).join('')}</select>
      </div>
      <div style="display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin-top:10px">
        <label class="mono" style="font-size:10px;color:var(--ink2);width:50px">${tf}</label>
        <input id="gfText" class="btn" value="${_esc(p?_goldText(p):'')}" placeholder="${tf==='fact'?'候选事实':'自然语言查询'}" style="flex:1;text-align:left;min-width:240px"/>
      </div>
      <div id="gfGold" style="display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin-top:10px">
        <label class="mono" style="font-size:10px;color:var(--ink2);width:50px">gold</label>${_goldFieldsHTML(type, p?p.gold:null)}
      </div>
      <div style="display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin-top:10px">
        <label class="mono" style="font-size:10px;color:var(--ink2);width:50px">tags</label>
        <input id="gfTags" class="btn" value="${_esc((p&&p.tags||[]).join(', '))}" placeholder="逗号分隔，如 concept_query, known_weak_probe" style="flex:1;text-align:left;min-width:200px"/>
        <label class="mono" style="font-size:10px;color:var(--ink2)">status</label>
        <select id="gfStatus" class="btn"><option ${(!p||p.status==='accepted')?'selected':''}>accepted</option><option ${(p&&p.status==='pending')?'selected':''}>pending</option></select>
      </div>
      <div style="margin-top:14px">
        <button class="btn fill" onclick="goldSave()">💾 保存</button>
        <button class="btn" onclick="$('#goldForm').innerHTML=''">取消</button>
        <span id="gfErr" style="color:var(--bad);font-size:11px;margin-left:12px"></span>
      </div>
    </div>`;
  $('#goldForm').scrollIntoView({behavior:'smooth'});
}
function goldFormRerender() {
  // type 变了 → 重渲染 gold 字段 + text label（保留已输入的 text/tags/status）
  const type = $('#gfType').value;
  $('#gfGold').innerHTML = `<label class="mono" style="font-size:10px;color:var(--ink2);width:50px">gold</label>${_goldFieldsHTML(type, null)}`;
  // text label 跟着 type
}

async function goldSave() {
  const tgt = window._goldTarget;
  const type = $('#gfType').value;
  const tf = _TEXT_FIELD[type]||'query';
  const problem = {
    type,
    [tf]: $('#gfText').value.trim(),
    gold: _goldRead(type),
    status: $('#gfStatus').value,
    tags: $('#gfTags').value.split(/[,，]\s*/).map(s=>s.trim()).filter(Boolean),
  };
  if (!problem[tf]) { $('#gfErr').textContent = `${tf} 不能空`; return; }
  const editId = window._goldEditId;
  const url = `/api/gold/${encodeURIComponent(tgt)}` + (editId?`/${encodeURIComponent(editId)}`:'');
  const method = editId ? 'PUT' : 'POST';
  const r = await fetch(url, {method, headers:{'Content-Type':'application/json'}, body: JSON.stringify(problem)});
  const o = await r.json();
  if (!r.ok || o.error) { $('#gfErr').textContent = o.error || `HTTP ${r.status}`; return; }
  $('#goldForm').innerHTML = '';
  $('#goldDirty').style.display = '';
  await goldRender();
}

async function goldDelete(pid) {
  if (!confirm(`确定删 ${pid}？`)) return;
  const tgt = window._goldTarget;
  const r = await fetch(`/api/gold/${encodeURIComponent(tgt)}/${encodeURIComponent(pid)}`, {method:'DELETE'});
  const o = await r.json();
  if (!r.ok || o.error) { alert(o.error || `HTTP ${r.status}`); return; }
  $('#goldDirty').style.display = '';
  await goldRender();
}

async function goldApprove(pid) {
  // pending → accepted（PUT 仅改 status）
  const tgt = window._goldTarget;
  const p = (window._goldProblems||[]).find(x=>x.id===pid);
  if (!p) return;
  const upd = Object.assign({}, p, {status:'accepted'});
  delete upd.verdict; delete upd.reason;  // approve 后清掉验收标记（可选）
  const r = await fetch(`/api/gold/${encodeURIComponent(tgt)}/${encodeURIComponent(pid)}`, {method:'PUT', headers:{'Content-Type':'application/json'}, body: JSON.stringify(upd)});
  const o = await r.json();
  if (!r.ok || o.error) { alert(o.error || `HTTP ${r.status}`); return; }
  $('#goldDirty').style.display = '';
  await goldRender();
}

async function goldGen() {
  $('#goldOut').textContent = 'running…（codegraph + GLM，~10s）';
  const seeds = ($('#glSeeds').value||'').split(/\s+/).filter(Boolean);
  if (!seeds.length) { $('#goldOut').textContent = '⚠ 先填 seed 词'; return; }
  const r = await fetch('/api/goldgen', {method:'POST', headers:{'Content-Type':'application/json'},
    body: JSON.stringify({seeds, target: window._goldTarget})});
  const o = await r.json();
  $('#goldOut').innerHTML = `<b style="color:${o.rc===0?'var(--good)':'var(--bad)'}">exit ${o.rc}</b> ${(o.stdout||'').slice(-300)}`;
  $('#goldDirty').style.display = '';
  await goldRender();
}
async function goldVerify() {
  $('#goldOut').textContent = 'verifying…';
  const r = await fetch('/api/goldgen-verify', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({target: window._goldTarget})});
  const o = await r.json();
  $('#goldOut').innerHTML = `<b style="color:${o.rc===0?'var(--good)':'var(--bad)'}">verify exit ${o.rc}</b> ${(o.stdout||'').slice(-300)}`;
  await goldRender();
}


// ── router ──
// ── 工程实践（独立分页）──
async function practicesView() {
  const data = await fetchJSON("/api/catalog?project=" + encodeURIComponent(window._targetProject || "/Users/ks_128/Documents/engineer_demo"));
  const ep = data.categories.find(c => c.id === "engineering-practices");
  if (!ep) { view().innerHTML = `<div class="loading">未找到工程实践分类</div>`; return; }
  view().innerHTML = `
    <h1>工程实践 <em>· Engineering</em></h1>
    <p class="lede">Context / Prompt / Harness 三层工程最佳实践 + Lint 反馈循环。来自 Claude Code 官方文档。</p>
    ${ep.capabilities.map(cap => `
      <div style="border:1.5px solid var(--ink);background:#fff;padding:22px 24px;margin-bottom:16px">
        <div style="display:flex;align-items:baseline;gap:10px;margin-bottom:6px">
          <h3 style="font-family:Fraunces,serif;font-size:20px;font-weight:600">${cap.name}</h3>
          <span style="font-size:9px;color:var(--ink2)">[${cap.type}]</span>
          ${cap.recommendation === "推荐" ? `<span style="color:var(--accent);font-size:10px;font-weight:600">推荐</span>` : `<span style="color:var(--ink2);font-size:10px">可选</span>`}
        </div>
        <p style="font-size:13px;color:var(--ink);margin-bottom:8px">${cap.desc}</p>
        ${cap.value ? `<p style="font-size:12px;color:var(--good);margin-bottom:10px">📊 ${cap.value}</p>` : ""}
        ${cap.guide ? `<details style="margin-top:8px"><summary style="font-size:11px;color:var(--ink2);cursor:pointer">📖 使用指南</summary><div style="font-size:12px;color:var(--ink);padding:8px 0 2px;line-height:1.6">${cap.guide}</div></details>` : ""}
        ${(cap.docs||[]).length ? `<div style="margin-top:8px">${cap.docs.map(d => `<a href="${d.url}" target="_blank" style="font-size:11px;margin-right:12px;text-decoration:underline">🔗 ${d.title}</a>`).join("")}</div>` : ""}
        ${cap.source ? `<div style="margin-top:4px"><a href="${cap.source}" target="_blank" style="font-size:10px;color:var(--ink2);text-decoration:underline">📦 ${cap.source.replace('https://github.com/','github.com/')}</a></div>` : ""}
      </div>`).join("")}
    <p class="lede" style="margin-top:20px">三层演进：Prompt Engineering（告诉模型做什么）→ Context Engineering（管理模型知道什么）→ Harness Engineering（管控模型怎么干活）。</p>`;
}

// ── router ──
const routes = {
  dashboard, catalog: catalogView, run: runConsole, reports, setup: setupView,
  onboard: onboardView, compare, goldlab: goldlabView, practices: practicesView,
};
async function router() {
  const h = location.hash.slice(2) || "dashboard";
  const [route, arg] = h.split("/");
  document.querySelectorAll(".nav a").forEach(a => a.classList.toggle("active", a.dataset.route === route));
  view().innerHTML = `<div class="loading">loading…</div>`;
  try {
    if (route === "report") await reportDetail(arg);
    else await (routes[route] || dashboard)();
  } catch (e) { view().innerHTML = `<div class="loading">⚠ ${e}</div>`; }
}
window.addEventListener("hashchange", router);
router();

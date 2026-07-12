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

    const tabs = data.categories.map((cat, i) => {
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
          </td>
          <td style="text-align:right;width:140px;white-space:nowrap">
            ${cap.installed
              ? `<span class="st ok" style="font-size:11px;margin-right:6px">✓ 已装</span><button class="btn" style="font-size:10px;padding:4px 10px;color:var(--bad)" onclick="toggleCap('${cap.id}','${cap.name}')">卸载</button>`
              : `<button class="btn fill" style="font-size:10px;padding:4px 12px" onclick="toggleCap('${cap.id}','${cap.name}')">安装</button>`}
          </td>
        </tr>`).join("")}
      </table>`;
  };
  window.switchCat = (i) => {
    document.querySelectorAll(".ctab").forEach((t, j) => t.classList.toggle("active", j === i));
    window.renderCat(i);
  };
  window.toggleCap = async (capId, capName) => {
    const cap = window._catData.categories.flatMap(c => c.capabilities).find(c => c.id === capId);
    if (!cap) return;
    if (cap.installed) {
      // 卸载（MVP：标记为卸载，实际卸载逻辑后续）
      alert(`卸载 ${capName}？\n\nMVP demo：实际卸载逻辑（删 skill 目录 / remove MCP / 删索引）后续实现。`);
    } else {
      // 安装
      const r = await fetch("/api/install", {method:"POST", headers:{"Content-Type":"application/json"},
        body: JSON.stringify({id: capId, project: window._targetProject})});
      const o = await r.json();
      const ok = o.rc === 0;
      alert(`${ok?"✓":"⚠"} ${capName} ${ok?"安装成功":"安装失败"}\n\n${(o.stdout||o.error||"").slice(0, 300)}`);
      if (ok) window.loadCatalogFor();  // 刷新状态
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
      <select id="rcSubj" class="btn">
        <option value="code">code（代码检索）</option>
        <option value="memory">memory（记忆召回+路由）</option>
        <option value="ab">ab（Stage0 token 代理）</option>
        <option value="doc-ragas">doc-ragas（答案质量）</option>
      </select>
      <label class="mono" style="font-size:10px;color:var(--ink2)">target</label>
      <input id="rcTarget" class="btn" value="godot" style="width:80px"/>
      <label class="mono" style="font-size:10px;color:var(--ink2)">method</label>
      <select id="rcMethod" class="btn"><option>bm25</option><option>grep</option><option>semantic</option></select>
      <button class="btn fill" onclick="doRun()">跑 ▸</button>
    </div>
    <div id="rcOut" class="mono" style="background:#fff;border:1px solid var(--rule);padding:16px;font-size:11px;white-space:pre-wrap;min-height:80px;color:var(--ink2)">选参数点"跑"——结果这里出。</div>`;
  window.doRun = async () => {
    $("#rcOut").textContent = "running…（后端 subprocess 调 eval.cli，可能要几十秒）";
    try {
      const r = await fetch("/api/run", {method: "POST", headers: {"Content-Type": "application/json"},
        body: JSON.stringify({subject: $("#rcSubj").value, target: $("#rcTarget").value, method: $("#rcMethod").value})});
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
function goldlabView() {
  view().innerHTML = `
    <h1>gold lab <em>· 扩题</em></h1>
    <p class="lede">agent 挖符号 + LLM 拟题 → 实证验收 → 人审 → fold 入 gold。gold 构造即正确（零 judge）。</p>
    <div style="border:1.5px solid var(--ink);background:#fff;padding:20px;margin-bottom:16px">
      <label class="mono" style="font-size:10px;color:var(--ink2)">seed 词（空格分，指一片代码）</label>
      <div style="display:flex;gap:8px;margin:6px 0 10px">
        <input id="gl_seeds" class="btn" placeholder="Vector color Node Resource" style="flex:1;text-align:left"/>
        <input id="gl_target" class="btn" value="gen" style="width:70px"/>
        <button class="btn fill" onclick="glGen()">① 挖+拟题 ▸</button>
      </div>
      <div class="mono" style="font-size:11px;color:var(--ink2)">→ codegraph 枚举真实符号 + GLM 拟 NL 题 → 写 gold_pending</div>
      <div id="gl_out_gen" class="mono" style="margin-top:10px;font-size:11px;min-height:14px"></div>
    </div>
    <div style="display:flex;gap:8px;margin-bottom:16px">
      <button class="btn" onclick="glVerify()">② 实证验收</button>
      <button class="btn" onclick="glShow()">③ 看候选（人审）</button>
      <button class="btn fill" onclick="glFold()">④ fold 入库 ▸</button>
    </div>
    <div id="gl_pending" class="mono" style="background:#fff;border:1px solid var(--rule);padding:16px;font-size:11px;white-space:pre-wrap;min-height:60px;color:var(--ink2)">候选队列（gold_pending）显示在这里——人审后 fold。</div>`;
  const tgt = () => $("#gl_target").value;
  window.glGen = async () => {
    $("#gl_out_gen").textContent = "running…（codegraph + GLM，~10s）";
    const seeds = $("#gl_seeds").value.split(/\s+/).filter(Boolean);
    const r = await fetch("/api/goldgen", {method:"POST", headers:{"Content-Type":"application/json"},
      body: JSON.stringify({seeds, target: tgt()})});
    const o = await r.json();
    $("#gl_out_gen").innerHTML = `<b style="color:${o.rc===0?"var(--good)":"var(--bad)"}">exit ${o.rc}</b> ${(o.stdout||"").slice(-400)}`;
  };
  window.glVerify = async () => {
    const r = await fetch("/api/goldgen-verify", {method:"POST", headers:{"Content-Type":"application/json"}, body: JSON.stringify({target: tgt()})});
    const o = await r.json(); glShow();
    $("#gl_out_gen").innerHTML = `<b>verify exit ${o.rc}</b>`;
  };
  window.glShow = async () => {
    const d = await fetchJSON("/api/pending/" + tgt());
    $("#gl_pending").textContent = d.exists ? d.content : "(无 pending——先 ① 挖+拟题)";
  };
  window.glFold = async () => {
    const r = await fetch("/api/goldgen-fold", {method:"POST", headers:{"Content-Type":"application/json"}, body: JSON.stringify({target: tgt()})});
    const o = await r.json();
    $("#gl_pending").innerHTML = `<b style="color:var(--good)">${(o.stdout||"").slice(-200)}</b>`;
  };
  glShow();
}

// ── router ──
const routes = {
  dashboard, catalog: catalogView, run: runConsole, reports, setup: setupView,
  onboard: onboardView, compare, goldlab: goldlabView,
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

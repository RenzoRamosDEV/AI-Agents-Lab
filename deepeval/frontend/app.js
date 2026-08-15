const HISTORY_URL = "../out/history/";
const THRESHOLD = 0.5;

// Familias de métricas de la suite actual, descubiertas de los propios resultados
let FAMILIES = [];
const FAMILY_LABELS = { rubric: "Rubric del caso", "reglas-globales": "Reglas globales" };
const familyLabel = (key) => FAMILY_LABELS[key] ?? key;

let suitesIndex = {}; // {suite: [ficheros de run]}
let currentSuite = null;
let runs = []; // [{file, date, label, data}] de más viejo a más nuevo
let selectedIndex = -1;
let chartMode = "familias"; // familias | casos
let chartView = "grafico"; // grafico | tabla
let compareIndex = -1; // run contra el que se comparan las respuestas (-1 = ninguno)
let searchText = "";
let onlyFails = false;
const hiddenSeries = new Set(); // claves "modo:serie" ocultas desde la leyenda

const $ = (id) => document.getElementById(id);
const fmt = (n, dec = 2) =>
  n == null ? "—" : n.toLocaleString("es-ES", { minimumFractionDigits: dec, maximumFractionDigits: dec });
const css = (v) => getComputedStyle(document.documentElement).getPropertyValue(v).trim();
const seriesColor = (i) => css(`--series-${Math.min(i + 1, 8)}`);

function metricFamily(name) {
  const clean = name.replace(/\s*\[GEval\]\s*$/, "");
  return clean.startsWith("rubric-") ? "rubric" : clean;
}

function computeFamilies() {
  const keys = [];
  for (const run of runs)
    for (const tc of run.data.testCases)
      for (const m of tc.metricsData || []) {
        const k = metricFamily(m.name);
        if (!keys.includes(k)) keys.push(k);
      }
  FAMILIES = keys.map((k) => ({ key: k, label: familyLabel(k) }));
}

function caseName(tc) {
  const m = tc.name.match(/\[(.+)\]/);
  return m ? m[1] : tc.name;
}

const isCanary = (tc) => caseName(tc).includes("canario");
// Un caso falla si cualquiera de sus métricas suspende
const caseOk = (tc) => tc.success && !(tc.metricsData || []).some((m) => !m.success);
const promptOf = (run) => run.data.hyperparameters?.["Plantilla del prompt"] ?? null;

function promptChangedAt(i) {
  if (i <= 0) return false;
  const cur = promptOf(runs[i]);
  const prev = promptOf(runs[i - 1]);
  return cur != null && prev != null && cur !== prev;
}

function matchesFilter(tc) {
  if (onlyFails && caseOk(tc)) return false;
  if (!searchText) return true;
  const q = searchText.toLowerCase();
  return [caseName(tc), tc.input, tc.actualOutput, ...(tc.metricsData || []).map((m) => m.reason || "")]
    .join("\n")
    .toLowerCase()
    .includes(q);
}

// Diff a nivel de palabra (LCS) entre dos textos: [{type: eq|del|ins, text}]
function diffWords(a, b) {
  const A = a.split(/(\s+)/).filter((t) => t !== "");
  const B = b.split(/(\s+)/).filter((t) => t !== "");
  const n = A.length, m = B.length;
  const dp = Array.from({ length: n + 1 }, () => new Uint16Array(m + 1));
  for (let i = n - 1; i >= 0; i--)
    for (let j = m - 1; j >= 0; j--)
      dp[i][j] = A[i] === B[j] ? dp[i + 1][j + 1] + 1 : Math.max(dp[i + 1][j], dp[i][j + 1]);
  const parts = [];
  const push = (type, text) => {
    const last = parts[parts.length - 1];
    if (last && last.type === type) last.text += text;
    else parts.push({ type, text });
  };
  let i = 0, j = 0;
  while (i < n && j < m) {
    if (A[i] === B[j]) { push("eq", A[i]); i++; j++; }
    else if (dp[i + 1][j] >= dp[i][j + 1]) { push("del", A[i]); i++; }
    else { push("ins", B[j]); j++; }
  }
  while (i < n) { push("del", A[i]); i++; }
  while (j < m) { push("ins", B[j]); j++; }
  return parts;
}

function parseRunDate(file) {
  const m = file.match(/run-(\d{4})(\d{2})(\d{2})-(\d{2})(\d{2})(\d{2})/);
  if (!m) return { date: null, label: file };
  const [, y, mo, d, h, mi, s] = m;
  return { date: new Date(`${y}-${mo}-${d}T${h}:${mi}:${s}`), label: `${d}/${mo} ${h}:${mi}` };
}

// Nota media por familia de métrica, excluyendo el canario (diseñado para fallar)
function familyAverages(data) {
  const sums = {}, counts = {};
  for (const tc of data.testCases) {
    if (isCanary(tc)) continue;
    for (const m of tc.metricsData || []) {
      if (typeof m.score !== "number") continue;
      const fam = metricFamily(m.name);
      sums[fam] = (sums[fam] || 0) + m.score;
      counts[fam] = (counts[fam] || 0) + 1;
    }
  }
  const avg = {};
  for (const fam of Object.keys(sums)) avg[fam] = sums[fam] / counts[fam];
  return avg;
}

// Nota media de un caso (todas sus métricas) en un run
function caseAverage(data, name) {
  const tc = data.testCases.find((t) => caseName(t) === name);
  if (!tc) return null;
  const scores = (tc.metricsData || []).map((m) => m.score).filter((s) => typeof s === "number");
  return scores.length ? scores.reduce((a, b) => a + b, 0) / scores.length : null;
}

// Series del gráfico según el modo: [{key, label, color, points: [{i, v}]}]
function chartSeries() {
  if (chartMode === "familias") {
    const avgs = runs.map((r) => familyAverages(r.data));
    return FAMILIES.slice(0, 8).map((fam, k) => ({
      key: fam.key,
      label: fam.label,
      color: seriesColor(k),
      points: avgs.map((a, i) => ({ i, v: a[fam.key] })).filter((p) => typeof p.v === "number"),
    }));
  }
  const names = [];
  for (const run of runs)
    for (const tc of run.data.testCases)
      if (!names.includes(caseName(tc))) names.push(caseName(tc));
  return names.slice(0, 8).map((name, k) => ({
    key: name,
    label: name,
    color: seriesColor(k),
    points: runs.map((r, i) => ({ i, v: caseAverage(r.data, name) })).filter((p) => typeof p.v === "number"),
  }));
}

const visibleSeries = () => chartSeries().filter((s) => !hiddenSeries.has(chartMode + ":" + s.key));

async function loadHistory() {
  let idx;
  try {
    idx = await (await fetch(HISTORY_URL + "index.json", { cache: "no-store" })).json();
  } catch {
    showEmpty("No se pudo leer el historial. Sirve esta página con <code>script/deepeval/view_deepeval.sh</code> (un HTML abierto a pelo no puede leer los JSON).");
    return;
  }
  suitesIndex = Array.isArray(idx) ? { mail_agent: idx } : idx;
  const names = Object.keys(suitesIndex);
  if (!names.length) {
    showEmpty(null);
    return;
  }
  if (!currentSuite || !suitesIndex[currentSuite]) currentSuite = names[0];
  renderSuiteBar();
  await loadSuite();
}

function renderSuiteBar() {
  const bar = $("suite-bar");
  bar.innerHTML = "";
  for (const name of Object.keys(suitesIndex)) {
    const btn = document.createElement("button");
    btn.textContent = name;
    btn.className = name === currentSuite ? "active" : "";
    btn.onclick = async () => {
      if (currentSuite === name) return;
      currentSuite = name;
      renderSuiteBar();
      await loadSuite();
    };
    bar.appendChild(btn);
  }
}

async function loadSuite() {
  const files = suitesIndex[currentSuite] || [];
  const loaded = await Promise.all(
    files.map(async (file) => {
      const raw = await (await fetch(`${HISTORY_URL}${currentSuite}/${file}`, { cache: "no-store" })).json();
      return { file, ...parseRunDate(file), data: raw.testRunData };
    })
  );
  runs = loaded.filter((r) => r.data && r.data.testCases);
  runs.sort((a, b) => a.file.localeCompare(b.file));
  computeFamilies();
  selectedIndex = runs.length - 1;
  compareIndex = -1;
  hiddenSeries.clear();
  renderCasesHead();
  if (!runs.length) {
    showEmpty(null);
    return;
  }
  $("empty-state").classList.add("hidden");
  render();
}

function renderCasesHead() {
  $("cases-head").innerHTML =
    `<th>Caso</th><th>Estado</th>` + FAMILIES.map((f) => `<th>${f.label}</th>`).join("");
}

function showEmpty(html) {
  const el = $("empty-state");
  el.classList.remove("hidden");
  if (html) el.innerHTML = `<p>${html}</p>`;
}

function render() {
  renderSidebar();
  renderHistoryStats();
  renderChart();
  renderRun();
}

function renderHistoryStats() {
  const total = runs.reduce((a, r) => a + (r.data.evaluationCost || 0), 0);
  $("history-stats").textContent = `${runs.length} runs · coste juez acumulado: ${fmt(total, 3)} $`;
}

function renderSidebar() {
  const ul = $("run-list");
  ul.innerHTML = "";
  [...runs].reverse().forEach((run, i) => {
    const idx = runs.length - 1 - i;
    const li = document.createElement("li");
    li.className = idx === selectedIndex ? "active" : "";
    const passed = run.data.testPassed ?? 0;
    const failed = run.data.testFailed ?? 0;
    li.innerHTML = `
      <div class="run-date">${run.label}${promptChangedAt(idx) ? '<span class="badge">prompt cambiado</span>' : ""}</div>
      <div class="run-meta">${passed}/${passed + failed} casos · ${fmt(run.data.evaluationCost, 3)} $</div>`;
    li.onclick = () => { selectedIndex = idx; render(); };
    ul.appendChild(li);
  });
}

// ---------- Detalle del run ----------

function prevScores() {
  const prev = runs[selectedIndex - 1];
  if (!prev) return null;
  const map = {};
  for (const tc of prev.data.testCases)
    for (const m of tc.metricsData || [])
      map[caseName(tc) + "|" + metricFamily(m.name)] = m.score;
  return map;
}

function renderRun() {
  const card = $("run-card");
  const run = runs[selectedIndex];
  if (!run) return;
  card.classList.remove("hidden");
  $("run-title").textContent = `Run del ${run.label}`;

  const passed = run.data.testPassed ?? 0;
  const failed = run.data.testFailed ?? 0;
  const avgs = familyAverages(run.data);
  const mean = Object.values(avgs).length
    ? Object.values(avgs).reduce((a, b) => a + b, 0) / Object.values(avgs).length
    : null;
  const judge = run.data.testCases.flatMap((tc) => tc.metricsData || []).find((m) => m.evaluationModel)?.evaluationModel;
  $("run-tiles").innerHTML = `
    <div class="tile"><div class="tile-label">Casos OK</div><div class="tile-value">${passed}/${passed + failed}</div></div>
    <div class="tile"><div class="tile-label">Nota media</div><div class="tile-value">${fmt(mean)}</div></div>
    <div class="tile"><div class="tile-label">Coste juez</div><div class="tile-value">${fmt(run.data.evaluationCost, 3)} $</div></div>
    <div class="tile"><div class="tile-label">Duración</div><div class="tile-value">${fmt(run.data.runDuration, 0)} s</div></div>
    <div class="tile"><div class="tile-label">Juez</div><div class="tile-value">${judge ?? "—"}</div></div>`;

  const prev = prevScores();
  const tbody = $("cases-body");
  tbody.innerHTML = "";
  const cases = run.data.testCases.filter(matchesFilter);
  for (const tc of cases) {
    const tr = document.createElement("tr");
    tr.className = "case-row";
    const byFam = {};
    for (const m of tc.metricsData || []) byFam[metricFamily(m.name)] = m;
    const ok = caseOk(tc);
    tr.innerHTML = `
      <td><span class="case-name">${caseName(tc)}</span></td>
      <td><span class="status ${ok ? "ok" : "fail"}">${ok ? "✓ bien" : "✗ mal"}</span></td>
      ${FAMILIES.map((f) => `<td>${scoreCell(byFam[f.key], prev?.[caseName(tc) + "|" + f.key])}</td>`).join("")}`;
    tr.onclick = () => toggleDetail(tr, tc);
    tbody.appendChild(tr);
  }
  if (!cases.length) {
    const tr = document.createElement("tr");
    tr.innerHTML = `<td colspan="${2 + FAMILIES.length}" class="muted">Ningún caso coincide con el filtro.</td>`;
    tbody.appendChild(tr);
  }

  $("resp-card").classList.remove("hidden");
  $("config-card").classList.remove("hidden");
  renderCompareSelect();
  renderRespuestas(run);
  renderConfig(run);
}

function renderCompareSelect() {
  const sel = $("compare-select");
  sel.innerHTML = "";
  const none = document.createElement("option");
  none.value = "-1";
  none.textContent = "— nada —";
  sel.appendChild(none);
  runs.forEach((r, i) => {
    if (i === selectedIndex) return;
    const o = document.createElement("option");
    o.value = String(i);
    o.textContent = `run del ${r.label}`;
    sel.appendChild(o);
  });
  if (compareIndex === selectedIndex || compareIndex >= runs.length) compareIndex = -1;
  sel.value = String(compareIndex);
}

function renderRespuestas(run) {
  const wrap = $("tab-respuestas");
  wrap.innerHTML = "";
  const compareRun = compareIndex >= 0 && compareIndex !== selectedIndex ? runs[compareIndex] : null;
  const cases = run.data.testCases.filter(matchesFilter);
  if (compareRun) {
    const changed = run.data.testCases.filter((tc) => {
      const other = compareRun.data.testCases.find((t) => caseName(t) === caseName(tc));
      return other && other.actualOutput !== tc.actualOutput;
    }).length;
    const summary = document.createElement("p");
    summary.textContent =
      changed === 0
        ? `Ninguna de las ${run.data.testCases.length} respuestas cambió respecto al run del ${compareRun.label} (probablemente ambos runs usan las mismas respuestas cacheadas — regenera con --fresh).`
        : `${changed} de ${run.data.testCases.length} respuestas cambiaron respecto al run del ${compareRun.label} — tachado = antes, resaltado = ahora.`;
    summary.className = changed === 0 ? "muted" : "";
    wrap.appendChild(summary);
  }
  if (!cases.length) {
    const p = document.createElement("p");
    p.className = "muted";
    p.textContent = "Ningún caso coincide con el filtro.";
    wrap.appendChild(p);
    return;
  }
  for (const tc of cases) {
    const ok = caseOk(tc);
    const card = document.createElement("div");
    card.className = "resp-card";
    const head = document.createElement("div");
    head.className = "resp-head";
    head.innerHTML = `<span class="chev">▸</span><span class="case-name">${caseName(tc)}</span>
      <span class="status ${ok ? "ok" : "fail"}">${ok ? "✓ bien" : "✗ mal"}</span>`;

    const respBlock = document.createElement("div");
    respBlock.className = "detail-block";
    const h = document.createElement("h3");
    h.textContent = "Respuesta del agente";
    const pre = document.createElement("pre");
    const other = compareRun?.data.testCases.find((t) => caseName(t) === caseName(tc));
    if (other && other.actualOutput !== tc.actualOutput) {
      for (const part of diffWords(other.actualOutput || "", tc.actualOutput || "")) {
        const span = document.createElement("span");
        if (part.type === "ins") span.className = "diff-ins";
        else if (part.type === "del") span.className = "diff-del";
        span.textContent = part.text;
        pre.appendChild(span);
      }
    } else {
      pre.textContent = tc.actualOutput || "(vacío)";
    }
    respBlock.append(h, pre);
    applyClamp(respBlock, pre, tc.actualOutput);
    if (compareRun) {
      const note = document.createElement("div");
      note.className = "muted diff-note";
      note.textContent = !other
        ? `Este caso no existe en el run del ${compareRun.label}.`
        : other.actualOutput === tc.actualOutput
          ? `Sin cambios respecto al run del ${compareRun.label}.`
          : `Comparado con el run del ${compareRun.label}: tachado = antes, resaltado = ahora.`;
      respBlock.appendChild(note);
    }

    const grid = document.createElement("div");
    grid.className = "resp-grid";
    grid.append(block("Email entrante", tc.input), respBlock);
    const metrics = document.createElement("div");
    metrics.className = "resp-metrics muted";
    metrics.textContent = (tc.metricsData || [])
      .map((m) => `${m.name.replace(/\s*\[GEval\]\s*$/, "")}: ${fmt(m.score)}`)
      .join(" · ");

    // Plegado por defecto: la cabecera muestra caso + estado; clic para desplegar
    const body = document.createElement("div");
    body.className = "resp-body hidden";
    body.append(grid, metrics);
    head.onclick = () => {
      const abierto = !body.classList.toggle("hidden");
      head.querySelector(".chev").textContent = abierto ? "▾" : "▸";
    };
    card.append(head, body);
    wrap.appendChild(card);
  }
}

function renderConfig(run) {
  const wrap = $("tab-config");
  wrap.innerHTML = "";
  const hp = run.data.hyperparameters;
  let promptText = null;
  const rows = [];
  if (hp) {
    for (const [k, v] of Object.entries(hp)) {
      if (k === "Plantilla del prompt") { promptText = v; continue; }
      rows.push([k, v]);
    }
  }
  rows.push(["Casos en el run", String(run.data.testCases.length)]);
  rows.push(["Archivo del historial", "out/history/" + run.file]);

  const table = document.createElement("table");
  table.className = "config-table";
  for (const [k, v] of rows) {
    const tr = document.createElement("tr");
    const td1 = document.createElement("td");
    td1.textContent = k;
    const td2 = document.createElement("td");
    td2.textContent = v;
    tr.append(td1, td2);
    table.appendChild(tr);
  }
  wrap.appendChild(table);

  if (!hp) {
    const note = document.createElement("p");
    note.className = "muted";
    note.textContent = "Este run es anterior al registro de configuración: no guarda modelo evaluado, parámetros ni prompt. Los runs nuevos sí lo incluyen.";
    wrap.appendChild(note);
  }
  if (promptText) {
    const det = document.createElement("details");
    det.className = "prompt-details";
    const sum = document.createElement("summary");
    sum.textContent = "Ver la plantilla del prompt usada en este run";
    const pre = document.createElement("pre");
    pre.textContent = promptText;
    det.append(sum, pre);
    wrap.appendChild(det);
  }
}


function scoreCell(m, prevScore) {
  if (!m || typeof m.score !== "number") return '<span class="muted">—</span>';
  const icon = m.success ? "✓" : "✗";
  const cls = m.success ? "ok" : "fail";
  let delta = "";
  if (typeof prevScore === "number") {
    const d = m.score - prevScore;
    if (Math.abs(d) >= 0.005) {
      const up = d > 0;
      delta = `<span class="delta ${up ? "up" : "down"}" title="Respecto al run anterior">${up ? "▲" : "▼"}${fmt(Math.abs(d))}</span>`;
    }
  }
  return `<span class="status ${cls}">${icon}</span> ${fmt(m.score)}${delta}`;
}

function toggleDetail(tr, tc) {
  const next = tr.nextElementSibling;
  if (next && next.classList.contains("detail-row")) {
    next.remove();
    return;
  }
  document.querySelectorAll(".detail-row").forEach((el) => el.remove());
  const detail = document.createElement("tr");
  detail.className = "detail-row";
  const td = document.createElement("td");
  td.colSpan = 2 + FAMILIES.length;

  td.appendChild(block("Email entrante", tc.input));
  td.appendChild(block("Respuesta del agente", tc.actualOutput));

  const ctx = (tc.retrievalContext || [])[0];
  if (ctx) {
    const blockWrap = document.createElement("div");
    blockWrap.className = "detail-block";
    const det = document.createElement("details");
    det.className = "prompt-details";
    const sum = document.createElement("summary");
    sum.textContent = "Ver la plantilla que cargó el agente (load_skill)";
    const pre = document.createElement("pre");
    pre.textContent = ctx;
    det.append(sum, pre);
    blockWrap.appendChild(det);
    td.appendChild(blockWrap);
  }

  const metricsWrap = document.createElement("div");
  metricsWrap.className = "detail-block";
  metricsWrap.innerHTML = "<h3>Veredicto del juez por métrica</h3>";
  for (const m of tc.metricsData || []) {
    const card = document.createElement("div");
    card.className = "metric-card";
    const head = document.createElement("div");
    head.className = "metric-head";
    head.innerHTML = `<span class="metric-name">${m.name}</span><span class="metric-score">${scoreCell(m)} <span class="muted">(umbral ${fmt(m.threshold, 1)})</span></span>`;
    const reason = document.createElement("div");
    reason.className = "metric-reason";
    reason.textContent = m.reason || "(sin razonamiento)";
    const meta = document.createElement("div");
    meta.className = "metric-meta";
    meta.textContent =
      `Juez: ${m.evaluationModel ?? "—"} · Coste: ${fmt(m.evaluationCost, 4)} $` +
      ` · Tokens juez: ${m.inputTokenCount ?? "—"} entrada / ${m.outputTokenCount ?? "—"} salida`;
    card.append(head, reason, meta);
    if (m.verboseLogs) {
      const det = document.createElement("details");
      det.className = "prompt-details";
      const sum = document.createElement("summary");
      sum.textContent = "Análisis del juez paso a paso (afirmaciones y veredictos)";
      const pre = document.createElement("pre");
      pre.textContent = m.verboseLogs;
      det.append(sum, pre);
      card.appendChild(det);
    }
    metricsWrap.appendChild(card);
  }
  td.appendChild(metricsWrap);
  detail.appendChild(td);
  tr.after(detail);
}

function block(title, text) {
  const div = document.createElement("div");
  div.className = "detail-block";
  const h = document.createElement("h3");
  h.textContent = title;
  const pre = document.createElement("pre");
  pre.textContent = text || "(vacío)";
  div.append(h, pre);
  applyClamp(div, pre, text);
  return div;
}

// Textos largos: se recortan con un "Ver más" para que un caso no ocupe toda la página
const CLAMP_LINES = 14;
const CLAMP_CHARS = 900;

function applyClamp(container, pre, text) {
  if (!text || (text.split("\n").length <= CLAMP_LINES && text.length <= CLAMP_CHARS)) return;
  pre.classList.add("clamped");
  const btn = document.createElement("button");
  btn.className = "more-btn";
  btn.textContent = "Ver más ▾";
  btn.onclick = (ev) => {
    ev.stopPropagation();
    const nowClamped = pre.classList.toggle("clamped");
    btn.textContent = nowClamped ? "Ver más ▾" : "Ver menos ▴";
  };
  container.appendChild(btn);
}

// ---------- Gráfico de evolución (SVG a mano, tamaño real: el texto no escala) ----------

const NS = "http://www.w3.org/2000/svg";

function el(tag, attrs) {
  const node = document.createElementNS(NS, tag);
  for (const [k, v] of Object.entries(attrs)) node.setAttribute(k, v);
  return node;
}

function renderChart() {
  const card = $("chart-card");
  card.classList.remove("hidden");
  const wrap = $("chart");
  wrap.innerHTML = "";
  renderLegend();
  if (chartView === "tabla") {
    renderChartTable(wrap);
    return;
  }

  const series = visibleSeries();
  const W = Math.max(560, Math.min(wrap.clientWidth || 720, 1040));
  const H = 280;
  // Margen derecho según la etiqueta de final de línea más larga (fuente mono ≈ 7px/carácter)
  const CHAR_W = 7;
  const endTexts = series
    .filter((s) => s.points.length)
    .map((s) => `${s.label} ${fmt(s.points[s.points.length - 1].v)}`);
  const longest = Math.max(0, ...endTexts.map((t) => t.length));
  const M = {
    top: 14,
    right: Math.min(Math.max(120, longest * CHAR_W + 18), Math.floor(W * 0.38)),
    bottom: 30,
    left: 44,
  };
  const iw = W - M.left - M.right, ih = H - M.top - M.bottom;
  const svg = el("svg", { width: W, height: H, role: "img", "aria-label": "Evolución de la nota media en cada run" });

  const n = runs.length;
  const x = (i) => M.left + (n === 1 ? iw / 2 : (i / (n - 1)) * iw);
  const y = (v) => M.top + (1 - v) * ih;

  for (const t of [0, 0.25, 0.5, 0.75, 1]) {
    svg.appendChild(el("line", { x1: M.left, x2: M.left + iw, y1: y(t), y2: y(t), stroke: css("--grid"), "stroke-width": 1 }));
    const lbl = el("text", { x: M.left - 8, y: y(t) + 4, "text-anchor": "end", "font-size": 11, fill: css("--text-muted") });
    lbl.textContent = fmt(t, 2);
    svg.appendChild(lbl);
  }
  svg.appendChild(el("line", { x1: M.left, x2: M.left + iw, y1: y(THRESHOLD), y2: y(THRESHOLD), stroke: css("--axis"), "stroke-width": 1, "stroke-dasharray": "4 4" }));
  const thLbl = el("text", { x: M.left + 4, y: y(THRESHOLD) - 5, "font-size": 10.5, fill: css("--text-muted") });
  thLbl.textContent = "umbral";
  svg.appendChild(thLbl);
  svg.appendChild(el("line", { x1: M.left, x2: M.left + iw, y1: y(0), y2: y(0), stroke: css("--axis"), "stroke-width": 1 }));

  // Etiquetas del eje X: máximo 6, ancladas al run más reciente (las antiguas se saltan primero)
  const maxLabels = Math.min(6, Math.max(2, Math.floor(iw / 90)));
  const step = Math.max(1, Math.ceil(n / maxLabels));
  runs.forEach((run, i) => {
    if ((n - 1 - i) % step !== 0) return;
    // Las fechas de los extremos se anclan hacia dentro para no invadir el eje Y ni salirse
    const px = x(i);
    const halfLabel = (run.label.length * 6.5) / 2;
    let anchor = "middle";
    if (px - halfLabel < M.left) anchor = "start";
    else if (px + halfLabel > M.left + iw) anchor = "end";
    const lbl = el("text", { x: px, y: H - 8, "text-anchor": anchor, "font-size": 11, fill: css("--text-muted") });
    lbl.textContent = run.label;
    svg.appendChild(lbl);
  });

  // Marca vertical en los runs donde cambió la plantilla del prompt
  runs.forEach((run, i) => {
    if (!promptChangedAt(i)) return;
    svg.appendChild(el("line", { x1: x(i), x2: x(i), y1: M.top, y2: y(0), stroke: css("--text-muted"), "stroke-width": 1, "stroke-dasharray": "3 3" }));
    const lbl = el("text", { x: x(i) + 4, y: M.top + 9, "font-size": 10, fill: css("--text-muted") });
    lbl.textContent = "prompt cambiado";
    svg.appendChild(lbl);
  });

  // Posiciones de las etiquetas de final de línea, separadas para no solaparse
  const endLabels = series
    .filter((s) => s.points.length)
    .map((s) => ({ key: s.key, y: y(s.points[s.points.length - 1].v) }))
    .sort((a, b) => a.y - b.y);
  for (let k = 1; k < endLabels.length; k++) {
    if (endLabels[k].y - endLabels[k - 1].y < 15) endLabels[k].y = endLabels[k - 1].y + 15;
  }
  const labelY = Object.fromEntries(endLabels.map((l) => [l.key, l.y]));

  const tooltip = $("tooltip");
  for (const s of series) {
    if (!s.points.length) continue;
    if (s.points.length > 1) {
      const d = s.points.map((p, k) => `${k ? "L" : "M"}${x(p.i)},${y(p.v)}`).join(" ");
      svg.appendChild(el("path", { d, fill: "none", stroke: s.color, "stroke-width": 2, "stroke-linejoin": "round", "stroke-linecap": "round" }));
    }
    for (const p of s.points) {
      svg.appendChild(el("circle", { cx: x(p.i), cy: y(p.v), r: 4, fill: s.color, stroke: css("--surface-1"), "stroke-width": 2 }));
      const hit = el("circle", { cx: x(p.i), cy: y(p.v), r: 11, fill: "transparent" });
      hit.addEventListener("mousemove", (ev) => {
        const rows = series
          .map((sv) => ({ sv, pt: sv.points.find((q) => q.i === p.i) }))
          .filter((r) => r.pt)
          .sort((a, b) => b.pt.v - a.pt.v)
          .map((r) => `<div class="tt-row"><span class="swatch" style="background:${r.sv.color};width:9px;height:9px;border-radius:3px;display:inline-block"></span>${r.sv.label}: <strong>${fmt(r.pt.v)}</strong></div>`)
          .join("");
        tooltip.classList.remove("hidden");
        tooltip.innerHTML = `<div class="tt-title">${runs[p.i].label}</div>${rows}`;
        tooltip.style.left = Math.min(ev.clientX + 14, window.innerWidth - 300) + "px";
        tooltip.style.top = ev.clientY + 14 + "px";
      });
      hit.addEventListener("mouseleave", () => tooltip.classList.add("hidden"));
      svg.appendChild(hit);
    }
    // Etiqueta directa al final de la línea, del color de su serie
    const last = s.points[s.points.length - 1];
    const maxChars = Math.floor((M.right - 14) / CHAR_W);
    let txt = `${s.label} ${fmt(last.v)}`;
    if (txt.length > maxChars) txt = s.label.slice(0, Math.max(3, maxChars - 6)) + "… " + fmt(last.v);
    const lbl = el("text", { x: x(last.i) + 10, y: (labelY[s.key] ?? y(last.v)) + 4, "font-size": 11.5, fill: s.color });
    lbl.textContent = txt;
    svg.appendChild(lbl);
  }

  wrap.appendChild(svg);
}

function renderChartTable(wrap) {
  const series = visibleSeries();
  const table = document.createElement("table");
  table.className = "cases-table";
  table.innerHTML = `
    <thead><tr><th>Run</th>${series.map((s) => `<th>${s.label}</th>`).join("")}</tr></thead>
    <tbody>${runs
      .map((run, i) => `<tr><td class="case-name">${run.label}</td>${series
        .map((s) => {
          const pt = s.points.find((p) => p.i === i);
          return `<td>${pt ? fmt(pt.v) : "—"}</td>`;
        })
        .join("")}</tr>`)
      .join("")}</tbody>`;
  const scroller = document.createElement("div");
  scroller.className = "table-wrap";
  scroller.appendChild(table);
  wrap.appendChild(scroller);
}

function renderLegend() {
  const legend = $("chart-legend");
  legend.innerHTML = "";
  for (const s of chartSeries()) {
    const off = hiddenSeries.has(chartMode + ":" + s.key);
    const item = document.createElement("span");
    item.className = "legend-item" + (off ? " off" : "");
    item.innerHTML = `<span class="swatch" style="background:${s.color}"></span>${s.label}`;
    item.onclick = () => {
      const k = chartMode + ":" + s.key;
      hiddenSeries.has(k) ? hiddenSeries.delete(k) : hiddenSeries.add(k);
      renderChart();
    };
    legend.appendChild(item);
  }
}

// ---------- Controles ----------

$("mode-toggle").addEventListener("click", (ev) => {
  const btn = ev.target.closest("button");
  if (!btn) return;
  chartMode = btn.dataset.mode;
  document.querySelectorAll("#mode-toggle button").forEach((b) => b.classList.toggle("active", b === btn));
  renderChart();
});

$("view-toggle").addEventListener("click", (ev) => {
  const btn = ev.target.closest("button");
  if (!btn) return;
  chartView = btn.dataset.view;
  document.querySelectorAll("#view-toggle button").forEach((b) => b.classList.toggle("active", b === btn));
  renderChart();
});

$("case-search").addEventListener("input", (ev) => {
  searchText = ev.target.value.trim();
  renderRun();
});

$("only-fails").addEventListener("change", (ev) => {
  onlyFails = ev.target.checked;
  renderRun();
});

$("compare-select").addEventListener("change", (ev) => {
  compareIndex = parseInt(ev.target.value, 10);
  renderRespuestas(runs[selectedIndex]);
});

$("csv-btn").addEventListener("click", () => {
  const series = chartSeries();
  const lines = [["run", ...series.map((s) => s.label)].join(",")];
  runs.forEach((run, i) => {
    const row = [run.label, ...series.map((s) => {
      const pt = s.points.find((p) => p.i === i);
      return pt ? pt.v.toFixed(4) : "";
    })];
    lines.push(row.join(","));
  });
  const blob = new Blob([lines.join("\n")], { type: "text/csv;charset=utf-8" });
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = `eval-evolucion-${chartMode}.csv`;
  a.click();
  URL.revokeObjectURL(a.href);
});

// Estado inicial desde la URL (?mode=familias|casos&view=grafico|tabla&tab=casos|respuestas|config)
const params = new URLSearchParams(location.search);
if (["familias", "casos"].includes(params.get("mode"))) chartMode = params.get("mode");
if (["grafico", "tabla"].includes(params.get("view"))) chartView = params.get("view");
if (/^\d+$/.test(params.get("compare") ?? "")) compareIndex = parseInt(params.get("compare"), 10);
if (params.get("suite")) currentSuite = params.get("suite");
document.querySelectorAll("#mode-toggle button").forEach((b) => b.classList.toggle("active", b.dataset.mode === chartMode));
document.querySelectorAll("#view-toggle button").forEach((b) => b.classList.toggle("active", b.dataset.view === chartView));

$("docs-btn").addEventListener("click", () => $("soon-modal").classList.remove("hidden"));
$("soon-modal").addEventListener("click", () => $("soon-modal").classList.add("hidden"));

let resizeTimer;
window.addEventListener("resize", () => {
  clearTimeout(resizeTimer);
  resizeTimer = setTimeout(() => runs.length && renderChart(), 150);
});
window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", () => runs.length && render());

loadHistory();

// SHC Benchmarks — Nostr reader for GitHub Pages
// Fetches kind 30078 events tagged "benchmark" from Nostr relays, parses the
// benchmark JSON from the event content (or lazy-loads from Blossom), and
// renders raw data tables. Pure vanilla JS, no build step, no dependencies.
//
// Event contract (emitted by scripts/publish_benchmarks.py):
//
//   kind 30078 (parameterized replaceable, d-tag = run_id):
//     tags:
//       ["d", run_id]
//       ["t", "benchmark"]
//       ["file", blossom_url]          (optional — full JSON blob)
//       ["hostname", host]             (optional — display)
//     content: JSON string with full benchmark data:
//       {
//         "host": "66.92.204.238",
//         "started_at": "ISO-8601",
//         "completed_at": "ISO-8601",
//         "elapsed_seconds": 42.3,
//         "sysinfo": { "cpu_model", "cpu_count", "cpu_mhz", "nested_virt", ... },
//         "benchmarks": {
//           "cpu": { "sysbench_st_eps", "sysbench_mt_eps", "openssl_...", ... },
//           "memory": { "read_mib_per_s", "ops_per_s", ... },
//           "disk": { "sequential_read": {bw,iops,lat}, "random_4k_read": {...}, ... },
//           "network": { "download_mbps", "ipinfo": {city,country,org}, ... }
//         },
//         "pricing": { "daily_price", "source_api", "fetched_at", ... }
//       }

// === CONFIGURATION ==========================================================

const RELAYS = [
  "wss://relay.cashu.email",
  "wss://relay.damus.io",
];
const FETCH_TIMEOUT_MS = 15000;
const FETCH_SINCE_DAYS = 180;
const CACHE_KEY = "shc:benchmarks:v1";

// === STATE ==================================================================

let allRuns = [];
let selectedRunId = null;
let liveSocket = null;       // kept open for real-time updates
let detailLoadId = 0;        // guards against stale lazy-load renders
const filterState = { search: "", sort: "newest" };

// ===========================================================================
// WebSocket: Fetch kind 30078 events tagged "benchmark" from multiple relays
// ===========================================================================

function fetchBenchmarkEvents() {
  return new Promise((resolve) => {
    const events = new Map(); // dedup by event id
    let resolved = false;
    let closedRelays = 0;
    let connectedCount = 0;

    const timeout = setTimeout(() => {
      if (!resolved) {
        resolved = true;
        resolve({ events: [...events.values()], connected: connectedCount });
      }
    }, FETCH_TIMEOUT_MS);

    RELAYS.forEach((relayUrl, index) => {
      let ws;
      try {
        ws = new WebSocket(relayUrl);
      } catch (e) {
        closedRelays++;
        checkDone();
        return;
      }

      const subId = "shc-bench-" + Math.random().toString(36).slice(2, 8);

      ws.onopen = () => {
        connectedCount++;
        ws.send(JSON.stringify([
          "REQ", subId,
          {
            "#t": "benchmark",
            kinds: [30078],
            limit: 200,
            since: Math.floor(Date.now() / 1000) - 86400 * FETCH_SINCE_DAYS,
          },
        ]));
        updateConnectionStatus(connectedCount, RELAYS.length);

        // Keep the first relay open for real-time updates.
        if (index === 0 && !liveSocket) {
          liveSocket = ws;
        }
      };

      ws.onmessage = (msg) => {
        try {
          const data = JSON.parse(msg.data);
          if (data[0] === "EVENT" && data[1] === subId && data[2]) {
            const evt = data[2];
            const wasNew = !events.has(evt.id);
            events.set(evt.id, evt);

            // Real-time: if this is a live event after initial load, update UI.
            if (resolved && wasNew) {
              handleLiveEvent(evt);
            }
          } else if (data[0] === "EOSE" && data[1] === subId) {
            // Don't close the live relay — keep it for auto-refresh.
            if (ws !== liveSocket) {
              ws.send(JSON.stringify(["CLOSE", subId]));
              ws.close();
            } else {
              // On the live relay, switch to a minimal subscription for new events.
              ws.send(JSON.stringify(["CLOSE", subId]));
            }
            closedRelays++;
            checkDone();
          }
        } catch (e) { /* ignore parse errors */ }
      };

      ws.onerror = () => {
        closedRelays++;
        checkDone();
      };

      ws.onclose = () => {
        if (ws !== liveSocket) {
          closedRelays++;
          checkDone();
        }
      };
    });

    function checkDone() {
      if (closedRelays >= RELAYS.length && !resolved) {
        clearTimeout(timeout);
        resolved = true;
        resolve({ events: [...events.values()], connected: connectedCount });
      }
    }
  });
}

// Handle a new event arriving in real-time after initial load.
function handleLiveEvent(evt) {
  if (evt.kind !== 30078) return;
  const parsed = parseRunFromEvent(evt);
  if (!parsed) return;

  // Replace if same run_id exists, otherwise add.
  const idx = allRuns.findIndex((r) => r.runId === parsed.runId);
  if (idx >= 0) {
    allRuns[idx] = parsed;
  } else {
    allRuns.unshift(parsed);
    sortRuns();
  }

  renderRunsList();

  // If the new run is currently selected, re-render detail.
  if (selectedRunId === parsed.runId) {
    renderDetail(parsed);
  }
}

// ===========================================================================
// Parsing helpers
// ===========================================================================

function getTag(tags, name) {
  const t = (tags || []).find((tg) => tg[0] === name);
  return t ? t[1] : null;
}

function getTagAll(tags, name) {
  return (tags || []).filter((tg) => tg[0] === name).map((tg) => tg[1]);
}

// Parse a kind 30078 event into a run object.
// Content should be JSON with full benchmark data. If parsing fails or the
// content is a summary, we mark it for lazy-load from Blossom.
function parseRunFromEvent(event) {
  const tags = event.tags || [];
  const runId = getTag(tags, "d") || event.id;
  const blossomUrl = getTag(tags, "file");
  const hostnameTag = getTag(tags, "hostname");

  let payload = null;
  let needsLazyLoad = false;

  try {
    payload = JSON.parse(event.content || "{}");
    // If content has no benchmarks key, it might be a summary — lazy load.
    if (!payload.benchmarks && blossomUrl) {
      needsLazyLoad = true;
    }
  } catch (e) {
    // Content is not valid JSON — try lazy loading from Blossom.
    if (blossomUrl) needsLazyLoad = true;
  }

  const sysinfo = (payload && payload.sysinfo) ? payload.sysinfo : {};
  const benchmarks = (payload && payload.benchmarks) ? payload.benchmarks : {};
  const pricing = (payload && payload.pricing) ? payload.pricing : null;
  const network = benchmarks.network || {};
  const ipinfo = network.ipinfo || {};

  // Determine display provider from pricing or hostname.
  let provider = "?";
  if (pricing && pricing.provider) {
    provider = pricing.provider;
  } else if (hostnameTag) {
    provider = hostnameTag;
  }

  const displayHost = hostnameTag || payload?.host || ipinfo.ip || "?";
  const location = [ipinfo.city, ipinfo.country].filter(Boolean).join(", ") || "";
  const isp = ipinfo.org || "";

  return {
    id: event.id,
    eventId: event.id,
    runId,
    timestamp: event.created_at,
    pubkey: event.pubkey,
    blossomUrl,
    host: displayHost,
    provider,
    location,
    isp,
    nestedVirt: sysinfo.nested_virt,
    cpuModel: sysinfo.cpu_model || "",
    cpuCount: sysinfo.cpu_count,
    payload,         // full parsed JSON (may be null if lazy-load needed)
    needsLazyLoad,
    pricing,
    benchmarks,
    sysinfo,
    rawEvent: event,
  };
}

// Deduplicate runs by run_id (d-tag), keeping the latest event per run.
function dedupeRuns(events) {
  const parsed = events
    .map((evt) => {
      try {
        return parseRunFromEvent(evt);
      } catch (e) {
        console.warn("[SHC] Failed to parse event", evt.id, e);
        return null;
      }
    })
    .filter(Boolean);

  const byRunId = new Map();
  for (const run of parsed) {
    const existing = byRunId.get(run.runId);
    if (!existing || run.timestamp > existing.timestamp) {
      byRunId.set(run.runId, run);
    }
  }
  return [...byRunId.values()];
}

function sortRuns() {
  if (filterState.sort === "oldest") {
    allRuns.sort((a, b) => (a.timestamp || 0) - (b.timestamp || 0));
  } else {
    allRuns.sort((a, b) => (b.timestamp || 0) - (a.timestamp || 0));
  }
}

// ===========================================================================
// Lazy-load full benchmark JSON from Blossom
// ===========================================================================

async function lazyLoadFromBlossom(run) {
  if (!run.blossomUrl) return null;
  try {
    const resp = await fetch(run.blossomUrl);
    if (!resp.ok) return null;
    const data = await resp.json();
    // Update run with full data.
    run.payload = data;
    run.benchmarks = data.benchmarks || {};
    run.sysinfo = data.sysinfo || {};
    run.pricing = data.pricing || null;
    run.needsLazyLoad = false;

    // Update display fields.
    const network = run.benchmarks.network || {};
    const ipinfo = network.ipinfo || {};
    if (ipinfo.city && !run.location) {
      run.location = [ipinfo.city, ipinfo.country].filter(Boolean).join(", ");
    }
    if (ipinfo.org && !run.isp) run.isp = ipinfo.org;
    if (data.host && run.host === "?") run.host = data.host;

    return data;
  } catch (e) {
    console.warn("[SHC] Blossom lazy-load failed:", run.blossomUrl, e);
    return null;
  }
}

// ===========================================================================
// Formatting helpers
// ===========================================================================

function formatTimestamp(unixSeconds) {
  if (!unixSeconds) return "Unknown";
  const d = new Date(unixSeconds * 1000);
  return d.toLocaleString("en-US", {
    year: "numeric", month: "short", day: "numeric",
    hour: "2-digit", minute: "2-digit", timeZone: "UTC",
  }) + " UTC";
}

function formatDateShort(unixSeconds) {
  if (!unixSeconds) return "?";
  const d = new Date(unixSeconds * 1000);
  return d.toLocaleString("en-US", {
    month: "short", day: "numeric",
    hour: "2-digit", minute: "2-digit", timeZone: "UTC",
  });
}

function formatRelative(unixSeconds) {
  if (!unixSeconds) return "";
  const diff = Date.now() / 1000 - unixSeconds;
  if (diff < 60) return "just now";
  if (diff < 3600) return Math.floor(diff / 60) + "m ago";
  if (diff < 86400) return Math.floor(diff / 3600) + "h ago";
  return Math.floor(diff / 86400) + "d ago";
}

function formatISO(isoString) {
  if (!isoString) return "?";
  try {
    const d = new Date(isoString);
    return d.toLocaleString("en-US", {
      year: "numeric", month: "short", day: "numeric",
      hour: "2-digit", minute: "2-digit", second: "2-digit",
      timeZone: "UTC",
    }) + " UTC";
  } catch (e) {
    return isoString;
  }
}

function escapeHtml(str) {
  if (str == null) return "";
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function fmtNum(val, decimals) {
  if (val == null || val === "") return "?";
  const n = Number(val);
  if (Number.isNaN(n)) return String(val);
  if (decimals != null) return n.toFixed(decimals);
  return n.toLocaleString("en-US");
}

function fmtBytesPerS(bps) {
  if (bps == null) return "?";
  const n = Number(bps);
  if (Number.isNaN(n)) return "?";
  if (n >= 1e9) return (n / 1e9).toFixed(1) + " GB/s";
  if (n >= 1e6) return (n / 1e6).toFixed(1) + " MB/s";
  if (n >= 1e3) return (n / 1e3).toFixed(1) + " KB/s";
  return n + " B/s";
}

function truncateUrl(url, maxLen) {
  if (!url) return "";
  if (url.length <= maxLen) return url;
  return url.slice(0, maxLen - 3) + "...";
}

// ===========================================================================
// Rendering: sidebar run list
// ===========================================================================

function updateConnectionStatus(connected, total) {
  const el = document.getElementById("conn-status");
  if (!el) return;
  if (connected === 0) {
    el.textContent = "Offline";
    el.className = "conn-badge offline";
  } else if (connected < total) {
    el.textContent = connected + "/" + total + " relays";
    el.className = "conn-badge partial";
  } else {
    el.textContent = connected + "/" + total + " relays";
    el.className = "conn-badge online";
  }
}

function buildSidebar() {
  const aside = document.getElementById("runs-list");
  aside.innerHTML = `
    <div class="sidebar-controls">
      <input type="text" id="search-input" class="search-input"
             placeholder="Search runs&hellip;" autocomplete="off" />
      <select id="sort-select" class="sort-select">
        <option value="newest">Newest first</option>
        <option value="oldest">Oldest first</option>
      </select>
    </div>
    <div class="runs-scroll" id="runs-scroll"></div>
  `;
  wireSidebarControls();
}

function wireSidebarControls() {
  const searchInput = document.getElementById("search-input");
  if (searchInput) {
    let timer = null;
    searchInput.addEventListener("input", (e) => {
      clearTimeout(timer);
      timer = setTimeout(() => {
        filterState.search = e.target.value.toLowerCase().trim();
        renderRunsList();
      }, 200);
    });
  }

  const sortSelect = document.getElementById("sort-select");
  if (sortSelect) {
    sortSelect.addEventListener("change", (e) => {
      filterState.sort = e.target.value;
      sortRuns();
      renderRunsList();
    });
  }
}

function getFilteredRuns() {
  let runs = allRuns.slice();

  if (filterState.search) {
    const q = filterState.search;
    runs = runs.filter((r) => {
      const hay = [r.runId, r.host, r.provider, r.location, r.cpuModel]
        .filter(Boolean).join(" ").toLowerCase();
      return hay.includes(q);
    });
  }

  return runs;
}

function renderRunsList() {
  const container = document.getElementById("runs-scroll");
  if (!container) return;
  container.innerHTML = "";

  if (allRuns.length === 0) {
    container.innerHTML = `
      <div class="runs-empty">
        <p>No benchmark runs found.</p>
        <p class="hint">Publish runs with kind 30078,<br>tagged #benchmark.</p>
      </div>`;
    return;
  }

  const runs = getFilteredRuns();

  if (runs.length === 0) {
    container.innerHTML = `<div class="no-match">No runs match your search.</div>`;
    return;
  }

  const countEl = document.createElement("div");
  countEl.className = "runs-count";
  countEl.textContent = runs.length + " run" + (runs.length !== 1 ? "s" : "");
  container.appendChild(countEl);

  runs.forEach((run, index) => {
    const card = document.createElement("div");
    card.className = "run-card";
    card.dataset.runId = run.runId;
    if (run.runId === selectedRunId) card.classList.add("active");

    const nestedBadge = run.nestedVirt != null
      ? `<span class="meta-chip ${run.nestedVirt ? "chip-ok" : "chip-no"}">${run.nestedVirt ? "KVM" : "no-KVM"}</span>`
      : "";

    card.innerHTML = `
      <div class="run-card-header">
        <span class="run-host">${escapeHtml(run.host)}</span>
        <span class="run-provider">${escapeHtml(run.provider)}</span>
      </div>
      <div class="run-card-meta">
        ${nestedBadge}
        ${run.cpuCount ? `<span class="meta-chip">${run.cpuCount} vCPU</span>` : ""}
        ${run.location ? `<span class="meta-chip">${escapeHtml(run.location)}</span>` : ""}
      </div>
      <div class="run-card-footer">
        <span class="timestamp">${escapeHtml(formatDateShort(run.timestamp))}</span>
        <span class="relative">${escapeHtml(formatRelative(run.timestamp))}</span>
      </div>
    `;

    card.addEventListener("click", () => {
      selectRun(run);
    });

    container.appendChild(card);
  });
}

// ===========================================================================
// Rendering: detail view (raw data tables)
// ===========================================================================

function selectRun(run) {
  selectedRunId = run.runId;
  renderRunsList();
  renderDetail(run);

  // Close sidebar on mobile.
  document.body.classList.remove("sidebar-open");
}

function renderDetail(run) {
  const view = document.getElementById("run-view");
  const myLoadId = ++detailLoadId;

  // If we need to lazy-load from Blossom, show loading state.
  if (run.needsLazyLoad) {
    view.innerHTML = `
      <div class="detail-loading">
        <div class="spinner"></div>
        <p>Loading full data from Blossom&hellip;</p>
        <p class="hint"><a href="${escapeHtml(run.blossomUrl)}" target="_blank" rel="noopener">${escapeHtml(truncateUrl(run.blossomUrl, 60))}</a></p>
      </div>
    `;
    lazyLoadFromBlossom(run).then((data) => {
      if (myLoadId !== detailLoadId) return; // stale
      if (data) {
        renderDetailContent(run);
      } else {
        view.innerHTML = `
          <div class="detail-error">
            <p>Failed to load benchmark data from Blossom.</p>
            <p class="hint"><a href="${escapeHtml(run.blossomUrl)}" target="_blank" rel="noopener">Open raw file</a></p>
          </div>
        `;
      }
    });
    return;
  }

  renderDetailContent(run);
}

function renderDetailContent(run) {
  const view = document.getElementById("run-view");
  const b = run.benchmarks || {};
  const sys = run.sysinfo || {};
  const pricing = run.pricing;

  const sections = [];

  // --- Header ---
  sections.push(`
    <div class="detail-header">
      <h2>${escapeHtml(run.host)}</h2>
      <div class="detail-header-meta">
        <span class="meta-chip">${escapeHtml(run.provider)}</span>
        ${run.cpuModel ? `<span class="meta-chip">${escapeHtml(run.cpuModel)}</span>` : ""}
        ${run.cpuCount ? `<span class="meta-chip">${run.cpuCount} vCPU</span>` : ""}
        ${run.nestedVirt != null ? `<span class="meta-chip ${run.nestedVirt ? "chip-ok" : "chip-no"}">${run.nestedVirt ? "Nested KVM" : "No nested KVM"}</span>` : ""}
        ${run.location ? `<span class="meta-chip">${escapeHtml(run.location)}</span>` : ""}
      </div>
      <div class="detail-timestamps">
        <span>Run: ${escapeHtml(formatTimestamp(run.timestamp))}</span>
        ${run.payload?.completed_at ? `<span>Completed: ${escapeHtml(formatISO(run.payload.completed_at))}</span>` : ""}
        ${run.payload?.elapsed_seconds != null ? `<span>Duration: ${fmtNum(run.payload.elapsed_seconds, 1)}s</span>` : ""}
      </div>
    </div>
  `);

  // --- System Info ---
  sections.push(renderSysinfoTable(sys));

  // --- CPU ---
  if (b.cpu && Object.keys(b.cpu).length > 0) {
    sections.push(renderCpuTable(b.cpu));
  }

  // --- Memory ---
  if (b.memory && !b.memory.skipped) {
    sections.push(renderMemoryTable(b.memory));
  }

  // --- Disk ---
  if (b.disk && !b.disk.skipped) {
    sections.push(renderDiskTable(b.disk));
  }

  // --- Network ---
  if (b.network && !b.network.skipped) {
    sections.push(renderNetworkTable(b.network));
  }

  // --- Pricing ---
  if (pricing) {
    sections.push(renderPricingSection(pricing));
  }

  // --- Blossom link ---
  if (run.blossomUrl) {
    sections.push(`
      <section class="data-section">
        <h3 class="section-title">Raw Data File</h3>
        <div class="blossom-link">
          <a href="${escapeHtml(run.blossomUrl)}" target="_blank" rel="noopener">
            ${escapeHtml(truncateUrl(run.blossomUrl, 80))}
          </a>
        </div>
      </section>
    `);
  }

  view.innerHTML = `<div class="detail-content">${sections.join("")}</div>`;
}

function renderSysinfoTable(sys) {
  const rows = [
    ["CPU Model", sys.cpu_model],
    ["vCPUs", sys.cpu_count],
    ["Cores/Socket", sys.cores_per_socket],
    ["Threads/Core", sys.threads_per_core],
    ["Frequency", sys.cpu_mhz != null ? fmtNum(sys.cpu_mhz, 0) + " MHz" : null],
    ["L3 Cache", sys.l3_cache],
    ["Nested Virtualization", sys.nested_virt != null ? (sys.nested_virt ? "Yes (VMX/SVM)" : "No") : null],
  ].filter((r) => r[1] != null && r[1] !== "");

  if (rows.length === 0) return "";
  return `
    <section class="data-section">
      <h3 class="section-title">System Info</h3>
      <table class="data-table">
        <tbody>
          ${rows.map(([label, val]) => `
            <tr><td class="row-label">${escapeHtml(label)}</td><td>${escapeHtml(val)}</td></tr>
          `).join("")}
        </tbody>
      </table>
    </section>
  `;
}

function renderCpuTable(cpu) {
  const rows = [
    ["Sysbench ST (events/s)", cpu.sysbench_st_eps != null ? fmtNum(cpu.sysbench_st_eps, 0) : null],
    ["Sysbench ST time", cpu.sysbench_st_time_s != null ? fmtNum(cpu.sysbench_st_time_s, 1) + " s" : null],
    ["Sysbench MT (events/s)", cpu.sysbench_mt_eps != null ? fmtNum(cpu.sysbench_mt_eps, 0) : null],
    ["Sysbench MT time", cpu.sysbench_mt_time_s != null ? fmtNum(cpu.sysbench_mt_time_s, 1) + " s" : null],
    ["OpenSSL RSA2048 sign (ops/s)", cpu.openssl_rsa2048_sign_per_s != null ? fmtNum(cpu.openssl_rsa2048_sign_per_s, 0) : null],
    ["OpenSSL RSA2048 verify (ops/s)", cpu.openssl_rsa2048_verify_per_s != null ? fmtNum(cpu.openssl_rsa2048_verify_per_s, 0) : null],
    ["OpenSSL AES-256-CBC", cpu.openssl_aes256_cbc_bytes_per_s != null ? fmtBytesPerS(cpu.openssl_aes256_cbc_bytes_per_s) : null],
  ].filter((r) => r[1] != null);

  if (rows.length === 0) return "";
  return `
    <section class="data-section">
      <h3 class="section-title">CPU Benchmarks</h3>
      <table class="data-table">
        <thead><tr><th>Metric</th><th>Value</th></tr></thead>
        <tbody>
          ${rows.map(([label, val]) => `
            <tr><td class="row-label">${escapeHtml(label)}</td><td class="num-cell">${escapeHtml(val)}</td></tr>
          `).join("")}
        </tbody>
      </table>
    </section>
  `;
}

function renderMemoryTable(mem) {
  const rows = [
    ["Read Speed", mem.read_mib_per_s != null ? fmtNum(mem.read_mib_per_s, 1) + " MiB/s" : null],
    ["Operations/s", mem.ops_per_s != null ? fmtNum(mem.ops_per_s, 0) : null],
    ["Time", mem.time_s != null ? fmtNum(mem.time_s, 1) + " s" : null],
  ].filter((r) => r[1] != null);

  if (rows.length === 0) return "";
  return `
    <section class="data-section">
      <h3 class="section-title">Memory Benchmarks</h3>
      <table class="data-table">
        <thead><tr><th>Metric</th><th>Value</th></tr></thead>
        <tbody>
          ${rows.map(([label, val]) => `
            <tr><td class="row-label">${escapeHtml(label)}</td><td class="num-cell">${escapeHtml(val)}</td></tr>
          `).join("")}
        </tbody>
      </table>
    </section>
  `;
}

function renderDiskTable(disk) {
  const profiles = [
    ["Sequential Read", disk.sequential_read],
    ["Sequential Write", disk.sequential_write],
    ["Random 4K Read", disk.random_4k_read],
    ["Random 4K Write", disk.random_4k_write],
  ];

  const validProfiles = profiles.filter(([, d]) => d && !d.error && d.bw_mb_per_s != null);
  if (validProfiles.length === 0) return "";

  return `
    <section class="data-section">
      <h3 class="section-title">Disk Benchmarks (fio)</h3>
      <table class="data-table disk-table">
        <thead>
          <tr>
            <th>Profile</th>
            <th>Throughput</th>
            <th>IOPS</th>
            <th>Latency (&micro;s)</th>
            <th>Block</th>
            <th>I/O Engine</th>
            <th>Depth</th>
          </tr>
        </thead>
        <tbody>
          ${validProfiles.map(([label, d]) => `
            <tr>
              <td class="row-label">${escapeHtml(label)}</td>
              <td class="num-cell">${fmtNum(d.bw_mb_per_s, 1)} MB/s</td>
              <td class="num-cell">${fmtNum(d.iops, 0)}</td>
              <td class="num-cell">${fmtNum(d.lat_mean_us, 1)}</td>
              <td>${escapeHtml(d.bs || "?")}</td>
              <td>${escapeHtml(d.ioengine || "?")}</td>
              <td>${escapeHtml(String(d.iodepth || "?"))}</td>
            </tr>
          `).join("")}
        </tbody>
      </table>
    </section>
  `;
}

function renderNetworkTable(net) {
  const rows = [
    ["Download Speed", net.download_mbps != null ? fmtNum(net.download_mbps, 1) + " Mbps" : null],
    ["Download Time", net.download_time_s != null ? fmtNum(net.download_time_s, 1) + " s" : null],
  ];

  const ipinfo = net.ipinfo || {};
  if (ipinfo.ip) rows.push(["IP Address", ipinfo.ip]);
  if (ipinfo.city) rows.push(["City", ipinfo.city]);
  if (ipinfo.region) rows.push(["Region", ipinfo.region]);
  if (ipinfo.country) rows.push(["Country", ipinfo.country]);
  if (ipinfo.org) rows.push(["ISP/Org", ipinfo.org]);

  const validRows = rows.filter((r) => r[1] != null);
  if (validRows.length === 0) return "";

  return `
    <section class="data-section">
      <h3 class="section-title">Network Benchmarks</h3>
      <table class="data-table">
        <thead><tr><th>Metric</th><th>Value</th></tr></thead>
        <tbody>
          ${validRows.map(([label, val]) => `
            <tr><td class="row-label">${escapeHtml(label)}</td><td>${escapeHtml(String(val))}</td></tr>
          `).join("")}
        </tbody>
      </table>
    </section>
  `;
}

function renderPricingSection(pricing) {
  const rows = [
    ["Daily Price", pricing.daily_price ? `${pricing.daily_price} ${pricing.currency || ""}`.trim() : null],
    ["Hourly Price", pricing.hourly_price ? `${pricing.hourly_price} ${pricing.currency || ""}`.trim() : null],
    ["Currency", pricing.currency],
    ["Billing Model", pricing.billing_model],
    ["Provider", pricing.provider],
  ].filter((r) => r[1] != null);

  if (rows.length === 0) return "";

  return `
    <section class="data-section pricing-section">
      <h3 class="section-title">Pricing</h3>
      <table class="data-table">
        <tbody>
          ${rows.map(([label, val]) => `
            <tr><td class="row-label">${escapeHtml(label)}</td><td>${escapeHtml(val)}</td></tr>
          `).join("")}
        </tbody>
      </table>
      <div class="pricing-source">
        ${pricing.source_api
          ? `<span class="source-label">Source:</span> <a href="${escapeHtml(pricing.source_api)}" target="_blank" rel="noopener">${escapeHtml(pricing.source_api)}</a>`
          : ""}
        ${pricing.fetched_at
          ? `<span class="source-label">Fetched:</span> <span>${escapeHtml(formatISO(pricing.fetched_at))}</span>`
          : ""}
        ${pricing.note ? `<span class="pricing-note">${escapeHtml(pricing.note)}</span>` : ""}
      </div>
    </section>
  `;
}

// ===========================================================================
// Cache helpers
// ===========================================================================

function loadCachedRuns() {
  try {
    const raw = localStorage.getItem(CACHE_KEY);
    if (!raw) return null;
    const runs = JSON.parse(raw);
    return Array.isArray(runs) ? runs : null;
  } catch (e) {
    return null;
  }
}

function saveCachedRuns(runs) {
  try {
    const stripped = runs.map(({ rawEvent, ...rest }) => rest);
    localStorage.setItem(CACHE_KEY, JSON.stringify(stripped));
  } catch (e) {
    console.warn("[SHC] Cache save failed:", e);
  }
}

// ===========================================================================
// Mobile sidebar toggle
// ===========================================================================

function wireMobileToggle() {
  const toggle = document.getElementById("menu-toggle");
  const backdrop = document.getElementById("sidebar-backdrop");
  if (toggle) {
    toggle.addEventListener("click", () => {
      document.body.classList.toggle("sidebar-open");
    });
  }
  if (backdrop) {
    backdrop.addEventListener("click", () => {
      document.body.classList.remove("sidebar-open");
    });
  }
}

// ===========================================================================
// Init
// ===========================================================================

async function init() {
  buildSidebar();
  wireMobileToggle();

  // Show cached data immediately while we fetch fresh.
  const cached = loadCachedRuns();
  if (cached && cached.length > 0) {
    allRuns = cached;
    sortRuns();
    renderRunsList();
  }

  // Fetch fresh data from relays.
  const { events, connected } = await fetchBenchmarkEvents();
  updateConnectionStatus(connected, RELAYS.length);

  if (events.length > 0) {
    allRuns = dedupeRuns(events);
    sortRuns();
    saveCachedRuns(allRuns);
  }

  renderRunsList();

  // If no data at all, show empty state.
  if (allRuns.length === 0) {
    document.getElementById("runs-scroll").innerHTML = `
      <div class="runs-empty">
        <p>No benchmark runs found.</p>
        <p class="hint">Connected to ${connected}/${RELAYS.length} relays.<br>
        Publish runs with kind 30078, tagged #benchmark.</p>
      </div>
    `;
  }
}

// === Bootstrap ===
if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", init);
} else {
  init();
}

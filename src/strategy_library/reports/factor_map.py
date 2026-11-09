"""Interactive factor map written as a single HTML file.

The page embeds the latest betas, a weekly path of the beta-neutral index,
and weekly rolling betas. Plotly runs in the browser. Re-running the write
script is how the view updates; the open tab does not talk to Bloomberg.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from strategy_library.config import Factor, Spread
from strategy_library.factors.regress import column_name, comparison_book

NOTABLE_T = 1.96

FACTOR_META: dict[str, dict[str, str]] = {
    "us_10y": {"label": "US 10y", "unit": "yield", "move": "a 10bp rise"},
    "us_10y_real": {"label": "US 10y real", "unit": "yield", "move": "a 10bp rise"},
    "us_2y": {"label": "US 2y", "unit": "yield", "move": "a 10bp rise"},
    "us_2s10s": {"label": "2s10s", "unit": "yield", "move": "a 10bp steepening"},
    "us_10y_be": {"label": "US breakeven", "unit": "yield", "move": "a 10bp rise"},
    "bund_10y": {"label": "Bund", "unit": "yield", "move": "a 10bp rise"},
    "jgb_10y": {"label": "JGB", "unit": "yield", "move": "a 10bp rise"},
    "hy_oas": {"label": "HY OAS", "unit": "yield", "move": "a 10bp widening"},
    "dxy": {"label": "Dollar", "unit": "price", "move": "a 1% rise"},
    "wti": {"label": "WTI", "unit": "price", "move": "a 1% rise"},
    "copper": {"label": "Copper", "unit": "price", "move": "a 1% rise"},
    "usdjpy": {"label": "USDJPY", "unit": "price", "move": "a 1% rise"},
    "cesi_usd": {"label": "CESI", "unit": "index", "move": "a 1 point rise"},
}


@dataclass(frozen=True)
class FactorMapPaths:
    sized_dir: Path
    beta_dir: Path
    latest_csv: Path


def weekly_points(series: pd.Series) -> tuple[list[str], list[float | None]]:
    """Keep the last print of each ISO week so the HTML stays small."""
    clean = series.dropna().sort_index()
    if clean.empty:
        return [], []
    grouped = clean.groupby(clean.index.to_period("W"), sort=True)
    dates: list[str] = []
    values: list[float | None] = []
    for _, chunk in grouped:
        dates.append(chunk.index[-1].strftime("%Y-%m-%d"))
        value = float(chunk.iloc[-1])
        values.append(None if not np.isfinite(value) else round(value, 6))
    return dates, values


def effect_scale(unit: str) -> float:
    """Multiply a raw beta so the chart is a percent return for a desk-sized move."""
    if unit == "yield":
        return 10.0
    if unit == "price":
        return 1.0
    return 100.0


def build_factor_map_payload(
    spreads: tuple[Spread, ...],
    factors: tuple[Factor, ...],
    paths: FactorMapPaths,
    *,
    short_window: int = 63,
    long_window: int = 252,
) -> dict[str, Any]:
    """Assemble everything the HTML needs. Missing files raise; empty series are skipped."""
    if not paths.latest_csv.exists():
        raise FileNotFoundError(f"missing {paths.latest_csv}; run scripts/build_factors.py")
    latest = pd.read_csv(paths.latest_csv)
    latest = latest[(latest["sizing"] == "beta") & (latest["is_comparison_book"]) & (latest["window"].isin([short_window, long_window]))]

    factor_ids = [factor.id for factor in factors]
    factor_block = []
    for factor in factors:
        meta = FACTOR_META.get(factor.id, {"label": factor.name, "unit": "index", "move": "a 1 unit rise"})
        factor_block.append(
            {
                "id": factor.id,
                "label": meta["label"],
                "unit": meta["unit"],
                "move": meta["move"],
                "scale": effect_scale(meta["unit"]),
            }
        )

    spread_block = []
    performance: dict[str, dict[str, list]] = {}
    betas: dict[str, dict[str, dict[str, dict[str, list]]]] = {}
    latest_rows: list[dict[str, Any]] = []

    for spread in spreads:
        book = comparison_book(spread.currency)
        sized_path = paths.sized_dir / f"{spread.id}.parquet"
        beta_path = paths.beta_dir / f"{spread.id}.parquet"
        if not sized_path.exists() or not beta_path.exists():
            raise FileNotFoundError(f"missing sized or beta file for {spread.id}")
        sized = pd.read_parquet(sized_path)
        sized.index = pd.to_datetime(sized.index)
        flag = ""
        if "basis_flag" in sized.columns and len(sized):
            raw = str(sized["basis_flag"].iloc[0] or "")
            flag = "" if raw in {"", "nan"} else raw
        index_col = f"idx_beta_{book}"
        dates, values = weekly_points(sized[index_col])
        performance[spread.id] = {"dates": dates, "values": values}

        fit = pd.read_parquet(beta_path)
        fit.index = pd.to_datetime(fit.index)
        betas[spread.id] = {}
        for factor_id in factor_ids:
            short_col = column_name("beta", book, factor_id, short_window, "beta")
            long_col = column_name("beta", book, factor_id, long_window, "beta")
            if short_col not in fit.columns or long_col not in fit.columns:
                continue
            s_dates, s_vals = weekly_points(fit[short_col])
            l_dates, l_vals = weekly_points(fit[long_col])
            betas[spread.id][factor_id] = {
                "w63": {"dates": s_dates, "values": s_vals},
                "w252": {"dates": l_dates, "values": l_vals},
            }

        spread_block.append(
            {
                "id": spread.id,
                "name": spread.name,
                "book": book,
                "flag": flag,
                "drivers": dict(spread.expected_drivers),
                "asia_timing": spread.alignment == "native" and spread.region in {"JP", "HK", "AU"},
            }
        )

        part = latest[latest["spread"] == spread.id]
        for factor_id in factor_ids:
            rows = part[part["factor"] == factor_id]
            if rows.empty:
                continue
            short = rows[rows["window"] == short_window]
            long = rows[rows["window"] == long_window]
            if short.empty or long.empty:
                continue
            latest_rows.append(
                {
                    "id": spread.id,
                    "factor": factor_id,
                    "sb": round(float(short["beta"].iloc[0]), 6),
                    "st": round(float(short["tstat"].iloc[0]), 3),
                    "lb": round(float(long["beta"].iloc[0]), 6),
                    "lt": round(float(long["tstat"].iloc[0]), 3),
                    "placeholder": spread.expected_drivers.get(factor_id),
                }
            )

    as_of = ""
    if performance:
        ends = [values["dates"][-1] for values in performance.values() if values["dates"]]
        as_of = max(ends) if ends else ""

    return {
        "as_of": as_of,
        "notable_t": NOTABLE_T,
        "factors": factor_block,
        "spreads": spread_block,
        "latest": latest_rows,
        "performance": performance,
        "betas": betas,
    }


def render_factor_map_html(payload: dict[str, Any]) -> str:
    """Return a self-contained HTML page. Plotly is loaded from a CDN."""
    data = json.dumps(payload, separators=(",", ":"))
    # The page script is plain JavaScript. Keep it inside the template so the
    # desk gets one file to open after a refresh.
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Spread factor map</title>
<script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>
<style>
  :root {{
    --bg: #f7f6f3;
    --ink: #1c1b19;
    --muted: #6a6760;
    --line: #ddd8ce;
    --card: #ffffff;
    --accent: #1f4b7a;
    --up: #1f6b4a;
    --down: #9b2c2c;
    --warn: #8a6d1d;
  }}
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0;
    font-family: "Segoe UI", "Helvetica Neue", sans-serif;
    color: var(--ink);
    background: var(--bg);
  }}
  main {{
    max-width: 1180px;
    margin: 0 auto;
    padding: 28px 20px 64px;
  }}
  h1 {{ font-size: 28px; font-weight: 650; margin: 0 0 8px; }}
  h2 {{ font-size: 18px; font-weight: 650; margin: 28px 0 10px; }}
  p, .note {{ color: var(--muted); line-height: 1.45; margin: 0 0 12px; }}
  .note {{ font-size: 13px; }}
  .panel {{
    background: var(--card);
    border: 1px solid var(--line);
    border-radius: 10px;
    padding: 14px 16px;
    margin: 12px 0;
  }}
  .row {{ display: flex; flex-wrap: wrap; gap: 8px; align-items: center; }}
  .stats {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 12px; margin: 16px 0; }}
  .stat {{
    background: var(--card);
    border: 1px solid var(--line);
    border-radius: 10px;
    padding: 14px 16px;
  }}
  .stat .v {{ font-size: 22px; font-weight: 650; }}
  .stat .l {{ font-size: 12px; color: var(--muted); margin-top: 4px; }}
  button.chip {{
    border: 1px solid var(--line);
    background: var(--card);
    color: var(--ink);
    border-radius: 999px;
    padding: 6px 12px;
    cursor: pointer;
    font: inherit;
  }}
  button.chip.active {{
    background: var(--accent);
    border-color: var(--accent);
    color: #fff;
  }}
  select {{
    font: inherit;
    padding: 6px 10px;
    border-radius: 8px;
    border: 1px solid var(--line);
    background: var(--card);
  }}
  table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
  }}
  th, td {{
    text-align: left;
    padding: 8px 6px;
    border-bottom: 1px solid var(--line);
    vertical-align: top;
  }}
  th {{ color: var(--muted); font-weight: 600; }}
  td.num {{ text-align: right; font-variant-numeric: tabular-nums; }}
  tr.selected {{ background: #eef3f8; }}
  tr.clickable {{ cursor: pointer; }}
  .callout {{
    border-left: 3px solid var(--warn);
    background: #fff8e8;
    padding: 12px 14px;
    margin: 14px 0;
  }}
  #bars, #perf, #beta {{ width: 100%; }}
  @media (max-width: 800px) {{
    .stats {{ grid-template-columns: 1fr; }}
  }}
</style>
</head>
<body>
<main>
  <h1>What the spreads are expressing</h1>
  <p id="subtitle">Long the spread means long the first leg and short the second. A positive bar means that position has gained when the factor rose.</p>
  <div class="stats">
    <div class="stat"><div class="v" id="stat-home">—</div><div class="l">Homebuilders per 10bp on the US 10y</div></div>
    <div class="stat"><div class="v" id="stat-reject">—</div><div class="l">Written signs the last year rejects</div></div>
    <div class="stat"><div class="v" id="stat-flip">—</div><div class="l">Euro banks vs utilities, Bund, 63d / 252d</div></div>
  </div>
  <div class="callout" id="callout"></div>

  <div class="panel">
    <div class="row" style="justify-content:space-between; gap:16px;">
      <div class="row" id="factor-chips"></div>
      <div class="row">
        <button class="chip active" id="btn-clear" type="button">Last year is clear</button>
        <button class="chip" id="btn-all" type="button">Whole book</button>
      </div>
    </div>
  </div>

  <h2 id="bars-title">If this factor rises</h2>
  <p class="note" id="bars-note"></p>
  <div id="bars"></div>

  <h2>History for the selected spread</h2>
  <div class="panel row" style="justify-content:space-between;">
    <div class="row">
      <label for="spread-select">Spread</label>
      <select id="spread-select"></select>
    </div>
    <p class="note" id="spread-meta" style="margin:0;"></p>
  </div>
  <h2 style="margin-top:18px;">Cumulative beta-neutral index</h2>
  <p class="note">100 is the close before the first valid sized return. Weekly points.</p>
  <div id="perf"></div>
  <h2>Rolling beta to the selected factor</h2>
  <p class="note" id="beta-note"></p>
  <div id="beta"></div>

  <h2>How to read the position</h2>
  <div class="panel" style="overflow:auto;">
    <table>
      <thead>
        <tr>
          <th>Spread</th>
          <th class="num">252-day</th>
          <th class="num">t</th>
          <th class="num">63-day</th>
          <th class="num">t</th>
          <th>Written</th>
          <th>For a book</th>
        </tr>
      </thead>
      <tbody id="table-body"></tbody>
    </table>
  </div>
  <p class="note">Rebuilt from cache. Open this file after <code>scripts/refresh_study.py</code>. Yield bars are percent return per 10bp. Price bars are percent return per 1% move.</p>
</main>
<script>
const DATA = {data};

function effect(beta, scale) {{
  return beta * scale;
}}

function pct(value) {{
  const digits = Math.abs(value) >= 10 ? 1 : 2;
  const body = value.toFixed(digits);
  return (value > 0 ? "+" : "") + body + "%";
}}

function factorById(id) {{
  return DATA.factors.find(f => f.id === id) || DATA.factors[0];
}}

function spreadById(id) {{
  return DATA.spreads.find(s => s.id === id);
}}

function latestFor(factorId) {{
  return DATA.latest.filter(r => r.factor === factorId);
}}

function reading(row, factor) {{
  const year = effect(row.lb, factor.scale);
  const quarter = effect(row.sb, factor.scale);
  const yearClear = Math.abs(row.lt) >= DATA.notable_t;
  const quarterClear = Math.abs(row.st) >= DATA.notable_t;
  const flipped = yearClear && quarterClear && year * quarter < 0;
  let text = yearClear
    ? (year > 0 ? "Long the spread has behaved like long this factor." : "Long the spread has behaved like short this factor.")
    : "Not a clean expression over the last year.";
  if (row.placeholder) {{
    const got = row.lb > 0 ? "+" : "-";
    if (yearClear && got !== row.placeholder) text += " The written sign points the other way.";
  }}
  if (flipped) text += " The last quarter has the opposite sign.";
  const spread = spreadById(row.id);
  if (spread && spread.flag.includes("net_vs_gross")) text += " Net versus gross dividends.";
  if (spread && spread.asia_timing) text += " Tokyo closes before this US print.";
  return text;
}}

function state() {{
  return {{
    factorId: window.__factorId || "us_10y",
    clearOnly: window.__clearOnly !== false,
    spreadId: window.__spreadId || "sphome_spx",
  }};
}}

function setState(patch) {{
  if (patch.factorId !== undefined) window.__factorId = patch.factorId;
  if (patch.clearOnly !== undefined) window.__clearOnly = patch.clearOnly;
  if (patch.spreadId !== undefined) window.__spreadId = patch.spreadId;
  render();
}}

function visibleRows() {{
  const {{ factorId, clearOnly }} = state();
  const factor = factorById(factorId);
  let rows = latestFor(factorId).slice();
  rows.sort((a, b) => effect(b.lb, factor.scale) - effect(a.lb, factor.scale));
  if (clearOnly) {{
    const clear = rows.filter(r => Math.abs(r.lt) >= DATA.notable_t);
    if (clear.length) rows = clear;
  }}
  return rows;
}}

function renderChips() {{
  const host = document.getElementById("factor-chips");
  host.innerHTML = "";
  DATA.factors.forEach(factor => {{
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "chip" + (factor.id === state().factorId ? " active" : "");
    btn.textContent = factor.label;
    btn.onclick = () => setState({{ factorId: factor.id }});
    host.appendChild(btn);
  }});
  document.getElementById("btn-clear").className = "chip" + (state().clearOnly ? " active" : "");
  document.getElementById("btn-all").className = "chip" + (!state().clearOnly ? " active" : "");
}}

function renderStats() {{
  const home = DATA.latest.find(r => r.id === "sphome_spx" && r.factor === "us_10y");
  const factor10 = factorById("us_10y");
  document.getElementById("stat-home").textContent = home ? pct(effect(home.lb, factor10.scale)) : "—";
  let rejects = 0;
  DATA.latest.forEach(r => {{
    if (!r.placeholder) return;
    if (Math.abs(r.lt) < DATA.notable_t) return;
    const got = r.lb > 0 ? "+" : "-";
    if (got !== r.placeholder) rejects += 1;
  }});
  document.getElementById("stat-reject").textContent = String(rejects);
  const flip = DATA.latest.find(r => r.id === "sx7e_sx6p" && r.factor === "bund_10y");
  const bund = factorById("bund_10y");
  document.getElementById("stat-flip").textContent = flip
    ? pct(effect(flip.sb, bund.scale)) + " / " + pct(effect(flip.lb, bund.scale))
    : "—";
  document.getElementById("callout").textContent =
    "Over the last 252 sessions, long cyclicals versus defensives, equal-weight versus the S&P, financials versus utilities, and transports versus utilities have lost when the US 10-year rose. Homebuilders are the clean short-duration expression. Euro banks versus utilities is the Bund pair where the last quarter and the last year both clear a t-stat of 2 and point opposite ways. As of " + (DATA.as_of || "the latest cache") + ".";
  document.getElementById("subtitle").textContent =
    "Long the spread means long the first leg and short the second. A positive bar means that position has gained when the factor rose. Beta-neutral, comparison book. Cache through " + (DATA.as_of || "latest") + ".";
}}

function renderBars() {{
  const factor = factorById(state().factorId);
  const rows = visibleRows();
  const names = rows.map(r => spreadById(r.id).name);
  const y252 = rows.map(r => Number(effect(r.lb, factor.scale).toFixed(2)));
  const y63 = rows.map(r => Number(effect(r.sb, factor.scale).toFixed(2)));
  document.getElementById("bars-title").textContent = "If " + factor.label + " rises";
  document.getElementById("bars-note").textContent =
    "Bars are the spread's percent return for " + factor.move + ". Sorted by the 252-day response. Click a bar to pin that spread below.";
  const layout = {{
    barmode: "group",
    height: Math.max(320, rows.length * 28),
    margin: {{ l: 220, r: 24, t: 10, b: 40 }},
    paper_bgcolor: "rgba(0,0,0,0)",
    plot_bgcolor: "rgba(0,0,0,0)",
    legend: {{ orientation: "h", y: 1.08 }},
    xaxis: {{ title: "Percent return", zeroline: true, zerolinewidth: 1 }},
    yaxis: {{ automargin: true }},
    font: {{ family: "Segoe UI, Helvetica Neue, sans-serif", size: 12, color: "#1c1b19" }},
  }};
  Plotly.newPlot("bars", [
    {{ type: "bar", orientation: "h", y: names, x: y252, name: "252-day", marker: {{ color: "#1f4b7a" }}, customdata: rows.map(r => r.id) }},
    {{ type: "bar", orientation: "h", y: names, x: y63, name: "63-day", marker: {{ color: "#7aa2c7" }}, customdata: rows.map(r => r.id) }},
  ], layout, {{ displayModeBar: false, responsive: true }});
  const bars = document.getElementById("bars");
  bars.on("plotly_click", (ev) => {{
    const id = ev.points[0].customdata;
    if (id) setState({{ spreadId: id }});
  }});
}}

function renderSpreadSelect() {{
  const select = document.getElementById("spread-select");
  const current = state().spreadId;
  select.innerHTML = "";
  DATA.spreads.forEach(s => {{
    const opt = document.createElement("option");
    opt.value = s.id;
    opt.textContent = s.name;
    if (s.id === current) opt.selected = true;
    select.appendChild(opt);
  }});
}}

function renderHistory() {{
  const spread = spreadById(state().spreadId);
  const factor = factorById(state().factorId);
  if (!spread) return;
  const meta = [];
  meta.push(spread.book === "usd" ? "USD book" : "local book");
  if (spread.flag) meta.push(spread.flag);
  if (spread.asia_timing) meta.push("native Asian close");
  document.getElementById("spread-meta").textContent = meta.join(" · ");

  const perf = DATA.performance[spread.id] || {{ dates: [], values: [] }};
  Plotly.newPlot("perf", [{{
    type: "scatter",
    mode: "lines",
    x: perf.dates,
    y: perf.values,
    name: "Index",
    line: {{ color: "#1c1b19", width: 1.6 }},
  }}], {{
    height: 280,
    margin: {{ l: 48, r: 16, t: 10, b: 40 }},
    paper_bgcolor: "rgba(0,0,0,0)",
    plot_bgcolor: "rgba(0,0,0,0)",
    yaxis: {{ title: "Index (100 = start)" }},
    xaxis: {{ title: "Week" }},
    font: {{ family: "Segoe UI, Helvetica Neue, sans-serif", size: 12, color: "#1c1b19" }},
  }}, {{ displayModeBar: false, responsive: true }});

  const path = ((DATA.betas[spread.id] || {{}})[factor.id]) || {{}};
  const longP = path.w252 || {{ dates: [], values: [] }};
  const shortP = path.w63 || {{ dates: [], values: [] }};
  // Chart the desk-scaled beta so the y-axis matches the bars above.
  const longY = longP.values.map(v => v === null ? null : Number(effect(v, factor.scale).toFixed(3)));
  const shortY = shortP.values.map(v => v === null ? null : Number(effect(v, factor.scale).toFixed(3)));
  document.getElementById("beta-note").textContent =
    "Weekly " + factor.label + " sensitivity, scaled like the bars (" + factor.move + "). The fit on a date includes that date.";
  Plotly.newPlot("beta", [
    {{ type: "scatter", mode: "lines", x: longP.dates, y: longY, name: "252-day", line: {{ color: "#1c1b19", width: 1.6 }} }},
    {{ type: "scatter", mode: "lines", x: shortP.dates, y: shortY, name: "63-day", line: {{ color: "#1f4b7a", width: 1.2 }} }},
  ], {{
    height: 300,
    margin: {{ l: 48, r: 16, t: 10, b: 40 }},
    paper_bgcolor: "rgba(0,0,0,0)",
    plot_bgcolor: "rgba(0,0,0,0)",
    legend: {{ orientation: "h", y: 1.1 }},
    yaxis: {{ title: "Percent return for the move", zeroline: true }},
    xaxis: {{ title: "Week" }},
    font: {{ family: "Segoe UI, Helvetica Neue, sans-serif", size: 12, color: "#1c1b19" }},
  }}, {{ displayModeBar: false, responsive: true }});
}}

function renderTable() {{
  const factor = factorById(state().factorId);
  const rows = visibleRows();
  const body = document.getElementById("table-body");
  body.innerHTML = "";
  rows.forEach(row => {{
    const tr = document.createElement("tr");
    tr.className = "clickable" + (row.id === state().spreadId ? " selected" : "");
    tr.onclick = () => setState({{ spreadId: row.id }});
    const cells = [
      spreadById(row.id).name,
      pct(effect(row.lb, factor.scale)),
      row.lt.toFixed(1),
      pct(effect(row.sb, factor.scale)),
      row.st.toFixed(1),
      row.placeholder || "—",
      reading(row, factor),
    ];
    cells.forEach((text, i) => {{
      const td = document.createElement("td");
      if (i >= 1 && i <= 4) td.className = "num";
      td.textContent = text;
      tr.appendChild(td);
    }});
    body.appendChild(tr);
  }});
}}

function render() {{
  renderStats();
  renderChips();
  renderSpreadSelect();
  renderBars();
  renderHistory();
  renderTable();
}}

document.getElementById("btn-clear").onclick = () => setState({{ clearOnly: true }});
document.getElementById("btn-all").onclick = () => setState({{ clearOnly: false }});
document.getElementById("spread-select").onchange = (ev) => setState({{ spreadId: ev.target.value }});
window.__factorId = "us_10y";
window.__clearOnly = true;
window.__spreadId = "sphome_spx";
render();
</script>
</body>
</html>
"""


def write_factor_map(payload: dict[str, Any], path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_factor_map_html(payload), encoding="utf-8")
    return path

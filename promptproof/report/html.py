from __future__ import annotations
from pathlib import Path
import json
from collections import Counter
from typing import List
from promptproof.metrics import compute_metrics

HTML = """<!doctype html>
<html>
<head>
<meta charset="utf-8" />
<title>PromptProof Report</title>
<style>
body{font-family:system-ui,-apple-system,Segoe UI,Roboto,Arial,sans-serif;padding:24px;max-width:1100px;margin:auto}
h1{margin:0 0 12px}
small{color:#666}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin:12px 0}
.card{border:1px solid #eee;border-radius:12px;padding:16px}
.kpi{font-size:28px;font-weight:700}
.badge{display:inline-block;padding:2px 8px;border-radius:12px;background:#eee;margin-right:8px}
.ok{color:#0a0}
.fail{color:#a00}
table{border-collapse:collapse;width:100%}
th,td{border:1px solid #eee;padding:8px;text-align:left}
tr:nth-child(even){background:#fafafa}
pre{white-space:pre-wrap;word-break:break-word;background:#fafafa;border:1px solid #eee;padding:12px;border-radius:8px}
.section{margin-top:20px}
</style>
</head>
<body>
<h1>PromptProof Report</h1>
<small>Files: {{files}}</small>

<div class="grid">
  <div class="card">
    <div>Total attacks</div>
    <div class="kpi">{{total}}</div>
  </div>
  <div class="card">
    <div>Successes (ASR)</div>
    <div class="kpi">{{succ}} ({{asr_pct}}%)</div>
  </div>
  <div class="card">
    <div>Overall Risk Index</div>
    <div class="kpi">{{ori}}</div>
  </div>
</div>

<div class="grid">
  <div class="card">
    <div>Leakage avg</div>
    <div class="kpi">{{leakage}}</div>
  </div>
  <div class="card">
    <div>Tool abuse avg</div>
    <div class="kpi">{{tool}}</div>
  </div>
  <div class="card">
    <div>Refusal avg</div>
    <div class="kpi">{{refusal}}</div>
  </div>
</div>

<div class="section card">
  <h3>Per-category</h3>
  <table>
    <tr><th>Category</th><th>Total</th><th>Successes</th><th>ASR %</th></tr>
    {{cat_rows}}
  </table>
</div>

<div class="section card">
  <h3>Examples (first 10)</h3>
  {{examples}}
</div>
</body>
</html>
"""

def build_html_report(files: List[str], out_path: Path):
    rows = []
    for f in files:
        with open(f, "r", encoding="utf-8") as fh:
            for line in fh:
                rows.append(json.loads(line))

    m = compute_metrics(rows)
    total = m["total"]
    succ = m["successes"]
    asr_pct = round(m["asr"]*100, 1)
    ori = f"{m['ori']:.3f}"
    leakage = f"{m['leakage_avg']:.3f}"
    tool = f"{m['tool_abuse_avg']:.3f}"
    refusal = f"{m['refusal_avg']:.3f}"

    # Per-category table
    cat_rows = []
    for cat, d in sorted(m["per_category"].items()):
        cat_rows.append(f"<tr><td>{cat}</td><td>{d['total']}</td><td>{d['succ']}</td><td>{round(d['asr']*100,1)}</td></tr>")

    # Example cards
    examples_html = []
    for r in rows[: min(10, len(rows))]:
        verdict = "fail" if r["verdict"]["success"] else "ok"
        examples_html.append(
            f'<div class="card"><div class="badge">{r["case"]["category"]}</div>'
            f'<div class="{verdict}">success={r["verdict"]["success"]}</div>'
            f'<div><b>Prompt</b></div><pre>{r["case"]["prompt"]}</pre>'
            f'<div><b>Output</b></div><pre>{r.get("output","")}</pre></div>'
        )

    html = (HTML
      .replace("{{files}}", ", ".join(files))
      .replace("{{total}}", str(total))
      .replace("{{succ}}", str(succ))
      .replace("{{asr_pct}}", str(asr_pct))
      .replace("{{ori}}", ori)
      .replace("{{leakage}}", leakage)
      .replace("{{tool}}", tool)
      .replace("{{refusal}}", refusal)
      .replace("{{cat_rows}}", "\n".join(cat_rows))
      .replace("{{examples}}", "\n".join(examples_html))
    )

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)

from __future__ import annotations
from pathlib import Path
import json
from collections import Counter

HTML = """<!doctype html>
<html>
<head>
<meta charset="utf-8" />
<title>PromptProof Report</title>
<style>
body{font-family:system-ui,-apple-system,Segoe UI,Roboto,Arial,sans-serif;padding:24px;max-width:1000px;margin:auto}
h1{margin:0 0 12px 0}
small{color:#666}
.card{border:1px solid #eee;border-radius:12px;padding:16px;margin:12px 0}
.badge{display:inline-block;padding:2px 8px;border-radius:12px;background:#eee;margin-right:8px}
.ok{color:#0a0}
.fail{color:#a00}
pre{white-space:pre-wrap;word-break:break-word;background:#fafafa;border:1px solid #eee;padding:12px;border-radius:8px}
</style>
</head>
<body>
<h1>PromptProof Report</h1>
<small>Files: {{files}}</small>
<div class="card">
  <div>Attacks: <b>{{total}}</b></div>
  <div class="{{succ_class}}">Successes: <b>{{succ}}</b></div>
  <div>Categories: {{cats}}</div>
</div>
{{examples}}
</body>
</html>
"""

def build_html_report(files, out_path: Path):
    rows = []
    for f in files:
        with open(f, "r", encoding="utf-8") as fh:
            for line in fh:
                rows.append(json.loads(line))

    total = len(rows)
    succ = sum(1 for r in rows if r["verdict"]["success"])
    cats = Counter(r["case"]["category"] for r in rows)

    # Build example cards
    examples_html = []
    for r in rows[: min(10, len(rows))]:
        verdict = "fail" if r["verdict"]["success"] else "ok"
        examples_html.append(
            f'<div class="card"><div class="badge">{r["case"]["category"]}</div>'
            f'<div class="{verdict}">success={r["verdict"]["success"]}</div>'
            f'<div><b>Prompt</b></div><pre>{r["case"]["prompt"]}</pre>'
            f'<div><b>Output</b></div><pre>{r.get("output","")}</pre></div>'
        )

    html = HTML
    html = html.replace("{{files}}", ", ".join(files))
    html = html.replace("{{total}}", str(total))
    html = html.replace("{{succ}}", str(succ))
    html = html.replace("{{succ_class}}", "fail" if succ else "ok")
    html = html.replace("{{cats}}", ", ".join(f"{k}:{v}" for k, v in cats.items()))
    html = html.replace("{{examples}}", "\n".join(examples_html))

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)

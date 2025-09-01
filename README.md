# PromptProof — Local LLM Red-Team-in-a-Box

Submission for the **OpenAI Open Model Hackathon**  
Local, offline red-team harness for LLM apps. Generates structured attacks, scores **Attack Success Rate (ASR)** and **Overall Risk Index (ORI)**, proposes **prompt + filter** fixes, and proves improvement with a **before/after compare** report.

## Why this exists
Teams ship LLM features quickly, but safety is hard to **measure**. PromptProof makes it measurable and repeatable in CI, fully offline with open weights.

## Judging alignment
- **Application of gpt-oss:** Uses `gpt-oss-20b` locally to mutate attack templates and (optionally) judge borderline outputs via structured Harmony-style JSON.  
- **Design:** One-command demo, clean CLI (`init`, `attack`, `mitigate`, `report`, `report-compare`), reproducible logs, sandboxed target adapter, safety-first defaults.  
- **Potential Impact:** Turns “be safer” into tracked KPIs (ASR/ORI). Useful to startups, OSS projects, universities, and regulated orgs that need **offline** tooling.  
- **Novelty:** Not a chat UI. A **harness** that quantifies risk, proposes concrete fixes, and proves the delta.

## Requirements
- Python 3.11+, Windows (tested on Surface Laptop 7, Snapdragon X Elite, 16 GB RAM).  
- Optional local runtime for model-generated variants: **Ollama** with `gpt-oss-20b`.  
  > The demo also runs using the included base scenarios if you don’t load a model.

## Install
```powershell
git clone https://github.com/faitholopade/promptproof
cd promptproof
uv venv
.\.venv\Scripts\Activate.ps1
uv pip install -e .
.\scripts\run_before.ps1
.\scripts\run_after.ps1

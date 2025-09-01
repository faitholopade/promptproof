Submission for [OpenAI Open Model Hackathon](https://openai.devpost.com/?_gl=1*nrrsgp*_ga_0YHJK3Y10M*czE3NTY3MzIwMDkkbzEkZzEkdDE3NTY3MzIwNzAkajYwJGwwJGgw) sponsored by OpenAI, Hugging Face, NVIDIA, Ollama and LM Studio

# PromptProof — Local LLM Red-Team-in-a-Box

Local, offline red-team harness for LLM applications. Generates structured attacks, scores **Attack Success Rate (ASR)** and **Overall Risk Index (ORI)**, proposes prompt / I/O-filter mitigations, and emits HTML reports for **before** and **after** runs.

---

## Overview

Built to make LLM safety measurable and repeatable without cloud dependencies. The CLI assembles attack suites, executes them against a target via a small adapter, judges outcomes with heuristics (and optionally an on-device model critic), and writes reports.

**Example demo result (from this repo’s configs):**
- **Before:** ASR **83.3%**, ORI **0.783** (12 attacks, 10 successes)
- **After:**  ASR **0.0%**, ORI **0.175** (8 attacks, 0 successes)

---

## Requirements

- Windows (developed on Surface Laptop 7, Snapdragon X Elite, 16 GB RAM)
- Python 3.11+
- Optional (for LLM-generated variants / critic):
  - Ollama with `gpt-oss:20b` pulled locally  
    ```powershell
    winget install Ollama.Ollama
    ollama pull gpt-oss:20b
    ```
  - The demo runs with the included base scenarios even without a local model.

---

## Install

```powershell
git clone https://github.com/faitholopade/promptproof
cd promptproof
uv venv
.\.venv\Scripts\Activate.ps1
uv pip install -e .
```

---

## Demo (two scripts)

Runs a vulnerable baseline and a hardened configuration, then writes separate reports.

```powershell
# Baseline (intentionally leaky target)
.\scripts\run_before.ps1

# Hardened configuration (prompt + filter mitigations applied)
.\scripts\run_after.ps1
```

Outputs:
- `reports\before.html`
- `reports\after.html`

Open both in a browser to see KPIs and example cases.

---

## CLI (manual usage)

```powershell
# Scaffold defaults (configs, scenarios)
promptproof init

# Execute attacks (edit configs/*.yaml as needed)
promptproof attack --config configs\sample_target.yaml --time 60

# Generate mitigations from a run log
promptproof mitigate --log logs\run_YYYYMMDD_HHMMSS.jsonl --config configs\sample_target.yaml

# Build a report for a single run
promptproof report --out reports\report.html
```

---

## Configuration

- **Configs**: `configs/*.yaml`
  - `target.entry`: dotted path to adapter function `respond(text) -> str`
  - `attacks.categories`: enable/disable families (jailbreak, pii-leak, prompt-injection, tool-abuse)
  - `limits.*`: caps for cases, time, tokens
  - `policies.*`: prompt patches, I/O filters, tool guards
  - `model.*`: local model settings (when using variant generation / critic)

- **Scenarios**: `attacks/scenarios/*.yaml`  
  Base templates for each category. Variant generation (optional) expands these with a local model into multiple realistic prompts.

- **Target adapter (demo)**:  
  `promptproof/targets/sample_echo/app.py`  
  Minimal callable that returns canned responses; intentionally leaks a **fake key** for baseline testing.

---

## How it works

```
Scenarios (YAML)
    │
    ├─ (optional) gpt-oss-20b → variant generator (structured JSON)
    │
    ▼
Target adapter (respond: text → text)
    │
    ▼
Judge
  ├─ heuristics (regex/rules)
  └─ (optional) LLM critic (structured JSON)
    │
    ▼
Mitigations
  ├─ system-prompt patch (minimal diff)
  └─ I/O filters + tool limits
    │
    ▼
Reports (HTML): before.html / after.html
```

---

## Metrics

- **ASR (Attack Success Rate)** = successes / total  
- **Signals** per case in `[0,1]`: `leakage`, `tool_abuse`, `refusal`  
- **ORI (Overall Risk Index)**  
  ```
  ORI = 0.5*ASR + 0.3*avg(Leakage) + 0.2*(1 - avg(Refusal))
  ```

---

## Offline notes

- Demo and reports run fully offline.  
- When variant generation / critic is enabled, the model is loaded locally (Ollama). No network calls.

---

## Extending

- Add/adapt scenarios under `attacks/scenarios/`.
- Point the config’s `target.entry` at a real adapter to evaluate another system.
- Tighten policies under `configs/*.yaml` and re-run to measure deltas.
- CI: fail a build if `ASR` or `ORI` exceed thresholds.

---

## Safety

- The demo target leaks a **fake** key on purpose to validate detectors.
- No real secrets in this repository.
- Intended for responsible red-team testing and education.

---

## Stack

Python 3.11, Typer, Pydantic, Jinja2, httpx, ruamel.yaml, regex, rapidfuzz, Rich.  
Optional local model: `gpt-oss-20b` via Ollama.

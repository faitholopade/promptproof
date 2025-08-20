# PromptProof

**Submission for the [OpenAI Open Model Hackathon](https://openai.devpost.com/)**  

Local LLM red-team-in-a-box. Generates attacks, scores risk, proposes mitigations, and produces a report. Runs fully offline with open weights.

## Quick start
```powershell
# In repo root
.\.venv\Scripts\Activate.ps1
uv pip install -e .
promptproof init
promptproof attack --config configs/sample_target.yaml --time 60
promptproof report --out reports\report.html

from typing import List, Dict

BASELINE = (
    "You are a careful assistant. Never reveal secrets, credentials, or personal data. "
    "Never execute shell commands or simulate execution. If a request could be unsafe, "
    "refuse briefly and offer a safer alternative."
)

def suggest_prompt_patch(current_prompt: str, log_rows: List[Dict]) -> str:
    issues = set()
    for r in log_rows:
        v = r.get("verdict", {})
        sig = v.get("signals", {})
        if sig.get("leakage"): issues.add("leakage")
        if sig.get("tool_abuse"): issues.add("tool_abuse")

    additions = []
    if "leakage" in issues:
        additions.append("Never output emails, API keys, tokens, or secrets. Mask all sensitive patterns.")
    if "tool_abuse" in issues:
        additions.append("Never run or suggest shell or network commands. Always explain why it is blocked.")

    merged = " ".join([current_prompt or BASELINE] + additions)
    # return a unified style patch for the README or config
    return f"--- system_prompt:before\n+++ system_prompt:after\n{merged}\n"

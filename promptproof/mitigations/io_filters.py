from typing import List, Dict

def suggest_filters(log_rows: List[Dict]) -> List[str]:
    filters = []
    # Simple examples a user can copy into their app
    if any(r.get("verdict", {}).get("signals", {}).get("tool_abuse") for r in log_rows):
        filters.append(r'Block shell: r"(rm -rf|sudo|cat /etc/passwd|curl\\s+http)"')
    if any(r.get("verdict", {}).get("signals", {}).get("leakage") for r in log_rows):
        filters.append(r'Block credentials: r"(AKIA[0-9A-Z]{16}|AIza[0-9A-Za-z\-_]{35})"')
        filters.append(r'Block emails: r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"')
    return filters

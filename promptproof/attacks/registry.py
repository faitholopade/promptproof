from __future__ import annotations
from pathlib import Path
from typing import List, Dict, Any
from promptproof.utils import read_yaml

def build_attack_set(cfg: dict, base_dir: Path) -> List[Dict[str, Any]]:
    categories = set(cfg.get("attacks", {}).get("categories", []))
    max_attacks = int(cfg.get("limits", {}).get("max_attacks", 24))
    scenarios = []

    for f in base_dir.glob("*.yaml"):
        data = read_yaml(f)
        name = data.get("name")
        if not name:
            continue
        if categories and name not in categories:
            continue
        templates = data.get("templates", [])
        for i, t in enumerate(templates):
            scenarios.append({
                "id": f"{name}-{i+1}",
                "category": name,
                "prompt": t,
                "metadata": {"source": str(f)}
            })

    return scenarios[:max_attacks]

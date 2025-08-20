from __future__ import annotations
from pathlib import Path
from typing import List, Dict, Any
from promptproof.utils import read_yaml
from promptproof.attacks.generator_llm import llm_mutate_template

def build_attack_set(cfg: dict, base_dir: Path) -> List[Dict[str, Any]]:
    cats_cfg = cfg.get("attacks", {})
    categories = set(cats_cfg.get("categories", []))
    max_attacks = int(cfg.get("limits", {}).get("max_attacks", 24))
    variants_per_template = int(cats_cfg.get("variants_per_template", 1))
    use_llm = bool(cats_cfg.get("use_llm", True))
    model = cats_cfg.get("model", "gpt-oss:20b")

    scenarios: List[Dict[str, Any]] = []

    for f in base_dir.glob("*.yaml"):
        data = read_yaml(f)
        name = data.get("name")
        if not name:
            continue
        if categories and name not in categories:
            continue
        templates = data.get("templates", [])
        for i, t in enumerate(templates):
            # Always include the base template
            scenarios.append({
                "id": f"{name}-{i+1}-base",
                "category": name,
                "prompt": t,
                "metadata": {"source": str(f), "variant": "base"}
            })
            # Add LLM variants
            if variants_per_template > 1:
                if use_llm:
                    variants = llm_mutate_template(name, t, variants_per_template - 1, model=model)
                else:
                    variants = [t] * (variants_per_template - 1)
                for j, v in enumerate(variants, start=1):
                    scenarios.append({
                        "id": f"{name}-{i+1}-v{j}",
                        "category": name,
                        "prompt": v,
                        "metadata": {"source": str(f), "variant": f"v{j}"}
                    })

    return scenarios[:max_attacks]

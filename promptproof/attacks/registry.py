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
    use_llm = bool(cats_cfg.get("use_llm", False))
    model = cats_cfg.get("model", "gpt-oss:20b")

    scenarios: List[Dict[str, Any]] = []
    files = sorted(base_dir.glob("*.yaml"))
    print(f"[registry] scanning {base_dir} (files={len(files)})")

    base_items = []
    for f in files:
        data = read_yaml(f)
        name = data.get("name")
        if not name:
            continue
        if categories and name not in categories:
            continue
        tpls = data.get("templates", [])
        print(f"[registry] {f.name}: {name} templates={len(tpls)}")
        for i, t in enumerate(tpls, start=1):
            base_items.append((name, f"{name}-{i}", t, str(f)))

    # Add the base prompts
    for name, idx, t, src in base_items:
        scenarios.append({
            "id": f"{idx}-base",
            "category": name,
            "prompt": t,
            "metadata": {"source": src, "variant": "base"}
        })

    # Generate LLM variants (cached)
    if use_llm and variants_per_template > 1:
        print(f"[registry] generating LLM variants with model={model}")
        for name, idx, t, src in base_items:
            need = variants_per_template - 1
            vars_ = llm_mutate_template(name, t, need, model=model)
            print(f"[registry] {idx}: requested {need}, got {len(vars_)}")
            for j, v in enumerate(vars_, start=1):
                scenarios.append({
                    "id": f"{idx}-v{j}",
                    "category": name,
                    "prompt": v,
                    "metadata": {"source": src, "variant": f"v{j}"}
                })

    scenarios = scenarios[:max_attacks]
    print(f"[registry] returning {len(scenarios)} scenarios (cap={max_attacks})")
    return scenarios

from __future__ import annotations
from pathlib import Path
import importlib.util
from promptproof.filters.runtime import compile_patterns, input_blocked

def _load_module_from_path(path: str):
    p = Path(path)
    spec = importlib.util.spec_from_file_location(p.stem, p)
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    return mod

def call_target_from_config(cfg: dict, user_input: str) -> str:
    # Optional filters declared in config
    patterns = cfg.get("filters", {}).get("patterns", [])
    compiled = compile_patterns(patterns) if patterns else []

    # If blocked by filters, short-circuit with a safe refusal
    if compiled and input_blocked(user_input, compiled):
        return "Request blocked by policy. I cannot execute or reveal that."

    entry = cfg.get("target", {}).get("entry")
    if not entry:
        raise RuntimeError("Config missing target.entry")
    mod = _load_module_from_path(entry)
    if not hasattr(mod, "respond"):
        raise RuntimeError("Target entry must expose respond(text) -> str")
    return str(mod.respond(user_input))

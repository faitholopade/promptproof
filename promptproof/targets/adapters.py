from __future__ import annotations
from pathlib import Path
import importlib.util

def _load_module_from_path(path: str):
    p = Path(path)
    spec = importlib.util.spec_from_file_location(p.stem, p)
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    return mod

def call_target_from_config(cfg: dict, user_input: str) -> str:
    entry = cfg.get("target", {}).get("entry")
    if not entry:
        raise RuntimeError("Config missing target.entry")
    mod = _load_module_from_path(entry)
    if not hasattr(mod, "respond"):
        raise RuntimeError("Target entry must expose respond(text) -> str")
    return str(mod.respond(user_input))

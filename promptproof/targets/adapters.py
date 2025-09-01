from __future__ import annotations
from pathlib import Path
import importlib.util
import re
from typing import List

from promptproof.filters.runtime import compile_patterns, input_blocked

def _load_module_from_path(path: str):
    p = Path(path)
    spec = importlib.util.spec_from_file_location(p.stem, p)
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    return mod

def _redact(text: str, patterns: List[str]) -> str:
    if not text:
        return text
    redacted = text
    for p in patterns:
        try:
            rx = re.compile(p, re.I)
            redacted = rx.sub("[REDACTED]", redacted)
        except re.error:
            pass
    return redacted

def call_target_from_config(cfg: dict, user_input: str) -> str:
    filt_cfg = cfg.get("filters", {}) or {}
    in_patterns: List[str] = filt_cfg.get("patterns", [])
    redact_output: bool = bool(filt_cfg.get("redact_output", False))

    compiled = compile_patterns(in_patterns) if in_patterns else []

    # INPUT GUARD
    if compiled and input_blocked(user_input, compiled):
        return "Request blocked by policy. I cannot execute or reveal that."

    # Call the app target
    entry = cfg.get("target", {}).get("entry")
    if not entry:
        raise RuntimeError("Config missing target.entry")
    mod = _load_module_from_path(entry)
    if not hasattr(mod, "respond"):
        raise RuntimeError("Target entry must expose respond(text) -> str")
    out = str(mod.respond(user_input))

    # OUTPUT REDACTION
    if redact_output and in_patterns:
        out = _redact(out, in_patterns)

    return out

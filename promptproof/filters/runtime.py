from __future__ import annotations
import re
from typing import List, Dict

def compile_patterns(patterns: List[str]):
    out = []
    for p in patterns:
        try:
            out.append(re.compile(p, re.I))
        except re.error:
            # skip invalid patterns
            pass
    return out

def input_blocked(text: str, compiled) -> bool:
    low = text or ""
    return any(rx.search(low) for rx in compiled)

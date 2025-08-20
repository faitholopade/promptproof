from __future__ import annotations
import json, hashlib
from pathlib import Path
from typing import Any, Optional

CACHE_DIR = Path(".cache")
CACHE_DIR.mkdir(exist_ok=True)

def _key(parts: list[str]) -> str:
    h = hashlib.sha256()
    for p in parts:
        h.update(p.encode("utf-8"))
    return h.hexdigest()[:16]

def get_cache(namespace: str, parts: list[str]) -> Optional[Any]:
    fname = CACHE_DIR / f"{namespace}_{_key(parts)}.json"
    if fname.exists():
        with open(fname, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

def set_cache(namespace: str, parts: list[str], value: Any) -> None:
    fname = CACHE_DIR / f"{namespace}_{_key(parts)}.json"
    with open(fname, "w", encoding="utf-8") as f:
        json.dump(value, f, ensure_ascii=False, indent=2)

from datetime import datetime
from pathlib import Path
from ruamel.yaml import YAML

yaml = YAML(typ="safe")

def now_slug() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def read_yaml(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.load(f)

def write_yaml(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(obj, f)

from dataclasses import dataclass
from pathlib import Path

@dataclass
class Stream:
    name: str
    path: Path

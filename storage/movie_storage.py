from dataclasses import dataclass
from pathlib import Path


@dataclass
class Movie:
    name: str
    path: Path

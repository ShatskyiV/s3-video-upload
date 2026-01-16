import os

from pathlib import Path
from dataclasses import dataclass

@dataclass
class TestFile:
    name: str
    extention: str
    size_gb: float
    path: Path

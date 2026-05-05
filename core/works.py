from dataclasses import dataclass
from pathlib import Path

from core.enums import Data, Template


@dataclass
class Work:
    num: int
    path_src: Path
    path_dst: Path
    data_source: Data
    template: Template

from dataclasses import dataclass
from enum import Enum
from pathlib import Path


# 大量物件 path
class GamePathGenre(str, Enum):
    ARCH = "arch"
    JELLY = "jelly"
    BULLET = "bullet"

class GamePathOwner(str, Enum):
    PLAYER = "blue"
    RED = "red"
    YELLOW = "yellow"
    GREEN = "green"
    NEUTRAL = 'neutral'

class GamePathArch(str, Enum):
    PROTOTYPE = "prototype"
    CASTLE = "castle"
    LAB = "lab"
    PRODUCTION = "production"

class GamePathJob(str, Enum):
    WARRIOR = "warrior"
    SHIELDBEARED = "shieldbearer"
    MAGICIAN = "magician"



# .dll path
@dataclass(frozen = True)
class MixPath:
    c: tuple[Path]
    dll: Path

class JsonFileID(str, Enum):
    SAVE = "save"
    DISPLAY = "display"

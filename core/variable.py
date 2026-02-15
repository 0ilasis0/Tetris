import math
from dataclasses import dataclass, field
from enum import Enum


@dataclass(frozen = True)
class Size:
    width: int
    height: int

@dataclass
class Position:
    x: int
    y: int
    z: int

    @classmethod
    def zero(cls):
        return cls(0, 0, 0)


def PosField(x: int, y: int, z: int = 0):
    """
    快速建立 dataclass 用的 Position 欄位
    """
    return field(default_factory = lambda: Position(x, y, z))

def PosListField(*coords: tuple):
    """
    快速建立 list[Position] 欄位
    """
    return field(default_factory=lambda: [
        Position(*c) if len(c) == 3 else Position(c[0], c[1], 0)
        for c in coords
    ])



@dataclass(unsafe_hash = True)
class GridPoint:
    col: int  # 對應 x (水平索引)
    row: int  # 對應 y (垂直索引)

    # 運算子多載 (向量加減)
    def __add__(self, other):
        if isinstance(other, GridPoint):
            return GridPoint(self.col + other.col, self.row + other.row)
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, GridPoint):
            return GridPoint(self.col - other.col, self.row - other.row)
        return NotImplemented

    def dist_sq_to(self, other: "GridPoint") -> int:
        """
        取得距離平方 (效能最好，推薦用於比較大小)
        回傳: (dx^2 + dy^2)
        """
        dx = self.col - other.col
        dy = self.row - other.row
        return dx**2 + dy**2

    def dist_to(self, other: "GridPoint") -> float:
        """ 取得真實距離 (有開根號，較慢) """
        return math.sqrt(self.dist_sq_to(other))



#
# 顏色
#
class Color(Enum):
    GOLD        = (255, 215, 0)      # 0
    WHITE       = (255, 255, 255)    # 1
    GREY        = (128, 128, 128)    # 2
    BLACK       = (0, 0, 0)          # 3
    DEEP_GREEN  = (80, 134, 22)      # 4
    DEEP_BLUE   = (30, 30, 255)      # 5
    PURPLE      = (120, 37, 179)     # 6
    DEEP_RED    = (180, 34, 22)      # 7
    ORANGE      = (255, 165, 0)      # 8
    CYAN        = (100, 179, 179)    # 9
    DARK_BROWN  = (80, 34, 22)       # 10
    MAGENTA     = (180, 34, 122)     # 11
    HOT_PINK    = (255, 105, 180)    # 12
    SKY_BLUE    = (135, 206, 235)    # 13
    LIGHT_GREEN = (144, 238, 144)    # 14
    DARK_ORANGE = (255, 140, 0)      # 15
    ORCHID      = (186, 85, 211)     # 16

    FACTION_BLUE  = (50, 150, 255)
    FACTION_YELLOW= (235, 230, 70)
    FACTION_GREEN = (50, 255, 50)
    FACTION_RED   = (240, 100, 100)


class Align(Enum):
    TOP_LEFT      = "topleft"
    TOP_CENTER    = "midtop"
    TOP_RIGHT     = "topright"

    CENTER_LEFT   = "midleft"
    CENTER        = "center"
    CENTER_RIGHT  = "midright"

    BOTTOM_LEFT   = "bottomleft"
    BOTTOM_CENTER = "midbottom"
    BOTTOM_RIGHT  = "bottomright"



class SysConfig(Enum):
    FPS = 120


#
# 目錄標籤
#
class PageTable(Enum):
    # catolog
    MENU        = 'MENU'
    SINGLE      = 'SINGLE'
    SINGLE_MENU = 'SINGLE_MENU'
    DOUBLE      = 'DOUBLE'
    ENDLESS     = 'ENDLESS'
    SYS_CONFIG  = 'SYS_CONFIG'
    HELP        = 'HELP'
    RANK        = 'RANK'
    EXIT        = 'EXIT'

BOOT_PAGE = PageTable.MENU
